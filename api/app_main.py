from fastapi import FastAPI
import uuid


app = FastAPI()


class DummyRedis:
    def __init__(self):
        self.storage = {}
        self.lists = {}

    def lpush(self, key, value):
        self.lists.setdefault(key, []).insert(0, value)
        return 1

    def hset(self, key, field, value):
        # Store value as bytes to mimic real Redis
        self.storage.setdefault(key, {})[field] = str(value).encode()
        return 1

    def hget(self, key, field):
        return self.storage.get(key, {}).get(field, None)


# Initialize dummy Redis
r = DummyRedis()


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    # Decode bytes to string
    return {"job_id": job_id, "status": status.decode()}
