#!/usr/bin/env bash

gunicorn \
  -c have_i_not_been_owned/api/gunicorn_config.py \
  have_i_not_been_owned.api:app
