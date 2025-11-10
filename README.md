# bioepic_skills

A Python library for grounding terms to ontologies, especially **BERVO** (Biological and Environmental Research Variable Ontology), using the **Ontology Access Kit (OAK)**.

## Features

- 🔍 **Search** ontologies for terms with fuzzy matching
- 📖 **Retrieve** detailed term information including definitions, synonyms, and relationships
- 🎯 **Ground** text terms to ontology concepts with confidence scores
- 🌐 **Access** multiple ontologies: BERVO, ENVO, ChEBI, GO, NCBI Taxonomy, Uberon
- 🛠️ Built on the powerful [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/)

## Installation

Install using pip:

```bash
pip install bioepic_skills
```

Or install using uv (recommended):

```bash
uv add bioepic_skills
```

## Quick Start

### Command-Line Interface

The package includes a `bioepic` command-line tool:

```bash
# Get help
bioepic --help

# Show version
bioepic version

# List available ontologies
bioepic ontologies

# Search BERVO for environmental variables
bioepic search "soil moisture" --ontology bervo

# Ground multiple research terms to BERVO
bioepic ground "air temperature" "precipitation" "soil pH" --ontology bervo

# Get detailed information about a term
bioepic term ENVO:00000001

# Save results to JSON
bioepic search "temperature" --ontology bervo --output results.json
```

### Python API

Use the library programmatically in your Python code:

```python
from bioepic_skills.ontology_grounding import (
    search_ontology,
    get_term_details,
    ground_terms
)

# Search for environmental research variables in BERVO
results = search_ontology("soil moisture", ontology_id="bervo", limit=5)
for term_id, ont_id, label in results:
    print(f"{term_id}: {label}")

# Get detailed information about a specific term
details = get_term_details("ENVO:00000001", ontology_id="envo")
print(f"Label: {details['label']}")
print(f"Definition: {details['definition']}")
print(f"Synonyms: {details['synonyms']}")

# Ground multiple research variables to BERVO concepts
terms = ["air temperature", "precipitation", "soil pH"]
results = ground_terms(terms, ontology_id="bervo", threshold=0.8)
for text_term, matches in results.items():
    print(f"\n{text_term}:")
    for match in matches:
        print(f"  {match['term_id']}: {match['label']} (confidence: {match['confidence']})")
```

## About BERVO

**BERVO** (Biological and Environmental Research Variable Ontology) provides comprehensive vocabulary for:

- Environmental research variables and experimental conditions
- Earth science measurements and observations
- Plant science experimental variables
- Geochemistry conditions and processes
- Biological and physicochemical processes in environmental contexts

BERVO models the experimental variables, conditions, and concepts used in environmental research studies. It is accessed through BioPortal: https://bioportal.bioontology.org/ontologies/BERVO

## Available Ontologies

- **BERVO** - Biological and Environmental Research Variables (via BioPortal)
- **ENVO** - Environment Ontology
- **ChEBI** - Chemical Entities of Biological Interest
- **GO** - Gene Ontology
- **NCBI Taxonomy** - Organism taxonomy
- **Uberon** - Cross-species anatomy

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

## Resources

- **Ontology Access Kit (OAK)**: https://incatools.github.io/ontology-access-kit/
- **BERVO on BioPortal**: https://bioportal.bioontology.org/ontologies/BERVO
- **OAK MCP Reference**: https://github.com/monarch-initiative/oak-mcp

## License

See LICENSE file for details.