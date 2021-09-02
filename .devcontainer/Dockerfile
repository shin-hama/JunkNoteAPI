FROM python:3.9-slim as dev

ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

RUN apt-get update && \
    apt-get install -y curl git docker.io vim

COPY . .

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - && \
    export PATH="$HOME/.local/bin:$PATH" && \
    poetry config virtualenvs.create false --local && \
    poetry install
