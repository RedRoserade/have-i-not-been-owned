from bson import ObjectId
from werkzeug.exceptions import BadRequest

from have_i_not_been_owned.api.exceptions import DomainNotFound, EmailNotFound
from have_i_not_been_owned.common.db import get_breached_emails_collection, get_breached_email_domains_collection, \
    get_db
from have_i_not_been_owned.common.email import normalize_email


def get_breached_email(email: str):
    data_breaches = get_breached_emails_collection()

    normalized_email = normalize_email(email)

    if normalized_email is None:
        # In theory it shouldn't happen due to schema validation
        raise BadRequest("Invalid email address")

    breached_email = data_breaches.find_one({'email': normalized_email['email']})

    if breached_email is None:
        raise EmailNotFound(email)

    return _read_breached_email(breached_email)


def _read_breached_email(breached_email):
    return {
        '_id': breached_email['_id'],
        'email': breached_email['email'],
        'domain': breached_email['domain'],
        'breaches': [{'id': breach_id} for breach_id in breached_email['breaches']]
    }


def get_breached_domain(domain: str, after: str = None, limit: int = 100):
    db = get_db()

    domain_query = {'domain': domain.upper()}

    breached_domain = get_breached_email_domains_collection(db).find_one(domain_query)

    if breached_domain is None:
        raise DomainNotFound(domain)

    breached_emails = get_breached_emails_collection(db)

    # TODO This is expensive, and should be cached.
    total_breached_emails = breached_emails.count_documents(domain_query)

    if after is not None:
        domain_query['_id'] = {'$gt': ObjectId(after)}

    breached_emails_cursor = breached_emails.find(domain_query).limit(limit)

    with breached_emails_cursor:
        breached_emails_page = [
            _read_breached_email(breached_email) for breached_email in breached_emails_cursor
        ]

    return {
        'total_emails': total_breached_emails,
        'emails_page': breached_emails_page,
        'breaches': [{'id': breach_id} for breach_id in breached_domain['breaches']]
    }
