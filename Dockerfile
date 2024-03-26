# Stage 1: Dependencies installation
FROM python:3.11-slim-bookworm AS base
LABEL maintainer="pcngumoha"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

USER root

RUN set -x && \
  apt update && \
  apt install -y --no-install-recommends \
  libpq-dev \
  libpq5 \
  gcc \
  python3.11-dev && \
  python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
  /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt && \
  apt purge -y --auto-remove gcc libpq-dev && \
  rm -rf /tmp



# Stage 2: Final setup
FROM base
LABEL maintainer="pcngumoha"

ENV PYTHONUNBUFFERED 1

COPY ./app /app

WORKDIR /app

EXPOSE 8000

ENV PATH="/py/bin:$PATH"

RUN adduser --disabled-password --no-create-home django-user

USER django-user
