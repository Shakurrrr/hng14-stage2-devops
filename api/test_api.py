from fastapi.testclient import TestClient
from api.app_main import app


client = TestClient(app)


def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200


def test_create_job_endpoint(monkeypatch):
    class DummyRedis:
        def rpush(self, *args, **kwargs):
            return 1

    # Patch the DummyRedis used in app_main
    monkeypatch.setattr("api.app_main.r", DummyRedis())
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_job_status_endpoint(monkeypatch):
    class DummyRedis:
        def get(self, key):
            return b"completed"

    monkeypatch.setattr("api.app_main.r", DummyRedis())
    response = client.get("/jobs/123/status")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
