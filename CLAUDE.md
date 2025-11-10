# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

`bioepic_skills` is a Python library and CLI tool for grounding terms to ontologies using the Ontology Access Kit (OAK). The project focuses on environmental and biological research, with special emphasis on:

- **BERVO** (Biological and Environmental Research Variable Ontology)
- **ENVO** (Environment Ontology)
- **ChEBI** (Chemical Entities of Biological Interest)
- **NCBI Taxonomy**
- **COMO** (Context and Measurement Ontology)
- **PO** (Plant Ontology)
- **MIXS** (Minimal Information about any Sequence)

### Key Components

- **Python API**: Ontology grounding functions (`ontology_grounding.py`)
- **CLI**: Typer-based command-line tool (`bioepic` command)
- **OAK Integration**: Uses Ontology Access Kit for multiple ontology backends
- **Rich Output**: Beautiful terminal output with tables and formatted text

## Development Commands

### Installation

This project uses `uv` for modern Python dependency management.

```bash
# Install dependencies and create virtual environment
uv sync

# Install with dev dependencies (for testing, docs, etc.)
uv sync --extra dev

# Install with all extras
uv sync --all-extras
```

### Running Tests

Tests are fast unit tests that don't require network access.

```bash
# Run all tests with uv
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest bioepic_skills/test/test_ontology_grounding.py

# Run with coverage
uv run pytest --cov=bioepic_skills --cov-report=html
```

### Using the CLI

```bash
# Test the CLI during development
uv run bioepic --help
uv run bioepic version
uv run bioepic ontologies

# Search for terms
uv run bioepic search "soil moisture" --ontology bervo

# Ground multiple terms
uv run bioepic ground "air temperature" "precipitation" --ontology bervo

# Get term details
uv run bioepic term ENVO:00000001

# After installation, use directly
bioepic --help
bioepic search "temperature" --ontology envo
```

### Using Just Commands

The project includes a `justfile` for common tasks:

```bash
# List all available commands
just

# Run tests
just test

# Run tests with coverage
just test-cov

# Format code
just format

# Lint code
just lint

# Serve documentation locally
just docs

# Build documentation
just docs-build

# Test CLI
just cli-test
just cli-version
just cli-ontologies

# Show project info
just project-info
```

### Building Documentation

```bash
# Using uv (dev dependencies include mkdocs)
uv run mkdocs serve

# Or using just
just docs

# Build static site
uv run mkdocs build
just docs-build
```

## Architecture

### Python API Architecture

The library provides a functional API for ontology operations:

**Core Module: `ontology_grounding.py`**

1. **Configuration**: `ONTOLOGY_CONFIGS` dictionary maps ontology IDs to selectors
   - BioPortal ontologies: `bioportal:BERVO`, `bioportal:COMO`, `bioportal:MIXS`
   - OBO ontologies: `sqlite:obo:envo`, `sqlite:obo:chebi`, `sqlite:obo:po`, etc.

2. **Core Functions**:
   - `get_ontology_adapter(ontology_id)`: Gets OAK adapter for specified ontology
   - `search_ontology(search_term, ontology_id, limit)`: Search for terms
   - `get_term_details(term_id, ontology_id)`: Get detailed term information
   - `ground_terms(text_terms, ontology_id, threshold, limit_per_term)`: Ground text to concepts
   - `list_ontologies()`: List available ontologies

3. **OAK Integration**: Uses `oaklib.get_adapter()` with selector strings
   - Supports multiple backends (BioPortal, SQLite, OLS)
   - Automatic adapter selection based on ontology configuration

### CLI Architecture (cli.py)

The CLI is built with Typer and Rich, providing the following commands:

- **ontologies**: List available ontologies with descriptions
- **search**: Search for ontology terms with filters and pagination
- **term**: Get detailed information about a specific term (with relationships)
- **ground**: Ground text terms to ontology concepts with confidence scores
- **version**: Show version information
- **info**: Show comprehensive project information

All commands support:
- Verbose logging (`-v`, `-vv`)
- JSON output to file (`--output`)
- Pretty console display with Rich tables
- Comprehensive help text with examples

### Data Flow

