# Docker image for EMS Application using multistage builds
# This helps to keep the final image small and efficient by only including necessary runtime dependencies.

# Builder Stage
FROM python:3.11-slim AS builder

WORKDIR /install

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip uv

COPY requirements.txt .

RUN uv pip install \
    --system \
    --no-cache-dir \
    --prefix=/install/deps \
    -r requirements.txt


# Runtime Stage
FROM python:3.11-slim

LABEL description="Production-ready EMS application (FastAPI + Streamlit + PostgreSQL)"

RUN useradd -m appuser

WORKDIR /ems

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /install/deps /usr/local

COPY . .

ENV PYTHONPATH=/ems \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN chown -R appuser:appuser /ems

USER appuser
