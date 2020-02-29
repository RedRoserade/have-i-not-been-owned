from have_i_not_been_owned.common.db import get_db


def main():
    db = get_db()

    data_breaches = db.get_collection('data_breaches')

    data_breaches.create_index(
        keys=[('email', 1)],
        unique=True,
        name='email_asc_unique'
    )

    data_breaches.create_index(
        keys=[('domain', 1)],
        name='domain_asc'
    )

    # Could consider creating an index for the breaches...


if __name__ == '__main__':
    main()
