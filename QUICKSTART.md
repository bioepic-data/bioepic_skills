# Quick Start Guide

Welcome to BioEPIC Skills! This guide will help you get started quickly.

## Installation

### Using uv (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills

# Install dependencies
uv sync
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### From PyPI (Once Published)

```bash
pip install bioepic_skills
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```
ENV=prod
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
```

## Basic Usage

### Simple API Query

```python
from bioepic_skills.api_search import APISearch
from bioepic_skills.data_processing import DataProcessing

# Create clients
api_client = APISearch(collection_name="samples")
dp = DataProcessing()

# Get records
records = api_client.get_records(max_page_size=10)

# Convert to DataFrame
df = dp.convert_to_df(records)
print(df.head())
```

### With Authentication

```python
from bioepic_skills.api_search import APISearch
from bioepic_skills.auth import BioEPICAuth
import os

# Initialize authentication
auth = BioEPICAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET")
)

# Use API with authentication
api_client = APISearch(collection_name="samples")
# ... your API calls here
```

### Search by Attribute

```python
# Search for specific records
results = api_client.get_record_by_attribute(
    attribute_name="type",
    attribute_value="biological_sample",
    max_page_size=50,
    all_pages=True
)
```

### Data Processing

```python
# Extract specific fields
ids = dp.extract_field(records, "id")

# Build custom filters
filter_query = dp.build_filter(
    {"name": "test", "status": "active"},
    exact_match=False
)

# Merge DataFrames
merged_df = dp.merge_dataframes("id", df1, df2)
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=bioepic_skills --cov-report=html
```

## Building Documentation

```bash
uv run mkdocs serve
# Open http://127.0.0.1:8000 in your browser

# Or build static site
uv run mkdocs build
```

## Common Issues

### Import Errors

Make sure you've installed the package:
```bash
pip install -e .
```

### Authentication Errors

Verify your credentials in `.env` file and ensure they have the correct permissions.

### API Connection Issues

Check that:
- Your API endpoint URLs are correct in `api_base.py`
- You have network connectivity
- Your credentials are valid

## Next Steps

- Read the full documentation in `docs/`
- Check out `bioepic_skills/example_usage.py` for more examples
- Review `bioepic_skills/example_auth.py` for authentication patterns
- See `CONTRIBUTING.md` for development guidelines

## Getting Help

- Check the documentation in `docs/`
- Review example files in `bioepic_skills/`
- Open an issue on GitHub