1. User calls function or CLI command (e.g., `search_ontology("soil moisture", "bervo")`)
2. Function retrieves ontology configuration from `ONTOLOGY_CONFIGS`
3. Gets OAK adapter using `get_adapter(selector)` (e.g., `bioportal:BERVO`)
4. Executes OAK operations (e.g., `adapter.basic_search()`)
5. Processes results (labels, definitions, relationships)
6. Returns structured data (tuples, dicts, lists)

### Grounding Algorithm

The `ground_terms()` function implements a simple confidence-based matching:

1. For each input text term, search the ontology
2. Calculate confidence scores:
   - Exact match (case-insensitive): 1.0
   - Substring match: 0.9
   - Found in results: 0.7
3. Filter results by threshold (default: 0.8)
4. Return top N matches per term (default: 3)

## Important Notes

- **Dependency Management**: This project uses `uv` for modern dependency management
- **Lightweight Core**: Core dependencies are minimal (oaklib, typer, rich)
- **CLI Entry Point**: The `bioepic` command is configured in `pyproject.toml` under `[project.scripts]` pointing to `bioepic_skills.cli:app`
- **OAK Backends**: Different ontologies use different backends:
  - BioPortal: BERVO, COMO, MIXS (requires network)
  - SQLite: ENVO, ChEBI, PO, NCBI Taxonomy (downloads on first use)
  - OLS: Fallback for cross-ontology search
- **Type Annotations**: Uses Python 3.10+ union syntax (`str | None`)
- **CLI Testing**: CLI commands work immediately with `uv run bioepic`
- **Logging**: Available via standard Python logging; use `--verbose` for detailed output
- **Documentation**: Uses MkDocs with Material theme, mkdocstrings for API docs
- **Import Warnings**: Some false positive import errors from language server (oaklib, typer) can be ignored - packages are installed
- **Testing**: Unit tests don't require network; integration tests with real ontologies should be run separately

## Common Development Tasks

### Adding a New Ontology

1. Add configuration to `ONTOLOGY_CONFIGS` in `ontology_grounding.py`:
   ```python
   "new_ont": {
       "selector": "bioportal:NEWONT",  # or sqlite:obo:newont
       "name": "Full Ontology Name",
       "description": "Description of what it covers",
   }
   ```

2. Update README.md to include the new ontology in the list

3. Update CLI info command if the ontology is particularly important

4. Test with:
   ```bash
   uv run bioepic ontologies  # Should show new ontology
   uv run bioepic search "test" --ontology new_ont
   ```

### Updating Examples

When changing examples (e.g., from biofuel terms to environmental terms):
1. Update docstrings in `ontology_grounding.py`
2. Update CLI help text in `cli.py`
3. Update README.md
4. Update `docs/user-guide/cli.md`
5. Test all examples actually work

### Running Specific Tests

```bash
# Test specific function
uv run pytest -k "test_ontology_configs"

# Test with markers (if we add them)
uv run pytest -m "unit"

# Show what tests would run
uv run pytest --collect-only
```

## Project Structure

```
bioepic_skills/
├── bioepic_skills/
│   ├── __init__.py
│   ├── ontology_grounding.py  # Core functions
│   ├── cli.py                 # CLI commands
│   └── test/
│       └── test_ontology_grounding.py
├── docs/
│   ├── index.md
│   ├── user-guide/
│   │   ├── cli.md
│   │   └── ...
│   └── api/
├── pyproject.toml             # Project config, dependencies
├── uv.lock                    # Locked dependencies
├── justfile                   # Task automation
├── mkdocs.yml                 # Documentation config
└── README.md
```

## Troubleshooting

### OAK Adapter Issues

If an adapter fails to load:
- BioPortal ontologies require network access
- SQLite ontologies download on first use (may take time)
- Check selector string format: `bioportal:ONTID` or `sqlite:obo:ontid`

### Import Errors in IDE

False positive errors like "Import 'oaklib' could not be resolved":
- These are language server issues
- Verify packages are installed: `uv pip list | grep oaklib`
- Run `uv run bioepic --help` to confirm everything works

### Test Failures

If tests fail after changes:
- Run `uv sync` to ensure dependencies are current
- Check if ontology configurations were updated correctly
- Verify test assertions match new data (e.g., ontology names)
