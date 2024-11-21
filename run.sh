#!/bin/sh
docker build -t fastapi-hot-reload \
  --build-arg UID=$(id -u) \
  --build-arg GID=$(id -g) \
  devops/fastapi-hot-reload

UID=$(id -u) GID=$(id -g) docker compose build
UID=$(id -u) GID=$(id -g) docker compose up -d

uv --directory devops/get-ips run main.py
