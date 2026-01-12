"""Tests for core configuration."""

from src.core.config import Settings


def test_settings_defaults() -> None:
    """Test that settings have sensible defaults."""
    settings = Settings()
    assert settings.environment in ["development", "staging", "production"]
    assert settings.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    assert settings.api_port > 0
    assert settings.api_host is not None


def test_is_development() -> None:
    """Test development environment detection."""
    settings = Settings(environment="development")
    assert settings.is_development is True
    assert settings.is_production is False


def test_is_production() -> None:
    """Test production environment detection."""
    settings = Settings(environment="production")
    assert settings.is_production is True
    assert settings.is_development is False
