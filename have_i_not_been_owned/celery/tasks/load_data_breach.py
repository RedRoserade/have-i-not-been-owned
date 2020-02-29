import io
import logging
import os
import tempfile
from typing import Optional
from urllib.parse import urlparse

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from pymongo import UpdateOne

from have_i_not_been_owned.common.db import get_db

logger: logging.Logger = get_task_logger(__name__)

_SUPPORTED_EXTENSIONS = ('.txt',)
_MAX_BULK_SIZE = 100_000


@shared_task
def load_data_breach(*, source_url: str, breach_name: str):

    _, ext = os.path.splitext(urlparse(source_url).path)

    if ext.lower() not in _SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported extension: {ext!r}, supported extensions are {_SUPPORTED_EXTENSIONS!r}")

    breach_file = _download_breach_file(ext, source_url)

    try:
        return _process_breach_file(breach_file, breach_name)
    finally:
        if os.path.isfile(breach_file):
            os.remove(breach_file)


def _process_breach_file(breach_file: str, breach_name: str):

    db = get_db()

    data_breaches = db.get_collection('data_breaches')

    # Use MongoDB's bulk operations to reduce the number of database accesses, at the cost of memory usage.
    bulk = []

    total_processed = 0
    total_matched = 0

    with open(breach_file, 'r') as breach_file_reader:
        for line in breach_file_reader.readlines():
            normalized_email = _normalize_email(email=line)

            # Skip invalid email addresses.
            if not normalized_email:
                continue

            bulk.append(
                # I don't think that using upsert is the best way to do this performance-wise, especially
                # as collection size grows.
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

            # Split the bulk into smaller chunks to minimize memory pressure, resetting it
            # after it's sent to the server.
            if len(bulk) >= _MAX_BULK_SIZE:
                result = data_breaches.bulk_write(bulk, ordered=False)

                total_processed += len(bulk)
                total_matched += result.matched_count

                bulk = []

    # Flush any remaining operations.
    if len(bulk) > 0:
        data_breaches.bulk_write(bulk, ordered=False)

        total_processed += len(bulk)
        total_matched += result.matched_count

    return {
        'total_processed': total_processed,
        'total_matched': total_matched
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


def _normalize_email(email: str) -> Optional[dict]:
    if not email or not email.strip():
        return None

    email = email.strip().upper()
    domain = _get_domain(email)

    # Reject emails that don't have the domain set.
    if not domain:
        return None

    return {
        'email': email,
        'domain': domain
    }


def _get_domain(email: str) -> Optional[str]:
    domain = email.split('@')[-1].strip()

    if domain == email:
        return None

    return domain
