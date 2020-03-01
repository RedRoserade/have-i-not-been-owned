#!/usr/bin/env bash

set -eu

HINBO_CELERY_NUM_WORKERS="${HINBO_CELERY_NUM_WORKERS:-4}"
HINBO_CELERY_LOG_LEVEL="${HINBO_CELERY_LOG_LEVEL:-INFO}"

celery worker \
  -A have_i_not_been_owned.celery \
  -c "${HINBO_CELERY_NUM_WORKERS}" \
  -l "${HINBO_CELERY_LOG_LEVEL}"
