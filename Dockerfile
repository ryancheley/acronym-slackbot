# Multi-stage Dockerfile for Django application
# Stage 1: Builder - compile dependencies
FROM python:3.13-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install uv for fast package installation
RUN pip install --upgrade pip uv

# Copy minimal files needed for installation
COPY pyproject.toml README.md /tmp/
# Create minimal package structure for installation
RUN mkdir -p /tmp/acronyms /tmp/api /tmp/core && \
    touch /tmp/acronyms/__init__.py /tmp/api/__init__.py /tmp/core/__init__.py

# Install dependencies from pyproject.toml (with dev dependencies for DEBUG mode)
WORKDIR /tmp
RUN uv pip install --no-cache-dir ".[dev]"

# Stage 2: Runtime - minimal production image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=core.settings

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash django && \
    mkdir -p /app /app/staticfiles /app/static && \
    chown -R django:django /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=django:django . /app/

# Collect static files
USER django
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
