FROM apache/airflow:2.10.5-python3.10

LABEL maintainer="Nikita Yurasov <nikitayurasov@yahoo.com>"
SHELL ["/bin/bash", "-o", "pipefail", "-o", "errexit", "-o", "nounset", "-o", "xtrace", "-c"]

USER root

RUN apt-get update --allow-releaseinfo-change \
    && apt-get install --no-install-recommends -y \
        build-essential \
        libpq-dev

COPY . ${AIRFLOW_HOME}/sqlmesh_af
COPY sqlmesh_af ${AIRFLOW_HOME}/sqlmesh_af/sqlmesh_af
COPY examples/dags ${AIRFLOW_HOME}/sqlmesh_af/dags

RUN chown -R airflow:0 ${AIRFLOW_HOME}/sqlmesh_af

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

USER airflow

RUN uv pip install -e "${AIRFLOW_HOME}/sqlmesh_af"
