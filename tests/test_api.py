"""Tests for API main module."""

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_check() -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_docs_available() -> None:
    """Test that API documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_available() -> None:
    """Test that ReDoc documentation is available."""
    response = client.get("/redoc")
    assert response.status_code == 200
