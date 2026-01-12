# Agentic Chess Coach

An intelligent chess coaching system powered by LangGraph and FastAPI that provides personalized chess instruction through agentic AI workflows.

## 🎯 Project Overview

This is a **senior-level engineering artifact** designed to showcase:
- **Agentic AI workflows** using LangGraph for multi-step reasoning
- **Production-ready API design** with FastAPI
- **Chess engine integration** via Stockfish and python-chess
- **Clean architecture** with proper separation of concerns
- **Professional development practices** including CI/CD, testing, and type safety

## 🏗️ Architecture

```
src/
├── api/                 # FastAPI application layer
├── agents/              # LangGraph agent definitions
├── chess/               # Chess engine and game logic
├── models/              # Pydantic models and schemas
└── core/                # Shared utilities and configuration
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or 3.12
- Stockfish chess engine installed
- OpenAI or Anthropic API key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd agentic-chess-coach
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Install pre-commit hooks:
```bash
pre-commit install
```

### Running the Application

```bash
uvicorn src.api.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🧪 Testing

Run the full test suite:
```bash
pytest
```

Run with coverage report:
```bash
pytest --cov=src --cov-report=html
```

## 🔍 Code Quality

This project enforces strict code quality standards:

- **Formatting**: Black (line length: 100)
- **Linting**: Ruff
- **Type checking**: Mypy (strict mode)
- **Import sorting**: isort

Run all checks:
```bash
# Format code
black src tests

# Sort imports
isort src tests

# Lint
ruff check src tests

# Type check
mypy src
```

Or use pre-commit to run all checks:
```bash
pre-commit run --all-files
```

## 📋 Development Roadmap

- [x] **Epic 1**: Project foundations (Week 1)
- [ ] **Epic 2**: Chess engine integration (Week 2)
- [ ] **Epic 3**: LangGraph agent implementation (Week 3)
- [ ] **Epic 4**: FastAPI endpoints (Week 4)
- [ ] **Epic 5**: Testing and quality (Week 5)
- [ ] **Epic 6**: Documentation and deployment (Week 6)

## 🔑 Environment Variables

See `.env.example` for required configuration:

- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: LLM provider credentials
- `STOCKFISH_PATH`: Path to Stockfish binary
- `LOG_LEVEL`: Application logging level
- `ENVIRONMENT`: Development/production environment

## 📚 Key Technologies

- **FastAPI**: Modern async web framework
- **LangGraph**: Agentic workflow orchestration
- **LangChain**: LLM integration abstractions
- **python-chess**: Chess game logic and PGN parsing
- **Stockfish**: Chess engine for analysis
- **Pydantic**: Data validation and settings management
- **pytest**: Testing framework with async support

## 🤝 Contributing

This is a portfolio project, but contributions are welcome:

1. Ensure all tests pass
2. Maintain >90% code coverage
3. Follow existing code style
4. Add tests for new features
5. Update documentation

## 📄 License

MIT License - See LICENSE file for details

## 📧 Contact

Your Name - your.email@example.com

---

**Project Status**: Epic 1 Complete ✅ | Next: Epic 2 - Chess Engine Integration
