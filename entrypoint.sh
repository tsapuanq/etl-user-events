#!/bin/bash

airflow db migrate


airflow users create \
    --username admin \
    --firstname Air \
    --lastname Flow \
    --role Admin \
    --email admin@example.com \
    --password admin

airflow scheduler & airflow webserver