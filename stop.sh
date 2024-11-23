#!/bin/sh
UID=$(id -u) GID=$(id -g) docker compose down -v
