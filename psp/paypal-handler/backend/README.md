# Telecom Services Web Store Backend

## Project Setup

Install `uv`:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies:

```sh
uv sync
```

## Run locally

> These steps are temporary before introducing Docker Compose.

Run database:

```sh
docker run -d \
  --name my_postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=dbname \
  -p 5432:5432 \
  postgres
```

Run FastAPI app:

```sh
uv run fastapi dev --port 8022
```
