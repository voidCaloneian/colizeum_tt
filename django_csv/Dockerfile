FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src

WORKDIR /app

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000