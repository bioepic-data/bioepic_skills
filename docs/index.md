# Welcome to BioEPIC Skills

A Python library and CLI tool for:
1. **Ontology Grounding**: Ground terms to ontologies (especially BERVO) using the Ontology Access Kit (OAK)
2. **ESS-DIVE Data Extraction**: Extract and process variable names from ESS-DIVE datasets using trowel

## Features

### Ontology Grounding
- 🔍 **Search** ontologies for terms with fuzzy matching
- 📖 **Retrieve** detailed term information including definitions, synonyms, and relationships
- 🎯 **Ground** text terms to ontology concepts with confidence scores
- 🌐 **Access** multiple ontologies: BERVO, ENVO, ChEBI, NCBI Taxonomy, COMO, PO, MIXS
- 🛠️ Built on the powerful [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/)

### ESS-DIVE Data Extraction
- � **Retrieve** dataset metadata from ESS-DIVE API
- 🔬 **Extract** variable names from data files (CSV, TSV, Excel, XML)
- 📚 **Process** data dictionaries with definitions and units
- 🔗 **Match** extracted terms against reference lists with fuzzy matching
- ⚡ **Parallel processing** for large datasets
- 🎯 Built on [trowel](https://github.com/bioepic-data/trowel)

## Quick Links

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quickstart.md)
- [Workflows & Examples](user-guide/workflows.md) - **Complete end-to-end workflows!**
- [Command-Line Interface](user-guide/cli.md)
- [Contributing Guidelines](development/contributing.md)

## Overview

BioEPIC Skills bridges the gap between raw environmental research data and formal ontologies. It helps researchers:

- **Standardize** variable names across datasets
- **Link** experimental measurements to formal ontology terms
- **Validate** data quality and completeness
- **Integrate** data from multiple sources

### Special Support for BERVO

**BERVO** (Biological and Environmental Research Variable Ontology) is accessed through BioPortal and provides comprehensive vocabulary for:

- Environmental research variables and conditions
- Earth science experimental variables
- Plant science measurements
- Geochemistry conditions
- Biological and physicochemical processes

## Installation

Install using pip:

```bash
pip install bioepic_skills
```

Or using uv (recommended):

```bash
uv add bioepic_skills
```

Or install from source:

```bash
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills
uv sync
```

## Quick Examples

### Ontology Grounding

```bash
# Search BERVO for environmental variables
bioepic search "soil moisture" --ontology bervo

# Ground multiple research terms
bioepic ground "air temperature" "precipitation" "soil pH" --ontology bervo

# Get detailed term information
bioepic term ENVO:00000001
```

### ESS-DIVE Data Extraction

```bash
# Set authentication token
export ESSDIVE_TOKEN="your-token-here"

# Retrieve dataset metadata
bioepic essdive-metadata dois.txt --output ./data

# Extract variable names
bioepic essdive-variables --output ./data --workers 20

# Match against BERVO terms
bioepic match-terms variable_names.tsv bervo_terms.txt --fuzzy
```

### Python API

```python
from bioepic_skills.ontology_grounding import search_ontology, ground_terms
from bioepic_skills.trowel_wrapper import get_essdive_metadata, get_essdive_variables

# Search for terms in BERVO
results = search_ontology("soil moisture", ontology_id="bervo", limit=5)
for term_id, ont_id, label in results:
    print(f"{term_id}: {label}")

# Ground multiple terms
terms = ["air temperature", "precipitation", "soil pH"]
grounded = ground_terms(terms, ontology_id="bervo", threshold=0.8)

# Extract ESS-DIVE data
metadata = get_essdive_metadata("dois.txt", "./output")
variables = get_essdive_variables(output_dir="./output", workers=20)
```

## Complete Workflows

See the [Workflows & Examples](user-guide/workflows.md) guide for complete end-to-end workflows including:

- **Workflow 1**: Ground ESS-DIVE Variables to BERVO - Extract variables from datasets and map them to ontology terms
- **Workflow 2**: Multi-Dataset Variable Comparison - Compare variables across research domains
- **Workflow 3**: Quality Control Pipeline - Validate variable names and identify quality issues

## Getting Help

- 📖 Check the [User Guide](user-guide/usage.md) for detailed information
- 🐛 Report issues on [GitHub](https://github.com/bioepic-data/bioepic_skills/issues)
- 💬 Ask questions in [Discussions](https://github.com/bioepic-data/bioepic_skills/discussions)

## License

This project is licensed under the BSD License. See the [LICENSE](https://github.com/bioepic-data/bioepic_skills/blob/main/LICENSE) file for details.
