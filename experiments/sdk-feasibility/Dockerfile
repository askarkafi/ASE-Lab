FROM public.ecr.aws/docker/library/python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.lock /tmp/requirements.lock

RUN python -m pip install --no-cache-dir --no-deps -r /tmp/requirements.lock \
    && python -m pip check \
    && python -m pip list --format=freeze | sort > /tmp/installed.txt \
    && sort /tmp/requirements.lock > /tmp/locked.txt \
    && diff -u /tmp/locked.txt /tmp/installed.txt

RUN useradd --uid 10001 --create-home agent
WORKDIR /work
USER 10001:10001
