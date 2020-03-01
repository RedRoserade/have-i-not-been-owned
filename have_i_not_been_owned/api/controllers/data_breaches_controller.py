import logging
import os
import uuid
from datetime import datetime

from dateutil.tz import tz
from pymongo.errors import DuplicateKeyError
from werkzeug.exceptions import BadRequest

from have_i_not_been_owned.api.exceptions import BreachNameAlreadyExists
from have_i_not_been_owned.celery import app
from have_i_not_been_owned.celery.tasks import load_data_breach
from have_i_not_been_owned.common.celery.utils import read_async_result
from have_i_not_been_owned.common.config import cos
from have_i_not_been_owned.common.db import get_data_breaches_collection
from have_i_not_been_owned.common.s3 import create_presigned_post, create_presigned_url
from have_i_not_been_owned.common.utils.text import slugify

logger = logging.getLogger(__name__)


def prepare_data_breach_upload_url(body):
    file_name = os.path.basename(os.path.normpath(body['file_name'])).strip()

    if not file_name:
        # In theory it should never happen as we have schema validation
        raise BadRequest()

    data_breaches_base_key = cos['data_breach_uploads']['key_prefix']

    key = f'{data_breaches_base_key}/{uuid.uuid4()}/{file_name}'

    # We need two URLs, one to do the upload, and one to then download (on the task)
    signed_post = create_presigned_post(key)
    signed_url = create_presigned_url(key)

    return {
        'post': signed_post,
        'get': signed_url,
    }


def process_data_breach(body):

    breach_name = body['breach']['name']

    breach = {
        'id': slugify(breach_name),
        'name': breach_name,
        'inserted_at': datetime.now(tz.UTC),
    }

    data_breaches = get_data_breaches_collection()

    try:
        data_breaches.insert_one(breach)
    except DuplicateKeyError:
        logger.warning("The breach %r already exists at %r", breach['name'], breach['id'])
        raise BreachNameAlreadyExists(breach['name'])

    # We don't need the ID, and it breaks Celery
    del breach['_id']

    logger.info("Starting data breach import for %r", breach['id'])

    # Launch Celery Task and return its info and the breach to the caller.
    sig = load_data_breach.s(
        source=body['breach_source'],
        breach=breach,
    )

    # HACK for some damn reason the `apply_async` is returning the default Celery App with no backend.
    result = app.AsyncResult(sig.apply_async().id)

    return {
        'breach': breach,
        'load_task': read_async_result(result),
    }
