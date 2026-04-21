FROM python:3.12-slim

WORKDIR /app

# Non-root user
RUN useradd -m appuser

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

EXPOSE 8000

# Healthcheck (optional but recommended)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD pgrep -f worker.py || exit 1

CMD ["python", "worker.py"]