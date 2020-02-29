import os

broker_url = os.getenv('HINBO_BROKER_URL', 'amqp://localhost:5672')
result_backend = os.getenv('HINBO_RESULT_BACKEND', 'redis://localhost:6379/0')

accept_content = ["json"]
task_serializer = "json"

# Ensure that celery are not lost if workers die or exit (OOM, SIGTERM, SIGKILL)
task_track_started = True
task_acks_late = True
task_reject_on_worker_lost = True
worker_prefetch_multiplier = 1

task_ignore_result = False

# Reference our task functions
imports = [
    'have_i_not_been_owned.celery.tasks',
]
