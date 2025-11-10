# justfile for bioepic_skills development
# Run `just` to see available commands

# ============ Variables ============

# Python shebang for cross-platform compatibility
shebang := if os() == 'windows' {
  'py'
} else {
  '/usr/bin/env python3'
}

# ============ Default Command ============

# List all available commands
_default:
    @just --list

# ============ Development Commands ============

# Install dependencies
install:
    uv sync

# Run all tests
test:
    uv run pytest

# Run tests with coverage
test-cov:
    uv run pytest --cov=bioepic_skills --cov-report=html
    @echo "Coverage report generated in htmlcov/index.html"

# Run linting
lint:
    uv run ruff check bioepic_skills/

# Format code
format:
    uv run ruff format bioepic_skills/

# Run type checking (if mypy is added)
typecheck:
    @echo "Type checking not yet configured"
    @echo "To add: uv add --dev mypy"

# ============ Documentation Commands ============

# Serve documentation locally
docs:
    uv run mkdocs serve

# Build documentation
docs-build:
    uv run mkdocs build

# ============ CLI Testing Commands ============

# Test CLI is installed correctly
cli-test:
    uv run bioepic --help

# Test search command with ENVO
cli-search:
    uv run bioepic search "soil" --ontology envo --limit 3 || echo "Search test (may require network)"

# Test ontologies list
cli-ontologies:
    uv run bioepic ontologies

# Test version command
cli-version:
    uv run bioepic version

# ============ Package Management ============

# Update dependencies
update:
    uv lock --upgrade

# Add a new dependency
add PKG:
    uv add {{PKG}}

# Add a new dev dependency
add-dev PKG:
    uv add --dev {{PKG}}

# Remove a dependency
remove PKG:
    uv remove {{PKG}}

# ============ Cleanup Commands ============

# Clean build artifacts
clean:
    rm -rf build/ dist/ *.egg-info .pytest_cache __pycache__
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete

# Clean documentation build
clean-docs:
    rm -rf site/

# Clean everything including virtual environment
clean-all: clean clean-docs
    rm -rf .venv htmlcov/ .coverage

# ============ Build Commands ============

# Build package
build:
    uv build

# Build and check package
build-check: build
    uv run twine check dist/*

# ============ Utility Commands ============

# Show Python environment info
env-info:
    uv run python --version
    uv run python -c "import sys; print(f'Python: {sys.executable}')"
    @echo ""
    @echo "Installed packages:"
    uv pip list

# Show project info
project-info:
    @echo "Project: bioepic_skills"
    @echo "Version: 0.2.0"
    @echo "Python: >=3.10"
    @echo ""
    @echo "CLI command: bioepic"
    @echo "Purpose: Ontology grounding with OAK"
    @echo "Documentation: http://127.0.0.1:8000 (run 'just docs')"
