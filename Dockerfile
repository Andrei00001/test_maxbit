FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache postgresql-client

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-cache


COPY common ./common
COPY database ./database
COPY handlers ./handlers
COPY migrations ./migrations
COPY repositories ./repositories
COPY services ./services
COPY alembic.ini main.py ./

CMD alembic upgrade head && python main.py
