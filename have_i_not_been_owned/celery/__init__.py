from celery import Celery

from have_i_not_been_owned.celery import celeryconfig

app = Celery()

app.config_from_object(celeryconfig)
