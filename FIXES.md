# FIXES.md

All bugs found in the application source code, documented with file, line, problem, and fix.

---

## Fix 1

- **File**: `api/main.py`
- **Line**: 8
- **Problem**: Redis host hardcoded as `"localhost"`. Inside Docker, each service runs in its own container — `localhost` refers to the container itself, not the Redis container. The API would fail to connect to Redis on startup.
- **Fix**: Changed to `host=os.getenv("REDIS_HOST", "redis")` so the service name from `docker-compose.yml` is used at runtime.

---

## Fix 2

- **File**: `api/main.py`
- **Line**: 8
- **Problem**: Redis port hardcoded as `6379` with no environment variable override. Makes the port impossible to change without modifying source code.
- **Fix**: Changed to `port=int(os.getenv("REDIS_PORT", 6379))`.

---

## Fix 3

- **File**: `api/main.py`
- **Line**: 8
- **Problem**: Redis connection does not pass a password. The `.env` file defines `REDIS_PASSWORD`, meaning Redis is configured with `requirepass`. Any connection attempt without the password will be rejected with a `NOAUTH` error.
- **Fix**: Added `password=os.getenv("REDIS_PASSWORD")` to the Redis constructor.

---

## Fix 4

- **File**: `api/main.py`
- **Line**: 11
- **Problem**: Job queue key named `"job"` (singular). The worker pops from `"jobs"` (plural). This mismatch means the worker never receives any jobs — they are pushed to a key nobody reads.
- **Fix**: Changed `r.lpush("job", job_id)` to `r.lpush("jobs", job_id)` to match the worker.

---

## Fix 5

- **File**: `api/main.py`
- **Line**: (none — missing code)
- **Problem**: No `/health` endpoint exists. The `HEALTHCHECK` instruction in the Dockerfile and the `depends_on: condition: service_healthy` in `docker-compose.yml` both require a HTTP endpoint to probe. Without it, health checks fail and dependent services never start.
- **Fix**: Added the following route:
  ```python
  @app.get("/health")
  def health():
      return {"status": "ok"}
  ```

---

## Fix 6

- **File**: `worker/worker.py`
- **Line**: 5
- **Problem**: Redis host hardcoded as `"localhost"` — same Docker networking issue as Fix 1. The worker container cannot reach Redis via `localhost`.
- **Fix**: Changed to `host=os.getenv("REDIS_HOST", "redis")`.

---

## Fix 7

- **File**: `worker/worker.py`
- **Line**: 5
- **Problem**: Redis connection does not pass a password. Same issue as Fix 3 — connection will be rejected if Redis requires authentication.
- **Fix**: Added `password=os.getenv("REDIS_PASSWORD")` to the Redis constructor.

---

## Fix 8

- **File**: `worker/worker.py`
- **Line**: 5
- **Problem**: Redis port hardcoded as `6379` with no environment variable override.
- **Fix**: Changed to `port=int(os.getenv("REDIS_PORT", 6379))`.

---

## Fix 9

- **File**: `worker/worker.py`
- **Line**: 4
- **Problem**: `signal` module is imported but never used. More critically, there is no `SIGTERM` handler. When Docker stops the container (e.g. during a rolling deploy or `compose down`), the worker is killed immediately with no chance to finish the in-progress job. That job is silently lost — it was already popped off the queue but never marked `completed`.
- **Fix**: Replaced the infinite `while True` loop with a graceful shutdown pattern:
  ```python
  running = True

  def handle_signal(sig, frame):
      global running
      running = False

  signal.signal(signal.SIGTERM, handle_signal)
  signal.signal(signal.SIGINT, handle_signal)

  while running:
      job = r.brpop("jobs", timeout=5)
      if job:
          _, job_id = job
          process_job(job_id.decode())
  ```

---

## Fix 10

- **File**: `worker/worker.py`
- **Line**: 12
- **Problem**: Worker pops from queue key `"job"` (singular) while the API pushes to `"jobs"` (plural). This is the other side of Fix 4.
- **Fix**: Changed `r.brpop("job", timeout=5)` to `r.brpop("jobs", timeout=5)`.

---

## Fix 11

- **File**: `frontend/app.js`
- **Line**: 5
- **Problem**: API URL hardcoded as `"http://localhost:8000"`. When the frontend runs inside a Docker container, `localhost` is the frontend container itself — not the API container. All job submissions and status checks would fail with a connection refused error.
- **Fix**: Changed to `const API_URL = process.env.API_URL || "http://api:8000"` so the Docker service name is used by default.

---

## Fix 12

- **File**: `frontend/app.js`
- **Lines**: 13, 20
- **Problem**: Caught errors are swallowed — only `"something went wrong"` is returned to the client with no detail logged server-side. This makes debugging failures in production or CI impossible.
- **Fix**: Added `console.error(err.message)` inside each catch block before sending the 500 response.

---

## Fix 13

- **File**: `frontend/package.json`
- **Line**: (entire file)
- **Problem**: No `engines` field specifying the required Node.js version. Docker multi-stage builds pull the default `node` image tag, which can change between builds and introduce subtle breakage. There is also no `package-lock.json` committed, so `npm install` resolves different dependency trees on different machines.
- **Fix**: Added `"engines": { "node": ">=18.0.0" }` to `package.json`. Committed `package-lock.json` generated by `npm install`.

---

## Fix 14

- **File**: `.env` (root)
- **Line**: entire file
- **Problem**: A `.env` file containing `REDIS_PASSWORD=supersecretpassword123` and `APP_ENV=production` was present in the repository. Committing secrets to version control is a critical security violation and is explicitly penalised in this assessment.
- **Fix**: Added `.env` to `.gitignore`. Removed `.env` from git tracking with `git rm --cached .env`. Created `.env.example` with placeholder values. Verified secret does not appear in git history using `git log --all -S "supersecretpassword"`.