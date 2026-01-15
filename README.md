# Agentic Chess Coach

An intelligent chess coaching system powered by **LangGraph** and **FastAPI** that provides personalized chess instruction through agentic AI workflows.

This project is designed as a **senior-level engineering artifact** showcasing:

* Agentic AI workflows for multi-step reasoning
* Production-ready API design with FastAPI
* Chess engine integration via Stockfish and python-chess
* Deterministic evaluation and move classification pipelines
* Clean architecture and professional development practices (CI/CD, testing, type safety)

---

## 🎯 Project Overview

The system provides **personalized chess instruction** by combining:

1. **Deterministic Post-Move Analysis**

   * Uses Stockfish to evaluate the impact of each move
   * Computes centipawn deltas and mate transitions
   * Fully mover-relative, deterministic, and frozen for stability

2. **Move Classification**

   * Classifies moves as **BEST, GOOD, INACCURACY, MISTAKE, BLUNDER**
   * Handles all edge cases for mate transitions
   * Delta-based thresholds for non-mate positions

3. **Agentic Workflow Layer**

   * Orchestrates pipelines for real-time analysis
   * Prepares for future AI explanations and lesson extraction

---

## 🏗️ Architecture

```
src/
├── pipelines/            # Deterministic evaluation and delta calculation
│   └── post_move_analysis.py
├── classification/       # Move quality classification (BEST, GOOD, etc.)
│   └── move_quality.py
├── api/                  # FastAPI application layer
│   └── main.py
├── agents/               # LangGraph agent definitions
├── chess/                # Chess game logic and utilities
├── models/               # Pydantic models and schemas
└── core/                 # Shared utilities and configuration
```

**Principles:**

* Separation of concerns: evaluation, classification, agent orchestration
* Deterministic evaluation frozen before adding AI reasoning
* Contracts for predictable API outputs
* Test-driven development for critical edge cases (mate transitions)

---

## 🚀 Quick Start

### Prerequisites

* Python 3.11 or 3.12
* Stockfish chess engine installed
* OpenAI or Anthropic API key

### Installation

```bash
git clone <your-repo-url>
cd agentic-chess-coach
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your API keys and configuration
pre-commit install
```

### Running the Application

```bash
uvicorn src.api.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

---

## 🧪 Testing

* Run full test suite:

```bash
pytest
```

* Run with coverage report:

```bash
pytest --cov=src --cov-report=html
```

* Test areas include:

  * Mate transitions (escaping mate, losing mate, entering mate, still winning/losing)
  * Centipawn delta thresholds
  * Move quality classification correctness

---

## 🔍 Code Quality

This project enforces strict code quality standards:

* **Formatting**: Black (line length: 100)
* **Linting**: Ruff
* **Type checking**: Mypy (strict mode)
* **Import sorting**: isort

Run all checks:

```bash
black src tests
isort src tests
ruff check src tests
mypy src
pre-commit run --all-files
```

---

## 📋 Development Roadmap

| Epic   | Status     | Description                                                            |
| ------ | ---------- | ---------------------------------------------------------------------- |
| Epic 1 | ✅ Complete | Project foundations, CI/CD, repo structure, type safety                |
| Epic 2 | ✅ Complete | Chess engine integration, deterministic pipelines, move classification |
| Epic 3 | ⬜          | LangGraph agent implementation                                         |
| Epic 4 | ⬜          | FastAPI endpoints and API contract freezing                            |
| Epic 5 | ⬜          | Lesson extraction, LLM explanations, multi-turn memory                 |
| Epic 6 | ⬜          | Documentation, testing improvements, deployment pipeline               |

---

## 🔑 Environment Variables

See `.env.example` for configuration:

* `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: LLM provider credentials
* `STOCKFISH_PATH`: Path to Stockfish binary
* `LOG_LEVEL`: Application logging level
* `ENVIRONMENT`: Development/production environment

---

## 📚 Key Technologies

* **FastAPI**: Modern async web framework
* **LangGraph**: Agentic workflow orchestration
* **LangChain**: LLM integration abstractions
* **python-chess**: Chess game logic and PGN parsing
* **Stockfish**: Chess engine for deterministic analysis
* **Pydantic**: Data validation and settings management
* **pytest**: Testing framework with async support

---

## 🤝 Contributing

This is a portfolio project, but contributions are welcome:

1. Ensure all tests pass
2. Maintain >90% code coverage
3. Follow existing code style
4. Add tests for new features
5. Update documentation

---

## 📄 License

MIT License - See LICENSE file for details

---

## 📧 Contact

Your Name - [your.email@example.com](mailto:your.email@example.com)

---

**Project Status**: Epic 1 & 2 Complete ✅ | Next: Epic 3 - Agent Implementation
