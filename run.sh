#!/bin/sh
# Build FastAPI hot-reloading image
docker build -t fastapi-hot-reload \
  --build-arg UID=$(id -u) \
  --build-arg GID=$(id -g) \
  devops/fastapi-hot-reload

mkdir -p telecom/frontend/dist psp/core/frontend/dist psp/crypto-handler/frontend/dist bank/unicredit/frontend/dist bank/erste/frontend/dist

# Run all containers
UID=$(id -u) GID=$(id -g) docker compose build
UID=$(id -u) GID=$(id -g) docker compose up -d

# Update environment variables
uv --directory devops/update-env run main.py

# Rerun backends to apply new environment variables
touch telecom/backend/app/main.py
touch psp/core/backend/app/main.py
touch psp/crypto-handler/backend/app/main.py
touch psp/card-handler/backend/app/main.py
touch psp/paypal-handler/backend/app/main.py
touch bank/unicredit/backend/app/main.py
touch bank/erste/backend/app/main.py

# Build frontends with updated environment variables
npm install --prefix telecom/frontend
npm run build --prefix telecom/frontend
npm install --prefix psp/core/frontend
npm run build --prefix psp/core/frontend
npm install --prefix psp/crypto-handler/frontend
npm run build --prefix psp/crypto-handler/frontend
npm install --prefix bank/erste/frontend
npm run build --prefix bank/erste/frontend
npm install --prefix bank/unicredit/frontend
npm run build --prefix bank/unicredit/frontend

# Print IP addresses of all running containers
uv --directory devops/get-ips run main.py
