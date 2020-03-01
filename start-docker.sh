#!/usr/bin/env bash

docker-compose -f docker-compose.deps.yaml -f docker-compose.app.yaml up -d --build