from fastapi.testclient import TestClient
from api.app_main import app, r

client = TestClient(app)

def test_create_job_endpoint(monkeypatch):
    class DummyRedis:
        def lpush(self, *args, **kwargs): return 1
        def hset(self, *args, **kwargs): return 1

    monkeypatch.setattr("api.app_main.r", DummyRedis())
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_job_status_endpoint(monkeypatch):
    class DummyRedis:
        def hget(self, key, field): return b"completed"

    monkeypatch.setattr("api.app_main.r", DummyRedis())
    response = client.get("/jobs/123/status")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
