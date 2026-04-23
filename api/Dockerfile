# ------------------- Stage 1: Build -------------------
FROM python:3.12-alpine AS builder
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc=13.2.1_git20230306-r0 \
    g++=13.2.1_git20230306-r0 \
    musl-dev=1.2.4-r3 \
    libffi-dev=3.4.4-r3 \
    make=4.4-r1 \
    bash=5.2.15-r2 \
    curl=8.2.1-r2

# Copy requirements and install into user site
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy API source
COPY . ./api

# ------------------- Stage 2: Final -------------------
FROM python:3.12-alpine
WORKDIR /app

# Create non-root user
RUN adduser -D myuser
USER myuser

# Copy Python packages and app from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/api ./api

# Add user site to PATH
ENV PATH=/root/.local/bin:$PATH

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "api.app_main:app", "--host", "0.0.0.0", "--port", "8000"]