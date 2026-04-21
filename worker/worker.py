import redis
import time
import os
import signal
import sys

# CONFIG
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# GRACEFUL SHUTDOWN
running = True

def shutdown(signum, frame):
    global running
    print("Shutting down worker gracefully...")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# CORE PROCESSING LOGIC
def process_job(job_id: str):
    print(f"[WORKER] Processing job {job_id}")
    time.sleep(2)  # simulate work

    r.hset(f"job:{job_id}", "status", "completed")
    print(f"[WORKER] Done: {job_id}")

# MAIN LOOP
print(f"[WORKER] Starting worker... connected to {REDIS_HOST}:{REDIS_PORT}")

while running:
    try:
        job = r.brpop("job", timeout=5)

        if job:
            _, job_id = job
            process_job(job_id.decode())

    except redis.exceptions.ConnectionError as e:
        print(f"[ERROR] Redis connection failed: {e}")
        time.sleep(3)

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        time.sleep(1)

print("[WORKER] stopped cleanly")