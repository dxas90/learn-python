# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12

# Builder stage - install dependencies with build tools
FROM python:${PYTHON_VERSION}-alpine3.20 AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev

# Copy requirements and install to a virtual environment
COPY requirements.txt ./
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Production stage - minimal Alpine image
FROM python:${PYTHON_VERSION}-alpine3.20 AS production

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Use the virtual environment from builder
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install runtime dependencies only
RUN apk add --no-cache \
    ca-certificates \
    tzdata curl

# Create a non-privileged user
RUN addgroup -g 1001 appuser && \
    adduser -D -u 1001 -G appuser appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=appuser:appuser . .

# Ensure tmp directories exist
RUN mkdir -p /tmp /var/tmp && chmod 1777 /tmp /var/tmp

# Switch to non-privileged user
USER appuser

# Ensure Python uses tmp for temp files
ENV TMPDIR=/tmp

# Expose the port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl http://127.0.0.1:8000/healthz || exit 1

# Run the application
CMD ["gunicorn", "app:app", "-c", "gunicorn_config.py"]
