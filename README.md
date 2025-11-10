# bioepic_skills

A Python library designed to simplify various research tasks for users looking to extract and prepare structured data from scientific literature for use with the EcoSIM model.

## Installation

Install using pip:

```bash
pip install bioepic_skills
```

Or install using uv (recommended):

```bash
uv add bioepic_skills
```

Periodically run update commands to ensure you have the latest version:
```bash
pip install --upgrade bioepic_skills
# or
uv lock --upgrade
```

## Quick Start

### Command-Line Interface

The package includes a `bioepic` command-line tool for quick access to the API:

```bash
# Get help
bioepic --help

# Show version
bioepic version

# Show API configuration
bioepic info

# Search for samples
bioepic sample --filter "type: soil" --limit 10

# Search by specific attribute
bioepic search depth_cm 15 --limit 5

# Export results to CSV
bioepic sample --filter "location: forest" --output results.csv

# Get all pages of results
bioepic sample --filter "year: 2023" --all-pages --output all_2023_samples.json
```

**Filter Syntax:**
- YAML style: `"key: value"` or `"field: value"`
- JSON style: `'{"field": {"$gte": 10}}'` for MongoDB-like queries

**Output Formats:**
- JSON (default): Full nested data structure
- CSV: Flattened data, suitable for spreadsheets
- TSV: Tab-separated values

### Python API

Use the library programmatically in your Python code:

```python
from bioepic_skills.api_search import APISearch

# Create an instance of the module
api_client = APISearch()

# Get a record by ID
record = api_client.get_record_by_id(record_id="example-id")

# Search with filters
results = api_client.search(filter={"type": "soil"}, limit=10)
```

## Logging - Debug Mode

To see debugging information, include these two lines where ever you are running the functions:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# when this is run, you will see debug information in the console
api_client.get_record_by_id(record_id="example-id")
```

For CLI commands, use the `--verbose` flag:
```bash
bioepic --verbose sample --id example-id
```

## Development

This project uses [uv](https://github.com/astral-sh/uv) for package management and [just](https://github.com/casey/just) for task automation.

```bash
# Install dependencies
uv sync

# Run tests
just test

# Format code
just format

# Serve documentation locally
just docs
```

See the [justfile](justfile) for all available commands.

## Documentation

Full documentation is available at [bioepic-data.github.io/bioepic_skills](https://bioepic-data.github.io/bioepic_skills/)

To build documentation locally:

```bash
uv run mkdocs serve
# or
just docs
```

## License

See LICENSE file for details.