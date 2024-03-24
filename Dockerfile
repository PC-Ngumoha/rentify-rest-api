# Stage 1: Dependencies installation
FROM python:3.11-slim-bookworm AS deps
LABEL maintainer="pcngumoha"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN set -x && \
  python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  /py/bin/pip install -r /tmp/requirements.dev.txt && \
  rm -rf /tmp


# Stage 2: Final setup
FROM python:3.11-slim-bookworm
LABEL maintainer="pcngumoha"

ENV PYTHONUNBUFFERED 1

COPY --from=deps /py /py
COPY ./app /app

WORKDIR /app

EXPOSE 8000

ENV PATH="/py/bin:$PATH"

RUN adduser --disabled-password --no-create-home django-user

USER django-user
