FROM apache/airflow:3.1.2-python3.13

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    vim \
    s3cmd \
    p7zip-full \
    && apt-get autoremove -yqq --purge \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*


USER airflow

COPY requirements/base.txt requirements.txt
RUN pip install --no-cache-dir --requirement requirements.txt

COPY --chown=airflow:root . ./

COPY --chmod=755 custom-dev-entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint.sh"]
