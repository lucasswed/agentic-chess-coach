"""Logging configuration using loguru."""

import sys
from typing import Any

from loguru import logger

from .config import settings


def configure_logging() -> None:
    """Configure application logging with loguru."""
    # Remove default handler
    logger.remove()

    # Add custom handler with format based on environment
    if settings.is_development:
        # Development: colorful and detailed
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>",
            level=settings.log_level,
            colorize=True,
        )
    else:
        # Production: JSON structured logging
        logger.add(
            sys.stderr,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
            level=settings.log_level,
            serialize=True,
        )


def get_logger(name: str) -> Any:
    """Get a logger instance for a specific module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logger.bind(module=name)
