#!/usr/bin/env bash

set -e

case "${1}" in
  run-setup)
    exec ./scripts/run-setup.sh
    ;;
  run-celery)
    exec ./scripts/run-celery.sh
    ;;
  run-api)
    exec ./scripts/run-api.sh
    ;;
  *)
    echo "Unknown option '${1}', valid options are 'run-setup', 'run-celery', 'run-api'"
    exit 1
esac
