FROM python:3.12-slim

WORKDIR /app

# Add non-root user
RUN useradd -m appuser

# Install curl (for healthcheck) safely with version pinning
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl=8.3.1-1+deb13u1 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
  CMD curl -f http://localhost:8000/docs || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]