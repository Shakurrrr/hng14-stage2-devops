# syntax=docker/dockerfile:1

# ─── Stage 1: builder ────────────────────────────────────────────────────────
FROM python:3.11-alpine AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir "pip==24.0" \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt
# ─── Stage 2: final ──────────────────────────────────────────────────────────
FROM python:3.11-alpine

WORKDIR /app

# Copy installed packages from builder — no pip or build tools in final image
COPY --from=builder /install /usr/local

# Copy application source
COPY worker.py .

# Create non-root user and hand over ownership
RUN adduser -D -u 1001 appuser \
    && chown -R appuser:appuser /app
    
USER appuser

# Worker has no HTTP port — health check verifies Redis connectivity
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import redis, os; r = redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT',6379)), password=os.getenv('REDIS_PASSWORD')); r.ping()" || exit 1

CMD ["python", "worker.py"]