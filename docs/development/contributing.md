# Contributing

Thank you for your interest in contributing to BioEPIC Skills!

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

Run all tests:
```bash
uv run pytest
```

Run with coverage:
```bash
uv run pytest --cov=bioepic_skills --cov-report=html
```

Run specific test files:
```bash
uv run pytest bioepic_skills/test/test_api_search.py
uv run pytest bioepic_skills/test/test_data_processing.py
```

## Building Documentation

Build the documentation locally:
```bash
uv run mkdocs serve
```

This will start a local development server at `http://127.0.0.1:8000/` where you can preview your changes.

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
├── docs/                    # Documentation (MkDocs)
│   ├── index.md
│   ├── getting-started/
│   ├── user-guide/
│   ├── api/
│   └── development/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── pyproject.toml
├── mkdocs.yml               # MkDocs configuration
├── CONTRIBUTING.md
└── CHANGELOG.md
```

## Code Style

We follow Python best practices:

- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Follow PEP 8 style guidelines
- Keep functions focused and modular
- Add type hints where appropriate

Example:

```python
def get_record_by_id(self, record_id: str) -> dict:
    """
    Retrieve a single record by its ID.
    
    Parameters
    ----------
    record_id : str
        The unique identifier of the record
        
    Returns
    -------
    dict
        The record data
        
    Raises
    ------
    RuntimeError
        If the API request fails
    """
    # Implementation...
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Make your changes
4. Run tests to ensure everything works:
   ```bash
   pytest
   ```
5. Commit your changes:
   ```bash
   git commit -m 'Add some amazing feature'
   ```
6. Push to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```
7. Open a Pull Request

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Add tests for new features
- Keep changes focused - one feature per PR

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages or stack traces

## Documentation

When adding or modifying features:

1. Update relevant documentation in `docs/`
2. Add docstrings to new functions/classes
3. Update the CHANGELOG.md
4. Test your documentation locally with `mkdocs serve`

## Questions?

Feel free to open an issue for:

- Feature requests
- Bug reports
- Documentation improvements
- General questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).
