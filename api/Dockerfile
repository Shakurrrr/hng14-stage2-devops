# Multi-stage build
FROM python:3.12-alpine AS build

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev curl

COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-alpine

WORKDIR /app

# Non-root user
RUN adduser -D appuser

# Install runtime dependencies
RUN apk add --no-cache curl

# Copy installed Python packages from build stage
COPY --from=build /install /usr/local

# Copy app code
COPY . .

USER appuser

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
  CMD curl -f http://localhost:8000/docs || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]