---
name: ontology-grounding
description: Skills for grounding environmental and biological research variable names to appropriate ontologies using the Ontology Access Kit
---

# Command

`bioepic ground --help`

## Full details

Usage: `bioepic ground [OPTIONS] TERMS...`

Ground multiple text terms to ontology terms with confidence scores.

This command takes a list of terms (variable names, concepts, etc.) and attempts to find matching ontology terms across the specified ontology. Returns confidence scores to indicate match quality:
- 1.0: Exact match
- 0.9: Substring match
- 0.7: Found but not exact

The grounding process helps standardize terminology and link free-text descriptions to formal ontology concepts, making data more interoperable and machine-readable.

Examples:

    # Ground environmental variables to BERVO
    bioepic ground "soil moisture" "air temperature" "precipitation"

    # Ground with higher confidence threshold
    bioepic ground "soil moisture" "pH" --threshold 0.9

    # Ground to different ontology
    bioepic ground "cellulose" "lignin" --ontology chebi

    # Get more matches per term
    bioepic ground "temperature" "humidity" --limit 5

    # Ground terms and save to file
    bioepic ground "soil moisture" "air temperature" --output grounded.json

╭─ Arguments ────────────────────────────────────────────────────────────────────╮
│ *    terms      TEXT...  One or more terms to ground [required]               │
╰────────────────────────────────────────────────────────────────────────────────╯

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --ontology    -o      TEXT     Ontology to use for grounding                  │
│                                 [default: bervo]                               │
│ --threshold   -t      FLOAT    Minimum confidence threshold (0.0-1.0)         │
│                                 [default: 0.7]                                 │
│ --limit       -l      INTEGER  Maximum results per term [default: 3]          │
│ --output              PATH     Output file for results (JSON format)          │
│ --help                         Show this message and exit.                    │
╰────────────────────────────────────────────────────────────────────────────────╯

## Available Ontologies

Use `bioepic ontologies` to see the full list of available ontologies:

- **BERVO**: Biological and Environmental Research Variable Ontology - environmental research variables, earth science measurements, plant science parameters, geochemistry
- **ENVO**: Environment Ontology - environmental features, habitats, ecosystems
- **ChEBI**: Chemical Entities of Biological Interest - chemical compounds and their properties
- **NCBI Taxonomy**: Organism taxonomy and classification
- **COMO**: Context and Measurement Ontology - environmental microbiology contexts and measurements
- **PO**: Plant Ontology - plant anatomy, morphology, developmental stages
- **MIXS**: Minimal Information about any Sequence - genomic and metagenomic sequence metadata standards

## Python API

You can also use the grounding functionality programmatically:

```python
from bioepic_skills.ontology_grounding import ground_terms

# Ground a list of terms
terms = ["soil moisture", "air temperature", "precipitation"]
results = ground_terms(terms, ontology_id="bervo", threshold=0.7, limit_per_term=3)

for term, matches in results.items():
    print(f"\nTerm: {term}")
    for match in matches:
        print(f"  - {match['label']} ({match['term_id']}) - confidence: {match['confidence']}")
```

## Use Cases

### 1. Standardizing Research Data

When collecting environmental data, researchers often use varying terminology:
- "soil water content" vs "soil moisture" vs "volumetric water content"
- "ambient temperature" vs "air temperature" vs "atmospheric temperature"

Grounding these terms to BERVO provides standard identifiers that make data comparable across studies.

### 2. Data Integration

Ground metadata fields before integrating datasets from different sources:

```bash
# Ground all variable names from a study
bioepic ground "dissolved organic carbon" "pH" "salinity" "chlorophyll a" \
    --ontology bervo --output metadata_grounded.json
```

### 3. Quality Control

Use confidence scores to identify terms that may need manual review:

```bash
# Only accept high-confidence matches
bioepic ground "temperature" "humidity" "precipitation" --threshold 0.9
```

Low confidence scores might indicate:
- Ambiguous terminology that needs clarification
- Terms that aren't well-represented in existing ontologies
- Typos or non-standard abbreviations

### 4. Multi-Ontology Grounding

Ground different types of terms to their appropriate ontologies:

```bash
# Environmental variables to BERVO
bioepic ground "soil moisture" "air temperature" -o bervo

# Chemical compounds to ChEBI
bioepic ground "glucose" "cellulose" "lignin" -o chebi

# Organisms to NCBI Taxonomy
bioepic ground "Escherichia coli" "Homo sapiens" -o ncbitaxon
```

## Tips

- Start with the default threshold (0.7) and adjust based on your precision needs
- Use `bioepic search` to explore ontology content before grounding
- Review low-confidence matches manually
- Consider grounding to multiple ontologies for comprehensive coverage
- Save results to JSON for downstream processing and record-keeping
