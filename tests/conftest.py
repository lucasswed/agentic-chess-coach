"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock environment variables for testing."""
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
