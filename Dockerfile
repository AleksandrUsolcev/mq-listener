FROM python:3.11.1-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-dev

ARG SERVICE_NAME
COPY ./$SERVICE_NAME ./

CMD ["python", "main.py"]