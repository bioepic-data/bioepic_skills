# Usage Guide

This guide covers common usage patterns and best practices for BioEPIC Skills.

## Overview

BioEPIC Skills provides two main capabilities:

1. **Ontology Grounding** - Map terms to formal ontology concepts
2. **ESS-DIVE Data Extraction** - Extract and process variables from datasets

## Ontology Grounding

### Search for Terms

```python
from bioepic_skills.ontology_grounding import search_ontology

# Search BERVO for environmental terms
results = search_ontology("soil moisture", ontology_id="bervo", limit=10)

for term_id, ont_id, label in results:
    print(f"{term_id}: {label}")
```

### Get Term Details

```python
from bioepic_skills.ontology_grounding import get_term_details

# Get comprehensive information about a term
details = get_term_details("ENVO:00000001", ontology_id="envo")

print(f"Label: {details['label']}")
print(f"Definition: {details['definition']}")
print(f"Synonyms: {details['synonyms']}")

# Access relationships
if details['relationships']:
    for rel_type, fillers in details['relationships'].items():
        print(f"\n{rel_type}:")
        for filler in fillers:
            print(f"  - {filler['label']} ({filler['id']})")
```

### Ground Multiple Terms

```python
from bioepic_skills.ontology_grounding import ground_terms

# Ground research variables to BERVO
terms = [
    "air temperature",
    "soil moisture",
    "precipitation",
    "pH",
    "salinity"
]

results = ground_terms(
    terms,
    ontology_id="bervo",
    threshold=0.7,
    limit_per_term=3
)

# Process results
for term, matches in results.items():
    print(f"\n{term}:")
    if matches:
        for match in matches:
            print(f"  {match['term_id']}: {match['label']}")
            print(f"    Confidence: {match['confidence']:.2f}")
    else:
        print("  No matches found")
```

### List Available Ontologies

```python
from bioepic_skills.ontology_grounding import list_ontologies

ontologies = list_ontologies()

for ont in ontologies:
    print(f"{ont['id']}: {ont['name']}")
    print(f"  {ont['description']}")
```

## ESS-DIVE Data Extraction

### Retrieve Dataset Metadata

```python
import os
from bioepic_skills.trowel_wrapper import get_essdive_metadata

# Set authentication token
os.environ["ESSDIVE_TOKEN"] = "your-token-here"

# Retrieve metadata for datasets
output_files = get_essdive_metadata(
    doi_file="dois.txt",
    output_dir="./data"
)

print(f"Results: {output_files['results']}")
print(f"Frequencies: {output_files['frequencies']}")
print(f"Filetable: {output_files['filetable']}")
```

### Extract Variables from Data Files

```python
from bioepic_skills.trowel_wrapper import get_essdive_variables

# Extract variable names from all data files
variables_file = get_essdive_variables(
    filetable_path="./data/filetable.tsv",
    output_dir="./data",
    workers=20  # Number of parallel workers
)

print(f"Variables extracted to: {variables_file}")

# Read the results
import pandas as pd
df = pd.read_csv(variables_file, sep='\t')
print(f"Found {len(df)} unique variables")
print(f"\nMost common variables:")
print(df.sort_values('frequency', ascending=False).head(10))
```

### Match Terms Against Reference Lists

```python
from bioepic_skills.trowel_wrapper import match_term_lists

# Match extracted variables against BERVO terms
matched_file = match_term_lists(
    terms_file="./data/variable_names.tsv",
    list_file="bervo_terms.txt",
    output="./data/matched_bervo.tsv",
    fuzzy=True,
    similarity_threshold=85.0
)

print(f"Matched results: {matched_file}")

# Analyze matches
df_matched = pd.read_csv(matched_file, sep='\t')
exact_matches = len(df_matched[df_matched['match_type'] == 'exact_match'])
fuzzy_matches = len(df_matched[df_matched['match_type'] == 'fuzzy_match'])
no_matches = len(df_matched[df_matched['match_type'] == 'no_match'])

print(f"\nMatching statistics:")
print(f"  Exact matches: {exact_matches}")
print(f"  Fuzzy matches: {fuzzy_matches}")
print(f"  No matches: {no_matches}")
```

