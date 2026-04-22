FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies with version pinning and single RUN
RUN apk add --no-cache bash=5.2.15-r0 curl=8.2.1-r0 \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/api/requirements.txt

# Set working directory
WORKDIR /app

# Copy app files
COPY ./api /app

# Expose port
EXPOSE 8000

# Start API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]