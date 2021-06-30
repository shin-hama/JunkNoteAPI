FROM python:3.9-slim as builder

WORKDIR /usr/src/app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export --dev -f requirements.txt > requirements.txt


FROM python:3.9-slim as dev

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/requirements.txt .

RUN apt-get update && \
    apt-get install -y curl git docker.io

RUN pip install -r requirements.txt

COPY . .

CMD alembic upgrade head && \
    uvicorn --host=0.0.0.0 app.main:app --reload
