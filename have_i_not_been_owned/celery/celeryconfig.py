import os

from have_i_not_been_owned.common.config import amqp, redis

broker_url = amqp["url"]
result_backend = redis["url"]

accept_content = ["json"]
task_serializer = "json"

# Ensure that tasks are not lost if workers die or exit (OOM, SIGTERM, SIGKILL)
task_track_started = True
task_acks_late = True
task_reject_on_worker_lost = True
worker_prefetch_multiplier = 1

task_ignore_result = False

# Reference our task functions
imports = [
    'have_i_not_been_owned.celery.tasks',
]
