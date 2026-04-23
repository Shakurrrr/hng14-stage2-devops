import redis
import time
import os
import signal

running = True


def handle_signal(sig, frame):
    global running
    running = False


signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)


def get_redis_connection():
    while True:
        try:
            client = redis.Redis(
                host=os.getenv("REDIS_HOST", "redis"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                password=os.getenv("REDIS_PASSWORD")
            )
            client.ping()
            print("Connected to Redis")
            return client
        except Exception as e:
            print(f"Redis not ready: {e} — retrying in 2s")
            time.sleep(2)


def process_job(r, job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


r = get_redis_connection()

while running:
    job = r.brpop("jobs", timeout=5)
    if job:
        _, job_id = job
        process_job(r, job_id.decode())
