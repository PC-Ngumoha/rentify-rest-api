FROM python:3.9.19-alpine
LABEL maintainer="pcngumoha"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app

EXPOSE 8000

ARG DEV=false

RUN <<EOF
  python -m venv /env
  /env/bin/pip install --upgrade pip
  /env/bin/pip install -r /tmp/requirements.txt
  if [ $DEV = "true" ]; then
    /env/bin/pip install -r /tmp/requirements.dev.txt
  fi
  rm -rf /tmp
  adduser --no-create-home --disabled-password dev-user
EOF

ENV PATH="/env/bin/:$PATH"

USER dev-user