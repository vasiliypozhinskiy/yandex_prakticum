FROM python:3.8-alpine

RUN apk update && apk add bash

WORKDIR /app
RUN addgroup -S app && adduser -S app app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add -U --no-cache build-base

COPY ./requirements.txt /app
RUN pip install -r /app/requirements.txt

WORKDIR /app