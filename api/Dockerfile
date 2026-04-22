# Base image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install curl and build dependencies with pinned versions
# curl=8.2.1-r2 and build-base is a meta package, we can pin each underlying tool
RUN apk add --no-cache \
    curl=8.2.1-r2 \
    gcc=13.2.1_git20230306-r0 \
    g++=13.2.1_git20230306-r0 \
    musl-dev=1.2.4-r3 \
    libffi-dev=3.4.4-r3 \
    make=4.4-r1 \
    bash=5.2.15-r2

# Copy requirements
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