# test_health.py
from fastapi.testclient import TestClient
from app_main import app, r  # import FastAPI app and DummyRedis

client = TestClient(app)


# Test root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Test creating a job
def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


# Test getting a job status
def test_job_status():
    # First create a job
    create_resp = client.post("/jobs")
    job_id = create_resp.json()["job_id"]

    # Set status manually in DummyRedis
    r.hset(f"job:{job_id}", "status", "completed")

    # Now fetch the job
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


# Test /docs endpoint
def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200