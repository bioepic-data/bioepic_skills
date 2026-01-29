# bioepic_skills

Primarily a collection of skills for agentic frameworks (e.g., Claude Code), with a supporting Python library for:
1. **Ontology Grounding**: Ground terms to ontologies, especially **BERVO** (Biological and Environmental Research Variable Ontology), using the **Ontology Access Kit (OAK)**
2. **ESS-DIVE Data Extraction**: Extract and process variable names from ESS-DIVE datasets using **trowel**
3. **ESS-DIVE Search**: Search and fetch datasets via the ESS-DIVE API
4. **TRY Discovery**: Discover TRY datasets, traits, and species lists (CLI-free helpers)

## Features

### Ontology Grounding
- 🔍 **Search** ontologies for terms with fuzzy matching
- 📖 **Retrieve** detailed term information including definitions, synonyms, and relationships
- 🎯 **Ground** text terms to ontology concepts with confidence scores
- 🌐 **Access** multiple ontologies: BERVO, ENVO, ChEBI, NCBI Taxonomy, COMO, PO, MIXS
- 🛠️ Built on the powerful [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/)

### ESS-DIVE Data Extraction
- 📦 **Retrieve** dataset metadata from ESS-DIVE API
- 🔬 **Extract** variable names from data files (CSV, TSV, Excel, XML)
- 📚 **Process** data dictionaries with definitions and units
- 🔗 **Match** extracted terms against reference lists
- 🔎 **Search** ESS-DIVE datasets via the API (keyword/provider/parameters)
- 📄 **Fetch** a single ESS-DIVE dataset record by package ID
- 🎯 Built on [trowel](https://github.com/bioepic-data/trowel)

### TRY Database Discovery
- 🔎 **Search** TRY dataset listings by keyword (no public API)
- 📋 **Access** the full TRY trait list (HTML → JSON/TSV helpers)
- 🧬 **Access** the full TRY species list with annotations (TXT → JSON/TSV helpers)


## Installation

### Install Skills in Claude Code

Use Claude Code's Skills commands to install this repo's marketplace and skills.

```bash
/plugin marketplace add bioepic-data/bioepic_skills
/plugin install essdive-extraction@bioepic-skills
/plugin install essdive-search@bioepic-skills
/plugin install try-skills@bioepic-skills
/plugin install ontology-grounding@bioepic-skills
```

See the official Claude Code Skills docs:

```text
https://code.claude.com/docs/en/skills
```

### Use Skills in OpenAI Codex

Codex loads skills from repo and user skill directories. This repo already includes symlinks under `.codex/skills` pointing at the skill folders, so no extra setup is required beyond restarting Codex.

User-scoped install is also supported via `~/.codex/skills`.

Codex Skills documentation:

```text
https://developers.openai.com/codex/skills/
```

### Local Installation (for development)

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

The package includes a `bioepic` command-line tool with 11 commands:

**Ontology Commands:**
```bash
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

**ESS-DIVE Commands:**
```bash
# Set up authentication token (required)
export ESSDIVE_TOKEN="your-token-here"

# Retrieve metadata for datasets
bioepic essdive-metadata dois.txt --output ./data

# Extract variable names from data files
bioepic essdive-variables --output ./data --workers 20

# Search for datasets
bioepic essdive-search --keyword "soil" --page-size 10

# Fetch a dataset record
bioepic essdive-dataset 7a9f0b1f-1234-5678-9abc-def012345678

# Match extracted variables against BERVO terms
bioepic match-terms variable_names.tsv bervo_terms.txt --fuzzy
```

**TRY Skills (CLI-free helpers):**
```bash
# Download TRY datasets page (use --insecure if certificate checks fail)
python skills/try-skills/scripts/try_download_and_search.py --page datasets --save try_datasets.html
python skills/try-skills/scripts/try_download_and_search.py --page datasets --save try_datasets.html --insecure

# Convert datasets page to detailed JSON/TSV
python skills/try-skills/scripts/try_datasets_to_json.py try_datasets.html --format json --output try_datasets_detailed.json
python skills/try-skills/scripts/try_datasets_to_json.py try_datasets.html --format tsv --output try_datasets_detailed.tsv

# Download and convert TRY trait list
python skills/try-skills/scripts/try_download_and_search.py --page traits --save try_traits.html
python skills/try-skills/scripts/try_download_and_search.py --page traits --save try_traits.html --insecure
python skills/try-skills/scripts/try_traits_to_json.py try_traits.html --format tsv --output try_traits.tsv

# Download and convert TRY species list
python skills/try-skills/scripts/try_download_and_search.py --page species --save TryAccSpecies.txt
python skills/try-skills/scripts/try_download_and_search.py --page species --save TryAccSpecies.txt --insecure
python skills/try-skills/scripts/try_species_to_json.py TryAccSpecies.txt --format json --output try_species.json
```

### Python API

Use the library programmatically in your Python code:

```python
from bioepic_skills.ontology_grounding import (
    search_ontology,
    get_term_details,
    ground_terms
)
from bioepic_skills.essdive_api import search_essdive_packages

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

# Search ESS-DIVE datasets by keyword
datasets = search_essdive_packages(keyword="soil", page_size=5)
print(datasets)
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
- **NCBI Taxonomy** - Organism taxonomy
- **COMO** - Context and Measurement Ontology (via BioPortal)
- **PO** - Plant Ontology
- **MIXS** - Minimal Information about any Sequence (via BioPortal)

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

## Skills

This repository includes agent skills for Claude Code and similar tools. These skills are the primary product of this repo; the Python library and CLI utilities exist to make those skills executable and reusable:

- `ontology-grounding` for ontology lookup and grounding
- `essdive-extraction` for ESS-DIVE metadata/variable extraction and term matching
- `essdive-search` for ESS-DIVE Dataset API search and dataset fetch (plus CLI-free fallbacks)
- `try-skills` for TRY dataset discovery, trait list access, and species coverage checks

See `skills/README.md` for details.

## Resources

- **Ontology Access Kit (OAK)**: https://incatools.github.io/ontology-access-kit/
- **BERVO on BioPortal**: https://bioportal.bioontology.org/ontologies/BERVO
- **OAK MCP Reference**: https://github.com/monarch-initiative/oak-mcp

## License

See LICENSE file for details.
