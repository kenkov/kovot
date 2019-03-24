FROM python:3.7.1-alpine3.8

COPY . /kovot
RUN apk add --no-cache gcc musl-dev libffi-dev libressl-dev && \
    pip install /kovot/