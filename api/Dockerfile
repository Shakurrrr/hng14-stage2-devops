# Base image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install curl and build dependencies
RUN apk add --no-cache curl build-base

# Copy requirements (if you want, you can keep a separate requirements.txt)
COPY requirements.txt .

# Install Python dependencies including dev tools
RUN pip install --no-cache-dir \
    fastapi==0.99.1 \
    uvicorn==0.23.1 \
    httpx==0.28.1 \
    redis==5.1.1 \
    pytest==8.3.5 \
    pytest-cov==7.1.0 \
    black==23.9.1 \
    flake8==6.1.0

# Copy app source
COPY . .

# Expose API port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]