## Combined Workflows

### Ground ESS-DIVE Variables to Ontologies

```python
import os
import pandas as pd
from bioepic_skills.trowel_wrapper import get_essdive_metadata, get_essdive_variables
from bioepic_skills.ontology_grounding import search_ontology, ground_terms

# Set up
os.environ["ESSDIVE_TOKEN"] = "your-token-here"

# Step 1: Get ESS-DIVE data
print("Retrieving metadata...")
metadata = get_essdive_metadata("dois.txt", "./workflow")

print("Extracting variables...")
variables_file = get_essdive_variables(output_dir="./workflow", workers=20)

# Step 2: Load variables
df = pd.read_csv(variables_file, sep='\t')
variable_list = df['name'].tolist()[:50]  # First 50 as example

# Step 3: Ground to BERVO
print("Grounding to BERVO...")
grounded = ground_terms(
    variable_list,
    ontology_id="bervo",
    threshold=0.7,
    limit_per_term=3
)

# Step 4: Analyze results
matched = sum(1 for v, matches in grounded.items() if matches)
print(f"\nResults: {matched}/{len(variable_list)} variables matched to BERVO")

# Show some examples
for var, matches in list(grounded.items())[:5]:
    print(f"\n'{var}':")
    if matches:
        for match in matches[:2]:
            print(f"  → {match['label']} ({match['confidence']:.2f})")
    else:
        print("  No matches")
```

## Error Handling

Always include proper error handling:

```python
from bioepic_skills.ontology_grounding import search_ontology
from bioepic_skills.trowel_wrapper import get_essdive_metadata

# Handle ontology errors
try:
    results = search_ontology("soil moisture", ontology_id="bervo")
except Exception as e:
    print(f"Ontology search failed: {e}")

# Handle ESS-DIVE errors
try:
    metadata = get_essdive_metadata("dois.txt", "./output")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except RuntimeError as e:
    print(f"ESS-DIVE API error: {e}")
    # Check if token is set
    if not os.getenv("ESSDIVE_TOKEN"):
        print("Remember to set ESSDIVE_TOKEN environment variable")
```

## Best Practices

### 1. Use Environment Variables for Tokens

```python
import os

# Set token from environment
token = os.getenv("ESSDIVE_TOKEN")
if not token:
    raise ValueError("ESSDIVE_TOKEN not set")
```

### 2. Process Data in Batches

```python
# For large lists of terms
batch_size = 50
for i in range(0, len(all_terms), batch_size):
    batch = all_terms[i:i+batch_size]
    results = ground_terms(batch, ontology_id="bervo")
    # Process results...
```

### 3. Cache Ontology Results

```python
import json
from pathlib import Path

cache_file = Path("bervo_cache.json")

# Load from cache if available
if cache_file.exists():
    with open(cache_file) as f:
        bervo_terms = json.load(f)
else:
    # Query and cache
    results = search_ontology("", ontology_id="bervo", limit=10000)
    bervo_terms = [{"id": tid, "label": label} for tid, _, label in results]
    with open(cache_file, 'w') as f:
        json.dump(bervo_terms, f)
```

### 4. Use Parallel Processing for Large Datasets

```python
# Use more workers for large ESS-DIVE datasets
variables_file = get_essdive_variables(
    output_dir="./data",
    workers=30  # Increase for better performance
)
```

## Logging and Debugging

### Enable Verbose Output

```bash
# CLI with verbose mode
bioepic search "soil moisture" -vv

# Or in Python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Custom Logger

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Use in your code
logger.info("Starting ontology grounding...")
results = ground_terms(terms, ontology_id="bervo")
logger.info(f"Matched {len(results)} terms")
```

## Next Steps

- Explore complete [Workflows & Examples](workflows.md) for end-to-end workflows
- Check the [Command-Line Interface](cli.md) documentation
- Review [Testing](../development/testing.md) guidelines
