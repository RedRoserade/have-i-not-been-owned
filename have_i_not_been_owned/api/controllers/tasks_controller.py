from celery.result import AsyncResult

from have_i_not_been_owned.celery import app
from have_i_not_been_owned.common.celery.utils import read_async_result


def get_task_status(task_id: str):
    return read_async_result(app.AsyncResult(task_id))
