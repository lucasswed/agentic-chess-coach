.PHONY: help install install-dev test lint format clean run docs

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run test suite"
	@echo "  make lint         - Run all linters"
	@echo "  make format       - Format code with black and isort"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo "  make run          - Start development server"
	@echo "  make type-check   - Run mypy type checking"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest --cov=src --cov-report=term-missing

test-verbose:
	pytest -v --cov=src --cov-report=term-missing --cov-report=html

lint:
	ruff check src tests
	black --check src tests
	isort --check-only src tests
	mypy src

format:
	black src tests
	isort src tests
	ruff check --fix src tests

type-check:
	mypy src

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

run-prod:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000
