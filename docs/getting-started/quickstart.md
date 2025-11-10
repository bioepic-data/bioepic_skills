# Quick Start Guide

This guide will help you get started with BioEPIC Skills quickly.

## Installation

### Using pip

```bash
pip install bioepic_skills
```

### Using uv (recommended)

```bash
uv add bioepic_skills
```

### From source

```bash
git clone https://github.com/bioepic-data/bioepic_skills.git
cd bioepic_skills
uv sync
```

## Basic Usage - Command Line

### List Available Ontologies

```bash
bioepic ontologies
```

### Search for Terms

```bash
# Search BERVO for environmental variables
bioepic search "soil moisture" --ontology bervo

# Search across all ontologies
bioepic search "temperature" --limit 10
```

### Ground Terms to Ontologies

```bash
# Ground multiple terms to BERVO
bioepic ground "air temperature" "precipitation" "soil pH" --ontology bervo

# Save results to file
bioepic ground "temperature" "humidity" --output results.json
```

### Get Term Details

```bash
# Get detailed information about a specific term
bioepic term ENVO:00000001
```

## ESS-DIVE Data Extraction

### Set Up Authentication

```bash
export ESSDIVE_TOKEN="your-token-here"
```

Get your token from: https://docs.ess-dive.lbl.gov/programmatic-tools/ess-dive-dataset-api#get-access

### Retrieve Dataset Metadata

```bash
# Create a file with DOIs (one per line)
cat > dois.txt << 'EOF'
doi:10.15485/1873253
doi:10.15485/1873254
EOF

# Retrieve metadata
bioepic essdive-metadata dois.txt --output ./data
```

### Extract Variables

```bash
# Extract variable names from data files
bioepic essdive-variables --output ./data --workers 20
```

### Match Terms

```bash
# Match extracted variables against reference list
bioepic match-terms variable_names.tsv bervo_terms.txt --fuzzy
```

## Python API Usage

### Ontology Grounding

```python
from bioepic_skills.ontology_grounding import (
    search_ontology,
    get_term_details,
    ground_terms
)

# Search for terms
results = search_ontology("soil moisture", ontology_id="bervo", limit=5)
for term_id, ont_id, label in results:
    print(f"{term_id}: {label}")

# Get term details
details = get_term_details("ENVO:00000001", ontology_id="envo")
print(f"Label: {details['label']}")
print(f"Definition: {details['definition']}")

# Ground multiple terms
terms = ["air temperature", "precipitation", "soil pH"]
results = ground_terms(terms, ontology_id="bervo", threshold=0.8)
for term, matches in results.items():
    print(f"\n{term}:")
    for match in matches:
        print(f"  {match['term_id']}: {match['label']} ({match['confidence']:.2f})")
```

### ESS-DIVE Data Extraction

```python
import os
from bioepic_skills.trowel_wrapper import (
    get_essdive_metadata,
    get_essdive_variables,
    match_term_lists
)

# Set token
os.environ["ESSDIVE_TOKEN"] = "your-token-here"

# Retrieve metadata
metadata_files = get_essdive_metadata("dois.txt", "./output")
print(f"Results: {metadata_files['results']}")
print(f"Filetable: {metadata_files['filetable']}")

# Extract variables
variables_file = get_essdive_variables(
    filetable_path=metadata_files['filetable'],
    output_dir="./output",
    workers=20
)
print(f"Variables: {variables_file}")

# Match terms
matched_file = match_term_lists(
    terms_file=variables_file,
    list_file="bervo_terms.txt",
    fuzzy=True,
    similarity_threshold=85.0
)
print(f"Matched: {matched_file}")
```

## Next Steps

- Check out complete [Workflows & Examples](../user-guide/workflows.md) for end-to-end workflows
- Explore the [Command-Line Interface](../user-guide/cli.md) documentation
- Read the [User Guide](../user-guide/usage.md) for detailed information
