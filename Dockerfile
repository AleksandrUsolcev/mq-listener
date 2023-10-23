FROM python:3.11.1-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

COPY ./internal ./internal

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

ARG SERVICE_NAME
COPY ./$SERVICE_NAME ./

CMD ["python", "main.py"]
