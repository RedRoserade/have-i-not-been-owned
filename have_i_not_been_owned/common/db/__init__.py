import pymongo

from have_i_not_been_owned.common.config import mongo


def get_db(url: str = None):
    if url is None:
        url = mongo['url']

    client = pymongo.MongoClient(url)

    return client.get_database()


def get_breached_emails_collection(db=None):
    if db is None:
        db = get_db()

    return db.get_collection('breached_emails')


def get_breached_email_domains_collection(db=None):
    if db is None:
        db = get_db()

    return db.get_collection('breached_email_domains')


def get_data_breaches_collection(db=None):
    if db is None:
        db = get_db()

    return db.get_collection('data_breaches')
