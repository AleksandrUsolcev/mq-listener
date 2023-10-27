FROM python:3.11.1-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

COPY ./internal ./internal

RUN pip install poetry

ARG SERVICE_NAME
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --with $SERVICE_NAME

COPY ./$SERVICE_NAME ./

CMD ["python", "main.py"]
