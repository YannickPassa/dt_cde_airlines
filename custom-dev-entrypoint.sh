#!/bin/bash

set -e
set -x

set -o allexport
source .env-base
set +o allexport



# Run database migrations
airflow db migrate

# Import DAG variables (only if file exists)
if [ -f "dag-variables.json" ]; then
    airflow variables import dag-variables.json
fi

exec /entrypoint "standalone"