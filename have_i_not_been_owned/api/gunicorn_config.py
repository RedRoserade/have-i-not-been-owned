import os

bind = f":{int(os.getenv('PORT', '8080'))}"

worker_class = "gevent"
workers = int(os.getenv('HINBO_API_NUM_WORKERS', '4'))
