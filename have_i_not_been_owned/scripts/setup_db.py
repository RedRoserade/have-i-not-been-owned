from have_i_not_been_owned.common.db import get_db, get_breached_emails_collection, \
    get_breached_email_domains_collection, get_data_breaches_collection


def main():
    db = get_db()

    _setup_data_breaches_collection(db)
    _setup_breached_email_domains_collection(db)


def _setup_data_breaches_collection(db):
    coll = get_breached_emails_collection(db)

    coll.create_index(
        keys=[('email', 1)],
        unique=True,
        name='email_asc_unique'
    )

    coll.create_index(
        keys=[('domain', 1)],
        name='domain_asc'
    )


def _setup_breached_email_domains_collection(db):
    coll = get_breached_email_domains_collection(db)

    coll.create_index(
        keys=[('domain', 1)],
        unique=True,
        name='domain_asc_unique'
    )


def _setup_breaches_collection(db):
    coll = get_data_breaches_collection(db)

    coll.create_index(
        keys=[('domain', 1)],
        unique=True,
        name='domain_asc_unique'
    )


if __name__ == '__main__':
    main()
