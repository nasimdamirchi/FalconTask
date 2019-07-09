#!/usr/bin/bash -x
FROM python:3.7.3


COPY requirements.txt requirements.txt

RUN pip install -U pip
RUN pip install -r requirements.txt
COPY . .
WORKDIR geolocation
CMD gunicorn -b 0.0.0.0:8000 api:app