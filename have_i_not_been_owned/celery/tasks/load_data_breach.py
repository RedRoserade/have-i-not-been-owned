import io
import logging
import os
import tempfile
from collections import Counter
from urllib.parse import urlparse

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from pymongo import UpdateOne

from have_i_not_been_owned.common.db import get_breached_emails_collection, get_db, \
    get_breached_email_domains_collection
from have_i_not_been_owned.common.email import normalize_email

logger: logging.Logger = get_task_logger(__name__)

_SUPPORTED_EXTENSIONS = ('.txt',)
_MAX_BULK_SIZE = 100_000


@shared_task
def load_data_breach(*, source_url: str, breach: dict):

    _, ext = os.path.splitext(urlparse(source_url).path)

    if ext.lower() not in _SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported extension: {ext!r}, supported extensions are {_SUPPORTED_EXTENSIONS!r}")

    breach_file = _download_breach_file(ext, source_url)

    try:
        return _process_breach_file(breach_file, breach['name'])
    finally:
        if os.path.isfile(breach_file):
            os.remove(breach_file)


def _process_breach_file(breach_file: str, breach_name: str):

    db = get_db()

    breached_emails = get_breached_emails_collection(db)
    breached_domains = get_breached_email_domains_collection(db)

    # Use MongoDB's bulk operations to reduce the number of database accesses, at the cost of memory usage.
    email_address_bulk = []

    email_totals = Counter()
    domain_totals = Counter()

    # The number of distinct domains will be far fewer than the number of emails processed.
    # So, use a Set for storing the distinct domains, and flush it as it exceeds a given size.
    domains_cache = set()

    def dump_domains():
        domain_bulk = [
            UpdateOne(
                {'domain': domain},
                {
                    # Store the breaches in here too. It's de-normalization, but it should help speeding up
                    # knowing which breaches an email domain has been part of. Otherwise `distinct`-like
                    # queries would have to be applied on the email collection,
                    # which could be costly, even with indexes.
                    '$addToSet': {
                        'breaches': breach_name,
                    },
                    '$setOnInsert': {'domain': domain},
                },
                upsert=True
            )
            for domain in domains_cache
        ]

        result = breached_domains.bulk_write(domain_bulk, ordered=False)

        domain_totals.update(
            processed=len(domain_bulk),
            matched=result.matched_count,
        )

    def dump_emails():
        return

        result = breached_emails.bulk_write(email_address_bulk, ordered=False)

        email_totals.update(
            processed=len(email_address_bulk),
            matched=result.matched_count,
        )

    with open(breach_file, 'r') as breach_file_reader:
        for line in breach_file_reader.readlines():
            normalized_email = normalize_email(email=line)

            # Skip invalid email addresses.
            if not normalized_email:
                continue

            # I don't think that using upsert is the best way to do this performance-wise, especially
            # as collection size grows.
            email_address_bulk.append(
                UpdateOne(
                    {'email': normalized_email['email']},
                    {
                        '$addToSet': {
                            'breaches': breach_name,
                        },
                        '$setOnInsert': normalized_email,
                    },
                    upsert=True
                )
            )

            domains_cache.add(normalized_email['domain'])

            # Split the bulk into smaller chunks to minimize memory pressure, resetting it
            # after it's sent to the server.
            if len(domains_cache) > _MAX_BULK_SIZE:
                dump_domains()
                domains_cache = set()

            if len(email_address_bulk) >= _MAX_BULK_SIZE:
                dump_emails()
                email_address_bulk = []

    # Flush any remaining operations for the domains and emails.
    if len(email_address_bulk) > 0:
        dump_emails()

    if len(domains_cache) > 0:
        dump_domains()

    return {
        'emails': email_totals,
        'domains': domain_totals,
    }


def _download_breach_file(extension: str, source_url: str) -> str:
    handle, fname = tempfile.mkstemp(extension)

    logger.debug("Downloading breach file %r to %r", source_url, fname)

    with requests.get(source_url, stream=True) as response, open(handle, 'wb') as breach_file_writer:

        response.raise_for_status()

        for chunk in response.iter_content(chunk_size=io.DEFAULT_BUFFER_SIZE):
            breach_file_writer.write(chunk)

    logger.debug("Breach file at %r downloaded successfully.", source_url)

    return fname
