#!/bin/sh
# Build FastAPI hot-reloading image
docker build -t fastapi-hot-reload \
  --build-arg UID=$(id -u) \
  --build-arg GID=$(id -g) \
  devops/fastapi-hot-reload

# Run all containers
UID=$(id -u) GID=$(id -g) docker compose build
UID=$(id -u) GID=$(id -g) docker compose up -d

# Update environment variables
uv --directory devops/update-env run main.py

# Rerun backends to apply new environment variables
touch telecom/backend/app/main.py
touch psp/core/backend/app/main.py
touch psp/crypto-handler/backend/app/main.py

# Build frontends with updated environment variables
npm install --prefix telecom/frontend
npm run build --prefix telecom/frontend
npm install --prefix psp/core/frontend
npm run build --prefix psp/core/frontend

# Print IP addresses of all running containers
uv --directory devops/get-ips run main.py
