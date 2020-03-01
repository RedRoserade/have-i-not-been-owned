#!/usr/bin/env bash

set -e

breach_name="${1:?Specify a breach name}"
breach_file="${2:?Specify a breach file in the 'data_breaches' directory}"

docker-compose -f docker-compose.deps.yaml -f docker-compose.app.yaml \
  exec api \
  python -m have_i_not_been_owned.scripts.upload_data_breach \
  --file "/data_breaches/${breach_file}" \
  --name "${breach_name}" \
  --api http://localhost:8080/api/v1/
