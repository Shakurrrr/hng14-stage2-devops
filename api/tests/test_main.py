import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main  # noqa: E402


@pytest.fixture
def mock_redis():
    with patch("main.r") as mock_r:
        yield mock_r


@pytest.fixture
def client(mock_redis):
    return TestClient(main.app)


# ── Test 1: POST /jobs creates a job and returns a job_id ────────────────────
def test_create_job_returns_job_id(client, mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) == 36  # UUID format


# ── Test 2: POST /jobs pushes to Redis queue and sets status ─────────────────
def test_create_job_writes_to_redis(client, mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")
    job_id = response.json()["job_id"]

    mock_redis.lpush.assert_called_once_with("jobs", job_id)
    mock_redis.hset.assert_called_once_with(f"job:{job_id}", "status", "queued")


# ── Test 3: GET /jobs/{id} returns status for existing job ───────────────────
def test_get_job_returns_status(client, mock_redis):
    mock_redis.hget.return_value = b"queued"

    response = client.get("/jobs/test-job-123")

    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "queued"


# ── Test 4: GET /jobs/{id} returns error for missing job ─────────────────────
def test_get_job_not_found(client, mock_redis):
    mock_redis.hget.return_value = None

    response = client.get("/jobs/nonexistent-job")

    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "not found"


# ── Test 5: GET /health returns ok ───────────────────────────────────────────
def test_health_check(client, mock_redis):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── Test 6: GET /jobs/{id} returns completed status ──────────────────────────
def test_get_job_completed_status(client, mock_redis):
    mock_redis.hget.return_value = b"completed"

    response = client.get("/jobs/done-job-456")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["job_id"] == "done-job-456"
