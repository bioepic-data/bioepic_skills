---
name: essdive-extraction
description: Skills for extracting and processing variable names from ESS-DIVE datasets
---

# Commands

`bioepic essdive-metadata --help`
`bioepic essdive-variables --help`
`bioepic match-terms --help`

## Full details

### ESS-DIVE Metadata Extraction

Usage: `bioepic essdive-metadata [OPTIONS] DOI_FILE`

Retrieve metadata from ESS-DIVE (Environmental System Science Data Infrastructure for a Virtual Ecosystem) for a list of DOIs.

This command connects to the ESS-DIVE API and retrieves comprehensive metadata for datasets, including:
- Dataset names and descriptions
- Variable lists
- Spatial coverage information
- Measurement techniques
- Associated data files

**Requirements:**
- ESSDIVE_TOKEN environment variable must be set
- Get your token at: https://docs.ess-dive.lbl.gov/programmatic-tools/ess-dive-dataset-api#get-access

**Input:**
- Text file containing one DOI per line (with or without "doi:" prefix)

**Output files:**
- `results.tsv`: Dataset metadata with variables, descriptions, methods
- `frequencies.tsv`: Frequency counts of variables across all datasets
- `filetable.tsv`: List of all data files associated with the datasets

Examples:

    # Retrieve metadata for DOIs listed in a file
    bioepic essdive-metadata dois.txt

    # Save output to a specific directory
    bioepic essdive-metadata dois.txt --output ./data

    # Increase verbosity to see progress details
    bioepic essdive-metadata dois.txt -vv

╭─ Arguments ────────────────────────────────────────────────────────────────────╮
│ *    doi_file      PATH  Path to file containing DOIs (one per line) [required]│
╰────────────────────────────────────────────────────────────────────────────────╯

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --output       -o      PATH     Directory where output files should be written│
│                                 [default: .]                                   │
│ --verbose      -v      INTEGER  Increase verbosity [default: 0]               │
│ --help                          Show this message and exit.                   │
╰────────────────────────────────────────────────────────────────────────────────╯

---

### Variable Name Extraction

Usage: `bioepic essdive-variables [OPTIONS]`

Extract variable names and metadata from ESS-DIVE data files.

This command processes the data files identified by `essdive-metadata` and extracts:
- **Column names** from tabular data files (CSV, TSV, Excel)
- **Keywords** from XML metadata files (EML format)
- **Data dictionary** contents with definitions and units

The command uses parallel processing to handle large numbers of files efficiently.

**Requirements:**
- Must run `essdive-metadata` first to generate the filetable

**Output files:**
- `variable_names.tsv`: All extracted variable names with:
  - Frequency (how many datasets contain this variable)
  - Source (column/keyword/data_dictionary)
  - Units (if available)
  - Definition (if available from data dictionary)
  - Dataset IDs and names
  - File descriptions
- `data_dictionaries.tsv`: Compiled data dictionary information from all datasets

Examples:

    # Extract variables from default filetable.tsv
    bioepic essdive-variables

    # Specify output directory and use more workers
    bioepic essdive-variables --output ./data --workers 20

    # Use a specific filetable
    bioepic essdive-variables --filetable ./mydata/filetable.tsv --output ./mydata

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --filetable    -f      PATH     Path to filetable.tsv (defaults to           │
│                                 filetable.tsv in output directory)            │
│ --output       -o      PATH     Directory where output files should be written│
│                                 [default: .]                                   │
│ --workers      -w      INTEGER  Number of parallel workers for file processing│
│                                 [default: 10]                                  │
│ --verbose      -v      INTEGER  Increase verbosity [default: 0]               │
│ --help                          Show this message and exit.                   │
╰────────────────────────────────────────────────────────────────────────────────╯

---

### Term Matching

Usage: `bioepic match-terms [OPTIONS] TERMS_FILE LIST_FILE`

Match terms from a TSV file against a reference list.

This command takes a TSV file with terms in the first column and matches them against a reference list of terms (one per line). It's particularly useful for:
- Checking which extracted ESS-DIVE variables match BERVO terms
- Identifying standardized terminology in extracted data
- Quality control and validation of variable names

**Matching modes:**
- **Exact matching** (default): Only matches identical terms (case-insensitive)
- **Fuzzy matching** (--fuzzy): Uses Levenshtein distance to find approximate matches when exact matches aren't found

The output file contains all original terms with added columns indicating:
- Whether a match was found
- What the matching term was
- Similarity score (for fuzzy matches)

Examples:

    # Exact matching only
    bioepic match-terms variable_names.tsv bervo_terms.txt

    # Enable fuzzy matching with default threshold (80%)
    bioepic match-terms variable_names.tsv reference.txt --fuzzy

    # Use stricter fuzzy matching threshold
    bioepic match-terms vars.tsv refs.txt --fuzzy --threshold 95

    # Save to specific output file
    bioepic match-terms vars.tsv refs.txt --output matched.tsv

