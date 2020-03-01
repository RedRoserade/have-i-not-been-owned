import os

bind = f":{int(os.getenv('PORT', '8080'))}"

# Interesting, 'gevent' is causing trouble when Celery tasks are involved. Maybe I need to do some monkey patching...
# worker_class = "gevent"
# workers = int(os.getenv('HINBO_API_NUM_WORKERS', '4'))

loglevel = "info"
