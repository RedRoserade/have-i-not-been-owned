import logging

from have_i_not_been_owned.common.db import get_db, get_breached_emails_collection, \
    get_breached_email_domains_collection, get_data_breaches_collection

logger = logging.getLogger(__name__)


def main():
    logger.info("Setting up the DB")

    db = get_db()

    _setup_breached_emails_collection(db)
    _setup_breached_email_domains_collection(db)
    _setup_breaches_collection(db)


def _setup_breached_emails_collection(db):
    logger.info("Setting up breached emails collection")

    coll = get_breached_emails_collection(db)

    # Create a surrogate key on the email to detect duplicates
    coll.create_index(
        keys=[('email', 1)],
        unique=True,
        name='email_asc_unique'
    )

    # Helps querying emails by domain
    coll.create_index(
        keys=[('domain', 1)],
        name='domain_asc'
    )


def _setup_breached_email_domains_collection(db):
    logger.info("Setting up breached email domains collection")

    coll = get_breached_email_domains_collection(db)

    coll.create_index(
        keys=[('domain', 1)],
        unique=True,
        name='domain_asc_unique'
    )


def _setup_breaches_collection(db):
    logger.info("Setting up data breaches collection")

    coll = get_data_breaches_collection(db)

    coll.create_index(
        keys=[('id', 1)],
        unique=True,
        name='id_asc_unique'
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    logger.setLevel(logging.INFO)
    main()
