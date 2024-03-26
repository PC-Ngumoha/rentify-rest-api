# Stage 1: Dependencies installation
FROM python:3.11-slim-bookworm AS base
LABEL maintainer="pcngumoha"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN set -x && \
  apt-get update && \
  apt-get install -y --no-install-recommends \
  libpq-dev \
  gcc \
  python3-dev && \
  rm -rf /var/lib/apt/lists/* && \
  python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
  /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt && \
  apt-get purge -y --auto-remove gcc libpq-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
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
