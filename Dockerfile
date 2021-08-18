FROM python:3.9-slim as builder

ARG WORKDIR
WORKDIR ${WORKDIR}

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry export -f requirements.txt > requirements.txt

FROM python:3.9-slim as server

ENV PYTHONUNBUFFERED=1

ARG WORKDIR
WORKDIR ${WORKDIR}

COPY --from=builder ${WORKDIR}/requirements.txt .

RUN pip install -r requirements.txt

COPY .env alembic.ini ./
COPY app/ ./app/

CMD alembic upgrade head && \
    uvicorn --host 0.0.0.0 --port ${APP_PORT} app.main:app --reload
