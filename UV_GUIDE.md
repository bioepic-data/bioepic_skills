# Quick Guide: Using uv with BioEPIC Skills

## What is uv?

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver, written in Rust. It's 10-100x faster than pip and provides better dependency resolution.

## Installation

### Install uv

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pip (if you prefer)
pip install uv
```

## Getting Started

### Clone and Setup

```bash
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills
uv sync  # This creates a virtual environment and installs all dependencies
```

## Common Commands

### Install Dependencies

```bash
# Install all dependencies (including dev)
uv sync

# Install without dev dependencies
uv sync --no-dev

# Install with all extras
uv sync --all-extras
```

### Add/Remove Packages

```bash
# Add a runtime dependency
uv add requests

# Add a dev dependency
uv add --dev pytest

# Remove a dependency
uv remove package-name
```

### Run Commands

```bash
# Run Python scripts
uv run python script.py

# Run tests
uv run pytest

# Run documentation server
uv run mkdocs serve

# Run any installed command
uv run ruff check .
```

### Update Dependencies

```bash
# Update all dependencies
uv lock --upgrade

# Update a specific package
uv lock --upgrade-package pandas
```

## Virtual Environment

uv automatically creates and manages a `.venv` directory:

```bash
# Activate manually (optional, uv run does this automatically)
source .venv/bin/activate  # Unix/macOS
.venv\Scripts\activate     # Windows

# Check Python version
uv run python --version

# Check installed packages
uv pip list
```

## Development Workflow

### Initial Setup

```bash
# Clone repository
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills

# Setup with uv
uv sync

# Copy environment variables
cp .env.example .env
# Edit .env with your credentials
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=bioepic_skills --cov-report=html

# Run specific tests
uv run pytest bioepic_skills/test/test_api_search.py -v
```

### Linting

```bash
# Check code style
uv run ruff check bioepic_skills/

# Format code
uv run ruff format bioepic_skills/
```

### Documentation

```bash
# Serve documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build
```

## Why uv?

### Speed
- **10-100x faster** than pip for package installation
- Uses a global cache to avoid re-downloading packages
- Parallel dependency resolution

### Better Dependency Resolution
- Resolves dependencies correctly the first time
- Clear error messages when conflicts occur
- Lockfile ensures reproducible builds

### Modern Workflow
- Single `pyproject.toml` for all configuration
- Automatic virtual environment management
- No need for separate requirements.txt files

## Comparison with pip

| Task | pip | uv |
|------|-----|-----|
| Install dependencies | `pip install -e ".[dev]"` | `uv sync` |
| Add package | `pip install pkg` + manual edit | `uv add pkg` |
| Run command | Activate venv first | `uv run command` |
| Update packages | `pip install --upgrade` | `uv lock --upgrade` |
| Speed | Baseline | 10-100x faster |

## Migration from pip

If you're used to pip, here's the mapping:

```bash
# pip commands → uv commands
pip install -e ".[dev]"     → uv sync
pip install package         → uv add package
pip install --upgrade pkg   → uv lock --upgrade-package pkg
pip list                    → uv pip list
pip freeze                  → uv pip freeze
python script.py            → uv run python script.py
pytest                      → uv run pytest
```

## Troubleshooting

### Command not found after installing uv

Add uv to your PATH:
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

### Virtual environment issues

Remove and recreate:
```bash
rm -rf .venv
uv sync
```

### Cache issues

Clear the cache:
```bash
uv cache clean
```

## Learn More

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [BioEPIC Skills Documentation](https://bioepic-data.github.io/bioepic_skills/)
