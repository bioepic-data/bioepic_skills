# BioEPIC Skills

## Development Setup

### Using uv (Recommended)

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills
```

3. Install dependencies:
```bash
uv sync
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Using pip

1. Clone the repository:
```bash
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Running Tests

```bash
uv run pytest
```

Or run specific test files:
```bash
uv run pytest bioepic_skills/test/test_api_search.py
uv run pytest bioepic_skills/test/test_data_processing.py
```

## Building Documentation

```bash
uv run mkdocs serve
```

This will start a local development server at `http://127.0.0.1:8000/`

To build the static site:
```bash
uv run mkdocs build
```

The documentation will be built in the `site/` directory.

## Project Structure

```
bioepic_skills/
├── bioepic_skills/          # Main package directory
│   ├── __init__.py          # Package initialization
│   ├── api_base.py          # Base API class
│   ├── api_search.py        # API search functionality
│   ├── auth.py              # Authentication handler
│   ├── data_processing.py   # Data processing utilities
│   ├── decorators.py        # Custom decorators
│   ├── utils.py             # Utility functions
│   ├── example_usage.py     # Usage examples
│   └── test/                # Test directory
│       ├── __init__.py
│       ├── test_api_search.py
│       └── test_data_processing.py
├── docs/                    # Documentation
│   ├── conf.py
│   ├── index.rst
│   ├── functions.rst
│   └── usage.rst
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── pyproject.toml
└── CONTRIBUTING.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

See LICENSE file for details.
