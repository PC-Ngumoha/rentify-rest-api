FROM python:3.11-slim-bookworm
LABEL maintainer="pcngumoha"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./create_user.sh /tmp/create_user.sh
COPY ./app /app

WORKDIR /app

EXPOSE 8000

ARG DEV=false

RUN <<EOF
  chmod +x /tmp/create_user.sh && /tmp/create_user.sh
  set -x
  python -m venv /env
  /env/bin/pip install --upgrade pip
  /env/bin/pip install -r /tmp/requirements.txt
  if [ $DEV = "true" ]; then
    /env/bin/pip install -r /tmp/requirements.dev.txt
  fi
  rm -rf /tmp
EOF

ENV PATH="/env/bin/:$PATH"

USER django-user