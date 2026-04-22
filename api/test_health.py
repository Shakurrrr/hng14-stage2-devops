from fastapi.testclient import TestClient
from main import app  # import your FastAPI app

# Use FastAPI's TestClient
client = TestClient(app)


# Test /docs endpoint
def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200


# Test creating a job (mock Redis)
def test_create_job(monkeypatch):
    class DummyRedis:
        def rpush(self, *args, **kwargs):
            return 1

    monkeypatch.setattr("main.redis_conn", DummyRedis())
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


# Test job status endpoint (mock Redis)
def test_job_status(monkeypatch):
    class DummyRedis:
        def get(self, key):
            return b"completed"

    monkeypatch.setattr("main.redis_conn", DummyRedis())
    response = client.get("/jobs/123/status")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
