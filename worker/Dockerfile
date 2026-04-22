FROM python:3.12-alpine

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies in a single RUN
RUN apk add --no-cache bash=5.2.15-r0 curl=8.2.1-r0 \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/worker/requirements.txt

# Set working directory
WORKDIR /app

# Copy app files
COPY ./worker /app

# Start Worker
CMD ["python", "worker.py"]