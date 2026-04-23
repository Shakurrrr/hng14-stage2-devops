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
COPY main.py .

# Create non-root user and hand over ownership
RUN adduser -D -u 1001 appuser \
    && chown -R appuser:appuser /app
    
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]