import os
from celery import Celery

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')

# :TODO вынести в core/settings.py
redis_url = "redis://%s:%s" % (redis_host, redis_port)
celery_app = Celery("worker", broker=redis_url)
celery_app.conf.task_routes = {"app.tasks.*": "main-queue"}
celery_app.conf.result_backend = 'redis'

