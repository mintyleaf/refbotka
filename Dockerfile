FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

ENV UV_CACHE_DIR=/root/.cache/uv
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/
COPY src /app/src

RUN --mount=type=cache,target=/root/.cache/uv \
	uv pip install --system .


FROM python:3.12-slim

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/refbotka /usr/local/bin/refbotka

CMD ["refbotka"]
