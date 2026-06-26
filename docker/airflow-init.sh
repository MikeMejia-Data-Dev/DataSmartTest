#!/bin/bash

set -e

echo "======================================"
echo "Initializing Airflow"
echo "======================================"

echo "Running database migrations..."

airflow db migrate

echo "Creating Admin User..."

airflow users create \
    --username "$AIRFLOW_USER" \
    --password "$AIRFLOW_PASSWORD" \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@datamart.com || true

echo "Importing Variables..."

airflow variables import /opt/airflow/docker/variables.json

echo "Creating Connections..."

bash /opt/airflow/docker/connections.sh

echo "======================================"
echo "Initialization Finished Successfully"
echo "======================================"