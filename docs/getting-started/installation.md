# Installation

## Requirements

- Python 3.10 or higher
- uv (recommended) or pip

## Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. It's significantly faster than pip and provides better dependency resolution.

### Install uv

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install BioEPIC Skills

```bash
# Clone the repository
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills

# Install with all dependencies
uv sync

# Or install without dev dependencies
uv sync --no-dev
```

## Using pip

For traditional pip installation:

```bash
# From source
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills
pip install -e ".[dev]"

# Or once published to PyPI
pip install bioepic_skills
```

## Verify Installation

Verify the installation by checking the version:

```python
import bioepic_skills
print(bioepic_skills.__version__)
```

## Virtual Environments

uv automatically manages virtual environments for you. When you run `uv sync`, it creates a `.venv` directory in your project.

To activate the virtual environment manually:

```bash
# Unix/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

However, with uv, you typically don't need to activate the environment - just use `uv run` to execute commands:

```bash
uv run python script.py
uv run pytest
uv run mkdocs serve
```

## Dependencies

### Core Dependencies

The following packages are installed automatically:

- `pandas` (≥2.2.3) - Data manipulation and analysis
- `requests` (≥2.32.3) - HTTP library for API calls
- `matplotlib` (≥3.10.0) - Plotting library

### Development Dependencies

For development work, additional packages are installed:

- `pytest` (≥7.0.0) - Testing framework
- `pytest-cov` (≥4.0.0) - Coverage plugin for pytest
- `python-dotenv` (≥1.0.0) - Environment variable management
- `mkdocs` (≥1.5.0) - Documentation generator
- `mkdocs-material` (≥9.0.0) - Material theme for MkDocs
- `mkdocstrings[python]` (≥0.24.0) - Python documentation plugin
- `ruff` (≥0.1.0) - Fast Python linter

These are automatically installed when you run `uv sync`.

## Working with uv

### Common Commands

```bash
# Install/sync dependencies
uv sync

# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Remove a dependency
uv remove package-name

# Run a command in the virtual environment
uv run python script.py
uv run pytest

# Update dependencies
uv lock --upgrade
```

## Next Steps

After installation, proceed to the [Quick Start Guide](quickstart.md) to learn how to use the library.
