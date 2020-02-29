from celery.result import AsyncResult


def read_async_result(result: AsyncResult):
    return {
        'state': result.state,
        'task_id': result.task_id
    }
