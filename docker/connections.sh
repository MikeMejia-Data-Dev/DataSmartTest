#!/bin/bash

set -e

echo "======================================"
echo "Creating Airflow Connections..."
echo "======================================"

if airflow connections get postgres_dw >/dev/null 2>&1; then
    echo "Connection postgres_dw already exists."
else
    airflow connections add postgres_dw \
        --conn-type postgres \
        --conn-host "$DW_DB_HOST" \
        --conn-login "$DW_DB_USER" \
        --conn-password "$DW_DB_PASSWORD" \
        --conn-port "$DW_DB_PORT" \
        --conn-schema "$DW_DB_NAME"

    echo "Connection postgres_dw created."
fi