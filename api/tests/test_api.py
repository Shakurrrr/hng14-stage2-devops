from fastapi.testclient import TestClient
from api.app_main import app

client = TestClient(app)


class DummyRedis:
    def __init__(self):
        self.data = {}
        self.lists = {}

    def lpush(self, name, value):
        self.lists.setdefault(name, []).insert(0, value)
        return 1

    def rpush(self, name, value):
        self.lists.setdefault(name, []).append(value)
        return 1

    def hset(self, name, key, value):
        self.data.setdefault(name, {})[key] = value
        return 1

    def hget(self, name, key):
        val = self.data.get(name, {}).get(key, None)
        return val if isinstance(val, bytes) else (val.encode() if val else None)

    def lrange(self, name, start, end):
        lst = self.lists.get(name, [])
        if end == -1:
            end = len(lst)
        return lst[start:end]


def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200


def test_create_job_endpoint(monkeypatch):
    monkeypatch.setattr("api.app_main.r", DummyRedis())
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_job_status_endpoint(monkeypatch):
    dummy_redis = DummyRedis()
    monkeypatch.setattr("api.app_main.r", dummy_redis)

    # Create a job via endpoint (adds job_id to "job" list automatically)
    response_create = client.post("/jobs")
    job_id = response_create.json()["job_id"]

    # Set the job status
    dummy_redis.hset(f"job:{job_id}", "status", b"completed")

    # Now status endpoint should succeed
    response_status = client.get(f"/jobs/{job_id}/status")
    assert response_status.status_code == 200
    assert response_status.json()["status"] == "completed"
