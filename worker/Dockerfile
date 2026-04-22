# Base image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies in a single RUN
RUN pip install --no-cache-dir -r requirements.txt

# Copy worker source
COPY . .

# Start the worker
CMD ["python", "worker.py"]