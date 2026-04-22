FROM python:3.12-alpine

WORKDIR /app

# Consolidate user creation, package install, and cleanup into one RUN
RUN adduser -D appuser && \
    apk add --no-cache curl=8.2.1-r0 bash=5.2.15-r0

# Copy Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/docs || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]