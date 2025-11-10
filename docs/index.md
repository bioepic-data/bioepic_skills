# Welcome to BioEPIC Skills

A Python library designed to simplify various research tasks for users looking to extract and prepare structured data from scientific literature for use with the EcoSIM model.

## Features

- 🔍 **API Search**: Flexible search and query capabilities
- 🔐 **Authentication**: Secure API authentication handling
- 📊 **Data Processing**: Utilities for data transformation and analysis
- 🧪 **Testing**: Comprehensive test suite
- 📚 **Documentation**: Complete API reference and user guides

## Quick Links

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quickstart.md)
- [API Reference](api/api-search.md)
- [Contributing Guidelines](development/contributing.md)

## Overview

BioEPIC Skills provides a collection of general-purpose functions that facilitate easy access, manipulation, and analysis of biological data through APIs.

### Key Components

- **APIBase**: Base class for API interactions with environment configuration
- **APISearch**: Search and retrieve data from API collections
- **BioEPICAuth**: Authentication handler with token management
- **DataProcessing**: Data transformation and analysis utilities

## Installation

Install from source:

```bash
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills
pip install -e ".[dev]"
```

Or via pip (once published):

```bash
pip install bioepic_skills
```

## Quick Example

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

## Getting Help

- 📖 Check the [User Guide](user-guide/usage.md) for detailed information
- 🐛 Report issues on [GitHub](https://github.com/bioepic-data/bioepic_skills/issues)
- 💬 Ask questions in [Discussions](https://github.com/bioepic-data/bioepic_skills/discussions)

## License

This project is licensed under the BSD License. See the [LICENSE](https://github.com/bioepic-data/bioepic_skills/blob/main/LICENSE) file for details.
