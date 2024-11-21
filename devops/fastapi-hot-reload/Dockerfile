FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG GID=1000
ARG UID=1000

RUN groupadd -g "${GID}" runner && \
    useradd -m -u "${UID}" -g runner runner
USER runner
