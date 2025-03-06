# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm

COPY requirements.txt requirements.txt
COPY main.py main.py
COPY cogs cogs
COPY entrypoint.sh entrypoint.sh

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
