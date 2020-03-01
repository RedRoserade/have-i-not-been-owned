#!/usr/bin/env bash

set -e

python -m have_i_not_been_owned.scripts.setup_db
python -m have_i_not_been_owned.scripts.setup_s3
