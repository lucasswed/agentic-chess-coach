#!/bin/bash
# Setup script for Agentic Chess Coach
# Run this on your local machine to complete Epic 1 setup

set -e  # Exit on error

echo "🚀 Setting up Agentic Chess Coach - Epic 1"
echo "==========================================="

# Check Python version
echo "📋 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_MAJOR=3
REQUIRED_MINOR=11

CURRENT_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
CURRENT_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$CURRENT_MAJOR" -ne "$REQUIRED_MAJOR" ] || [ "$CURRENT_MINOR" -lt "$REQUIRED_MINOR" ]; then
    echo "❌ Python 3.11+ required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "⚠️  Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📥 Installing dependencies..."
pip install -e ".[dev]"

# Set up pre-commit hooks
echo "🎣 Installing pre-commit hooks..."
pre-commit install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys"
else
    echo "⚠️  .env file already exists"
fi

# Run initial tests
echo "🧪 Running initial tests..."
pytest

# Run linting
echo "🔍 Running linters..."
echo "  - ruff..."
ruff check src tests || echo "⚠️  Ruff found issues (run 'make format' to fix)"

echo "  - black..."
black --check src tests || echo "⚠️  Black found formatting issues (run 'make format' to fix)"

echo "  - isort..."
isort --check-only src tests || echo "⚠️  isort found import issues (run 'make format' to fix)"

echo "  - mypy..."
mypy src || echo "⚠️  Mypy found type issues (acceptable in Epic 1)"

echo ""
echo "✅ Epic 1 Setup Complete!"
echo "======================="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Run 'make run' to start the development server"
echo "  3. Visit http://localhost:8000/docs for API documentation"
echo "  4. Run 'make test' to verify everything works"
echo ""
echo "Available commands (see Makefile):"
echo "  make install-dev  - Reinstall dependencies"
echo "  make test         - Run tests"
echo "  make lint         - Run linters"
echo "  make format       - Auto-format code"
echo "  make run          - Start dev server"
echo ""
