#!/usr/bin/env bash

set -eu

HINBO_RUN_SETUP="${HINBO_RUN_SETUP:-1}"

if [[ "${HINBO_RUN_SETUP}" == "1" ]]; then
  echo "Running setup"

  python -m have_i_not_been_owned.scripts.setup_db
  python -m have_i_not_been_owned.scripts.setup_s3
fi

