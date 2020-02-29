import pymongo

from have_i_not_been_owned.common.config import db_url


def get_db(url: str = None):
    if url is None:
        url = db_url

    client = pymongo.MongoClient(url)

    return client.get_database()
