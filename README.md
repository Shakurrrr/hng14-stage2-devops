# hng14-stage2-devops
# Job Processor — Microservices Application

A containerised job processing system consisting of four services: a Node.js frontend, a Python/FastAPI backend, a Python worker, and Redis as the message queue.

---

## Prerequisites

Make sure the following are installed on your machine before proceeding:

- [Docker](https://docs.docker.com/get-docker/) v24+
- [Docker Compose](https://docs.docker.com/compose/install/) v2.20+
- Git

Verify your installations:
```bash
docker --version
docker compose version
git --version
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hng14-stage2-devops.git
cd hng14-stage2-devops
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
REDIS_PASSWORD=your_strong_password_here
REDIS_PORT=6379
APP_ENV=production
FRONTEND_PORT=3000
```

> **Never commit the `.env` file.** It is listed in `.gitignore` and must stay local.

### 3. Build and start the stack

```bash
docker compose up --build -d
```

This will build all three service images and start all four containers (frontend, api, worker, redis).

### 4. Verify all services are healthy

```bash
docker compose ps
```

Expected output — all services should show `healthy`:

```
NAME                STATUS
app-frontend-1      running (healthy)
app-api-1           running (healthy)
app-worker-1        running (healthy)
app-redis-1         running (healthy)
```

It may take 30–60 seconds for all health checks to pass on first boot.

---

## Using the Application

Open your browser and go to:

```
http://localhost:3000
```

You will see the **Job Processor Dashboard**. Click **Submit New Job** to create a job. The job will appear in the list below with a status of `queued`, then transition to `completed` within a few seconds once the worker picks it up.

---

## Verifying the full flow via curl

```bash
# Submit a job
curl -s -X POST http://localhost:3000/submit

# Check job status (replace JOB_ID with the id returned above)
curl -s http://localhost:3000/status/JOB_ID
```

A successful response looks like:
```json
{ "job_id": "abc123...", "status": "completed" }
```

---

## Stopping the stack

```bash
docker compose down
```

To also remove the Redis data volume:

```bash
docker compose down --volumes
```

---

## Running Tests Locally

```bash
cd api
pip install fastapi uvicorn redis fakeredis pytest pytest-cov httpx
pytest tests/ -v --cov=. --cov-report=term-missing
```

---

## Project Structure

```
.
├── api/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
│       ├── __init__.py
│       └── test_main.py
├── worker/
│   ├── Dockerfile
│   ├── worker.py
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   ├── app.js
│   ├── package.json
│   └── views/
│       └── index.html
├── docker-compose.yml
├── .env.example
├── .gitignore
├── FIXES.md
└── README.md
```

---

## CI/CD Pipeline

The GitHub Actions pipeline runs automatically on every push and consists of six stages that must all pass in order:

| Stage | What it does |
|-------|-------------|
| lint | Checks Python (flake8), JavaScript (eslint), and Dockerfiles (hadolint) |
| test | Runs pytest with Redis mocked, uploads coverage report as artifact |
| build | Builds all 3 images, tags with git SHA and latest, pushes to local registry |
| security | Scans all images with Trivy, fails on any CRITICAL vulnerability |
| integration | Brings the full stack up, submits a job, asserts it completes, tears down |
| deploy | Rolling update to production server (runs on pushes to main only) |

---

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_PASSWORD` | Password for Redis authentication | required |
| `REDIS_PORT` | Redis port | `6379` |
| `APP_ENV` | Application environment | `production` |
| `FRONTEND_PORT` | Host port for the frontend | `3000` |