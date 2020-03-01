import logging
import time

import celery.result
import argparse
import os
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)


def main():
    args = _get_args()

    signed_url = _upload_breach_file(args)

    result = _launch_process(args, signed_url)

    logger.info("Breach: %r", result['breach'])

    task = _wait_for_task(args, result['load_task'])

    if task['state'] in celery.result.states.EXCEPTION_STATES:
        logger.error('Task %r failed with status %r', task['task_id'], task['state'])
        raise SystemExit(1)
    else:
        logger.info('Task %r finished successfully.', task['task_id'])


def _get_args():
    parser = argparse.ArgumentParser(description='Upload data breach')

    parser.add_argument('--file', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--api', default='http://localhost:5000/api/v1/')

    return parser.parse_args()


def _get_signed_urls(args):
    response = requests.post(urljoin(args.api, 'data_breaches/upload_url'), json={
        'file_name': os.path.basename(args.file)
    })

    response.raise_for_status()

    return response.json()


def _upload_breach_file(args) -> str:
    logger.info("Uploading breach file...")
    with open(args.file, 'rb') as breach_file_reader:
        signed_urls = _get_signed_urls(args)

        post = signed_urls['post']
        files = {'file': (post['fields']['key'], breach_file_reader)}

        response = requests.post(post['url'], data=post['fields'], files=files)
    response.raise_for_status()

    return signed_urls['get']


def _get_task(args, task_id):
    response = requests.get(urljoin(args.api, f'tasks/{task_id}'))

    response.raise_for_status()

    return response.json()


def _launch_process(args, signed_url):
    logger.info("Launching process...")
    response = requests.post(urljoin(args.api, 'data_breaches'), json={
        'breach': {'name': args.name},
        'breach_source': {'url': signed_url}
    })

    response.raise_for_status()

    return response.json()


def _wait_for_task(args, task):
    while task['state'] not in celery.result.states.READY_STATES:
        logger.info(f'Task {task["task_id"]!r} is {task["state"]!r}...')

        time.sleep(10)

        task = _get_task(args, task['task_id'])

    return task


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    logger.setLevel(logging.INFO)
    main()
