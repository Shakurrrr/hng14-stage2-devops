FROM python:3.12-alpine

WORKDIR /app

# Add non-root user
RUN adduser -D appuser

# Install dependencies in a single RUN and pin versions
# You can check current versions using `apk info -v` or leave latest if not critical
RUN apk add --no-cache curl=8.2.1-r0 bash=5.2.15-r0

# Copy Python requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

USER appuser

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/docs || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]