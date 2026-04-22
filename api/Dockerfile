# Stage 1: Build dependencies
FROM python:3.12.13-alpine AS builder
WORKDIR /app

# Install pinned build dependencies
RUN apk add --no-cache \
    gcc=13.2.1_git20230306-r0 \
    g++=13.2.1_git20230306-r0 \
    musl-dev=1.2.4-r3 \
    libffi-dev=3.4.4-r3 \
    make=4.4-r1 \
    bash=5.2.15-r2 \
    curl=8.2.1-r2

# Copy requirements
COPY requirements.txt ./

# Install Python dependencies including dev tools
RUN pip install --user --no-cache-dir \
    fastapi==0.99.1 \
    uvicorn==0.23.1 \
    httpx==0.28.1 \
    redis==5.1.1 \
    pytest==8.3.5 \
    pytest-cov==7.1.0 \
    black==23.9.1 \
    flake8==6.1.0

# Copy app source
COPY api/ ./api

# Stage 2: Final image
FROM python:3.12.13-alpine
WORKDIR /app

# Create non-root user
RUN adduser -D myuser
USER myuser

# Copy installed Python packages from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/api ./api

# Ensure pip-installed binaries are in PATH
ENV PATH=/root/.local/bin:$PATH

# Expose API port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "api.app_main:app", "--host", "0.0.0.0", "--port", "8000"]