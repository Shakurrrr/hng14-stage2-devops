from fastapi.testclient import TestClient

client = TestClient(app)


def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200


def test_create_job_endpoint(monkeypatch):
    class DummyRedis:
        def lpush(self, key, value):
            return 1

        def hset(self, key, field, value):
            return 1

    # Patch the correct object 'r' in app_main
    monkeypatch.setattr("api.app_main.r", DummyRedis())

    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_job_status_endpoint(monkeypatch):
    class DummyRedis:
        def hget(self, key, field):
            return b"completed"

    # Patch the correct object 'r' in app_main
    monkeypatch.setattr("api.app_main.r", DummyRedis())

    response = client.get("/jobs/123")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
