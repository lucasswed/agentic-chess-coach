"""Core configuration management using Pydantic settings."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Application environment",
    )

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )

    # LLM Provider
    openai_api_key: str | None = Field(
        default=None,
        description="OpenAI API key",
    )
    anthropic_api_key: str | None = Field(
        default=None,
        description="Anthropic API key",
    )

    # Chess Engine
    stockfish_path: str = Field(
        default="/usr/local/bin/stockfish",
        description="Path to Stockfish binary",
    )

    # API Configuration
    api_host: str = Field(
        default="0.0.0.0",
        description="API host address",
    )
    api_port: int = Field(
        default=8000,
        description="API port",
    )
    api_reload: bool = Field(
        default=True,
        description="Enable auto-reload in development",
    )

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins",
    )

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"


# Global settings instance
settings = Settings()
