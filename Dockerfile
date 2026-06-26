FROM apache/airflow:3.2.0

USER root

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY --chown=airflow:root requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY --chown=airflow:root docker /opt/airflow/docker