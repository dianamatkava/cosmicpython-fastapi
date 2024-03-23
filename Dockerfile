ARG PYTHON_VERSION=3.11.6
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY testing-src .


RUN pip install poetry
RUN poetry install --with pylint --no-root

RUN pylint ./* --output-format=codeclimate --exit-zero > gl-report.json
