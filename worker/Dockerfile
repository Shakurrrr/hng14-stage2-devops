FROM python:3.12-alpine

WORKDIR /app

# Add non-root user
RUN adduser -D appuser

# Install dependencies (combined RUN to satisfy DL3059)
# hadolint ignore=DL3018
RUN apk add --no-cache curl && \
    rm -rf /var/cache/apk/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
  CMD curl -f http://localhost:8000/docs || exit 1

CMD ["python", "worker.py"]