╭─ Arguments ────────────────────────────────────────────────────────────────────╮
│ *    terms_file      PATH  TSV file with terms in first column [required]     │
│ *    list_file       PATH  Text file with terms, one per line [required]      │
╰────────────────────────────────────────────────────────────────────────────────╯

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --output       -o      PATH     Output file path                              │
│ --fuzzy        -f               Enable fuzzy matching for terms without exact │
│                                 matches                                        │
│ --threshold    -t      FLOAT    Minimum similarity score (0-100) for fuzzy    │
│                                 matches [default: 80.0]                        │
│ --verbose      -v      INTEGER  Increase verbosity [default: 0]               │
│ --help                          Show this message and exit.                   │
╰────────────────────────────────────────────────────────────────────────────────╯

## Typical Workflow

Here's a complete workflow for extracting and grounding ESS-DIVE variables:

### 1. Prepare DOI list

Create a text file with ESS-DIVE dataset DOIs:
```bash
cat > dois.txt << EOF
doi:10.15485/1234567
doi:10.15485/2345678
doi:10.15485/3456789
EOF
```

### 2. Set up authentication

```bash
export ESSDIVE_TOKEN="your-token-here"
```

Get your token from: https://docs.ess-dive.lbl.gov/programmatic-tools/ess-dive-dataset-api#get-access

### 3. Retrieve metadata

```bash
bioepic essdive-metadata dois.txt --output ./data
```

This creates:
- `data/results.tsv` - dataset metadata
- `data/frequencies.tsv` - variable frequency counts
- `data/filetable.tsv` - list of data files

### 4. Extract variables

```bash
bioepic essdive-variables --output ./data --workers 20
```

This creates:
- `data/variable_names.tsv` - all extracted variables with metadata
- `data/data_dictionaries.tsv` - compiled data dictionary info

### 5. Export BERVO terms for matching

```bash
# Search BERVO and save all terms
bioepic search "" --ontology bervo --limit 10000 --output bervo_terms.json

# Extract just the labels into a text file
python -c "import json; terms = json.load(open('bervo_terms.json')); print('\n'.join(t['label'] for t in terms))" > bervo_terms.txt
```

### 6. Match extracted variables against BERVO

```bash
bioepic match-terms data/variable_names.tsv bervo_terms.txt --fuzzy --output data/matched_bervo.tsv
```

### 7. Ground unmatched terms

For terms that didn't match, try ontology grounding:

```bash
# Extract unmatched terms (those without exact matches)
# Then ground them to BERVO
bioepic ground "soil moisture content" "atmospheric pressure" "leaf area index" --ontology bervo --output data/grounded.json
```

## Python API

You can also use these functions programmatically:

```python
from bioepic_skills.trowel_wrapper import (
    get_essdive_metadata,
    get_essdive_variables,
    match_term_lists
)

# Retrieve metadata
output_files = get_essdive_metadata("dois.txt", "./data")
print(f"Results: {output_files['results']}")
print(f"Filetable: {output_files['filetable']}")

# Extract variables
variables_file = get_essdive_variables(
    filetable_path="./data/filetable.tsv",
    output_dir="./data",
    workers=20
)
print(f"Variables: {variables_file}")

# Match terms
matched_file = match_term_lists(
    terms_file="./data/variable_names.tsv",
    list_file="bervo_terms.txt",
    fuzzy=True,
    similarity_threshold=85.0
)
print(f"Matched terms: {matched_file}")
```

## Use Cases

### 1. Dataset Discovery and Analysis

Extract all variables from a collection of ESS-DIVE datasets to understand what data is available:

```bash
bioepic essdive-metadata dataset_dois.txt --output ./analysis
bioepic essdive-variables --output ./analysis
```

Review `analysis/variable_names.tsv` to see:
- Most common variables across datasets
- Variables with formal definitions
- Variables with units specified

### 2. Ontology Mapping

Map extracted variables to formal ontology terms:

```bash
# Extract variables
bioepic essdive-variables --output ./mapping

# Match against BERVO
bioepic match-terms ./mapping/variable_names.tsv bervo_terms.txt --fuzzy --output ./mapping/bervo_matched.tsv

# Ground unmatched terms
# (extract unmatched terms first, then ground them)
bioepic ground "term1" "term2" "term3" --ontology bervo
```

### 3. Data Standardization

Identify which datasets use standardized terminology:

```bash
# Get variables from all datasets
bioepic essdive-variables --output ./standardization

# Check against standard terms
bioepic match-terms ./standardization/variable_names.tsv standard_terms.txt --output ./standardization/compliance.tsv
```

Review the output to see which datasets follow naming conventions.

### 4. Cross-Dataset Integration

Find common variables across multiple datasets for integration:

```bash
# Extract variables
bioepic essdive-variables --output ./integration

# Check frequencies.tsv to find variables that appear in multiple datasets
# These are good candidates for cross-dataset analysis
```

## Tips

- **Performance**: Use `--workers` to adjust parallel processing based on your system
- **Large datasets**: Process subsets of DOIs if you have thousands of datasets
- **Token expiration**: ESS-DIVE tokens expire; get a fresh token if you see 401 errors
- **Fuzzy matching**: Start with threshold 80, increase to 90+ for stricter matching
- **Variable quality**: Data dictionaries provide the best metadata - prioritize datasets with DD files
