# Workflows and Examples

This guide provides complete, real-world workflows combining ontology grounding and ESS-DIVE data extraction.

## Workflow 1: Ground ESS-DIVE Variables to BERVO

This comprehensive workflow extracts variables from ESS-DIVE datasets and maps them to BERVO ontology terms.

### Step 1: Prepare Your Dataset List

Create a file with ESS-DIVE dataset DOIs you want to analyze:

```bash
cat > dois.txt << 'EOF'
doi:10.15485/1873253
doi:10.15485/1873254
doi:10.15485/1873255
EOF
```

### Step 2: Set Up Authentication

Get your ESS-DIVE API token from [ESS-DIVE API documentation](https://docs.ess-dive.lbl.gov/programmatic-tools/ess-dive-dataset-api#get-access) and set it as an environment variable:

```bash
export ESSDIVE_TOKEN="your-token-here"
```

### Step 3: Retrieve Dataset Metadata

Extract metadata from all datasets:

```bash
bioepic essdive-metadata dois.txt --output ./workflow1
```

This creates three files in `./workflow1/`:
- `results.tsv` - Dataset metadata (names, descriptions, site info, methods)
- `frequencies.tsv` - How often each variable appears across datasets
- `filetable.tsv` - List of all data files to process

**Example output:**
```
INFO: Processing identifiers: 100%|████████████| 3/3 [00:15<00:00]
✓ Metadata retrieval complete!

Output files:
  • results: ./workflow1/results.tsv
  • frequencies: ./workflow1/frequencies.tsv
  • filetable: ./workflow1/filetable.tsv
```

### Step 4: Extract Variable Names

Process all data files to extract variable names:

```bash
bioepic essdive-variables --output ./workflow1 --workers 20
```

This creates:
- `variable_names.tsv` - All extracted variables with metadata (frequency, source, units, definitions, dataset associations)
- `data_dictionaries.tsv` - Compiled data dictionary information

The command processes:
- CSV/TSV files (extracts column headers)
- Excel files (.xlsx, .xls)
- XML metadata files (extracts keywords)
- Data dictionary files (extracts terms with definitions)

**Example output:**
```
INFO: Processing 145 files with 20 workers...
Processing data files: 100%|████████████| 120/120 [02:30<00:00]
Processing data dictionaries: 100%|████████| 25/25 [00:45<00:00]
✓ Variable extraction complete!
Output file: ./workflow1/variable_names.tsv
```

### Step 5: Export BERVO Terms

Get all terms from BERVO to use as a reference:

```bash
# Search BERVO with empty query to get all terms
bioepic search "" --ontology bervo --limit 10000 --output ./workflow1/bervo_all.json

# Extract just the labels into a text file for matching
python3 << 'EOF'
import json
with open('./workflow1/bervo_all.json') as f:
    terms = json.load(f)
with open('./workflow1/bervo_terms.txt', 'w') as f:
    for term in terms:
        f.write(term['label'] + '\n')
EOF
```

Alternatively, use Python directly:

```python
from bioepic_skills.ontology_grounding import search_ontology
import json

# Get all BERVO terms
results = search_ontology("", ontology_id="bervo", limit=10000)

# Save to file
with open('./workflow1/bervo_terms.txt', 'w') as f:
    for term_id, ont_id, label in results:
        f.write(f"{label}\n")
```

### Step 6: Match Variables to BERVO Terms

Use fuzzy matching to find which extracted variables match BERVO terms:

```bash
bioepic match-terms ./workflow1/variable_names.tsv ./workflow1/bervo_terms.txt \
    --fuzzy \
    --threshold 85 \
    --output ./workflow1/bervo_matched.tsv
```

This creates a file showing:
- Original variable name
- Whether an exact or fuzzy match was found
- The matching BERVO term
- Similarity score (for fuzzy matches)

**Example output:**
```
✓ Term matching complete!
Output file: ./workflow1/bervo_matched.tsv
```

### Step 7: Ground Unmatched Terms

For variables without good matches, use ontology grounding:

```bash
# First, extract unmatched terms (those without exact matches)
awk -F'\t' '$2 != "exact_match" {print $1}' ./workflow1/bervo_matched.tsv | \
    tail -n +2 > ./workflow1/unmatched.txt

# Ground the first 10 unmatched terms as an example
head -10 ./workflow1/unmatched.txt | xargs bioepic ground \
    --ontology bervo \
    --threshold 0.7 \
    --output ./workflow1/grounded.json
```

Or programmatically in Python:

```python
from bioepic_skills.ontology_grounding import ground_terms
import pandas as pd

# Read matched results
matched = pd.read_csv('./workflow1/bervo_matched.tsv', sep='\t')

# Get unmatched terms (no exact match found)
unmatched = matched[matched['match_type'] != 'exact_match']['term'].tolist()

# Ground unmatched terms in batches
batch_size = 50
for i in range(0, len(unmatched), batch_size):
    batch = unmatched[i:i+batch_size]
    results = ground_terms(batch, ontology_id="bervo", threshold=0.7, limit_per_term=3)
    
    # Process results
    for term, matches in results.items():
        if matches:
            print(f"\n{term}:")
            for match in matches:
                print(f"  {match['term_id']}: {match['label']} (confidence: {match['confidence']:.2f})")
```

### Step 8: Analyze Results

Review the matching quality:

```bash
# Count exact matches vs. fuzzy matches vs. no matches
echo "Matching statistics:"
awk -F'\t' 'NR>1 {count[$2]++} END {for (type in count) print type": "count[type]}' \
    ./workflow1/bervo_matched.tsv

# Show most common unmatched variables
awk -F'\t' 'NR>1 && $2=="no_match" {print $1}' ./workflow1/bervo_matched.tsv | \
    sort | uniq -c | sort -rn | head -20
```

### Complete Python Script

Here's a complete Python script for the entire workflow:

```python
#!/usr/bin/env python3
"""Complete workflow: Extract ESS-DIVE variables and map to BERVO."""

import os
import json
import pandas as pd
from pathlib import Path
from bioepic_skills.trowel_wrapper import get_essdive_metadata, get_essdive_variables, match_term_lists
from bioepic_skills.ontology_grounding import search_ontology, ground_terms

def main():
    # Configuration
    output_dir = Path("./workflow1")
    output_dir.mkdir(exist_ok=True)
    doi_file = "dois.txt"
    
    # Check for token
    if not os.getenv("ESSDIVE_TOKEN"):
        print("ERROR: ESSDIVE_TOKEN environment variable not set")
        return
    
    print("Step 1: Retrieving ESS-DIVE metadata...")
    metadata_files = get_essdive_metadata(doi_file, str(output_dir))
    print(f"  Created: {metadata_files['results']}")
    
    print("\nStep 2: Extracting variables...")
    variables_file = get_essdive_variables(
        filetable_path=metadata_files['filetable'],
        output_dir=str(output_dir),
        workers=20
    )
    print(f"  Created: {variables_file}")
    
    print("\nStep 3: Getting BERVO terms...")
    bervo_terms = search_ontology("", ontology_id="bervo", limit=10000)
    bervo_file = output_dir / "bervo_terms.txt"
    with open(bervo_file, 'w') as f:
        for _, _, label in bervo_terms:
            f.write(f"{label}\n")
    print(f"  Created: {bervo_file}")
    
    print("\nStep 4: Matching variables to BERVO...")
    matched_file = match_term_lists(
        terms_file=variables_file,
        list_file=str(bervo_file),
        output=str(output_dir / "bervo_matched.tsv"),
        fuzzy=True,
        similarity_threshold=85.0
    )
    print(f"  Created: {matched_file}")
    
    print("\nStep 5: Analyzing results...")
    matched = pd.read_csv(matched_file, sep='\t')
    print(f"  Total variables: {len(matched)}")
    print(f"  Exact matches: {len(matched[matched['match_type'] == 'exact_match'])}")
    print(f"  Fuzzy matches: {len(matched[matched['match_type'] == 'fuzzy_match'])}")
    print(f"  No matches: {len(matched[matched['match_type'] == 'no_match'])}")
    
    print("\nStep 6: Grounding top unmatched terms...")
    unmatched = matched[matched['match_type'] == 'no_match']['term'].tolist()[:20]
    if unmatched:
        grounded = ground_terms(unmatched, ontology_id="bervo", threshold=0.7, limit_per_term=3)
        grounded_file = output_dir / "grounded.json"
        with open(grounded_file, 'w') as f:
            json.dump(grounded, f, indent=2)
        print(f"  Created: {grounded_file}")
    
    print("\n✓ Workflow complete!")
    print(f"\nResults in: {output_dir}/")

if __name__ == "__main__":
    main()
```

---

## Workflow 2: Multi-Dataset Variable Comparison

This workflow compares variables across multiple datasets to identify common measurement patterns and standardization gaps.

### Step 1: Organize Datasets by Research Domain

Create separate DOI files for different research domains:

```bash
# Soil science datasets
cat > soil_dois.txt << 'EOF'
doi:10.15485/1234567
doi:10.15485/1234568
EOF

# Atmospheric science datasets
cat > atmosphere_dois.txt << 'EOF'
doi:10.15485/2234567
doi:10.15485/2234568
EOF

# Marine science datasets
cat > marine_dois.txt << 'EOF'
doi:10.15485/3234567
doi:10.15485/3234568
EOF
```

### Step 2: Extract Variables from Each Domain

```bash
export ESSDIVE_TOKEN="your-token-here"

# Process soil datasets
bioepic essdive-metadata soil_dois.txt --output ./soil
bioepic essdive-variables --output ./soil --workers 20

# Process atmosphere datasets
bioepic essdive-metadata atmosphere_dois.txt --output ./atmosphere
bioepic essdive-variables --output ./atmosphere --workers 20

# Process marine datasets
bioepic essdive-metadata marine_dois.txt --output ./marine
bioepic essdive-variables --output ./marine --workers 20
```

### Step 3: Compare Variable Coverage Across Domains

```python
#!/usr/bin/env python3
"""Compare variables across research domains."""

import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

def load_variables(file_path):
    """Load variables from file."""
    df = pd.read_csv(file_path, sep='\t')
    return set(df['name'].tolist())

def main():
    # Load variables from each domain
    soil_vars = load_variables('./soil/variable_names.tsv')
    atm_vars = load_variables('./atmosphere/variable_names.tsv')
    marine_vars = load_variables('./marine/variable_names.tsv')
    
    # Find common variables
    all_domains = soil_vars & atm_vars & marine_vars
    soil_atm = (soil_vars & atm_vars) - marine_vars
    soil_marine = (soil_vars & marine_vars) - atm_vars
    atm_marine = (atm_vars & marine_vars) - soil_vars
    
    print("Variable Coverage Analysis")
    print("=" * 50)
    print(f"Soil-only variables: {len(soil_vars - atm_vars - marine_vars)}")
    print(f"Atmosphere-only variables: {len(atm_vars - soil_vars - marine_vars)}")
    print(f"Marine-only variables: {len(marine_vars - soil_vars - atm_vars)}")
    print(f"\nShared across all domains: {len(all_domains)}")
    print(f"Shared by soil & atmosphere: {len(soil_atm)}")
    print(f"Shared by soil & marine: {len(soil_marine)}")
    print(f"Shared by atmosphere & marine: {len(atm_marine)}")
    
    # Show common variables
    if all_domains:
        print(f"\nVariables in all domains:")
        for var in sorted(all_domains)[:20]:
            print(f"  • {var}")
    
    # Create visualization
    from matplotlib_venn import venn3
    plt.figure(figsize=(10, 10))
    venn3([soil_vars, atm_vars, marine_vars], 
          ('Soil', 'Atmosphere', 'Marine'))
    plt.title('Variable Overlap Across Research Domains')
    plt.savefig('domain_overlap.png')
    print("\n✓ Visualization saved to domain_overlap.png")

if __name__ == "__main__":
    main()
```

### Step 4: Map Common Variables to Standard Ontologies

```python
#!/usr/bin/env python3
"""Map common variables to multiple ontologies."""

from bioepic_skills.ontology_grounding import ground_terms
import pandas as pd
import json

def main():
    # Load all unique variables
    soil_df = pd.read_csv('./soil/variable_names.tsv', sep='\t')
    atm_df = pd.read_csv('./atmosphere/variable_names.tsv', sep='\t')
    marine_df = pd.read_csv('./marine/variable_names.tsv', sep='\t')
    
    all_vars = set(soil_df['name']) | set(atm_df['name']) | set(marine_df['name'])
    common_vars = list(set(soil_df['name']) & set(atm_df['name']) & set(marine_df['name']))
    
    print(f"Total unique variables: {len(all_vars)}")
    print(f"Variables in all domains: {len(common_vars)}")
    
    # Ground to multiple ontologies
    ontologies = ['bervo', 'envo', 'chebi']
    results = {}
    
    for ont in ontologies:
        print(f"\nGrounding to {ont.upper()}...")
        ont_results = ground_terms(
            common_vars[:50],  # Process first 50 as example
            ontology_id=ont,
            threshold=0.7,
            limit_per_term=3
        )
        results[ont] = ont_results
    
    # Save results
    with open('multi_ontology_grounding.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Analyze mapping quality
    print("\nMapping Quality Analysis:")
    for ont in ontologies:
        matched = sum(1 for v, matches in results[ont].items() if matches)
        print(f"  {ont.upper()}: {matched}/{len(common_vars[:50])} matched")
    
    print("\n✓ Multi-ontology mapping complete!")

if __name__ == "__main__":
    main()
```

### Step 5: Generate Standardization Report

```python
#!/usr/bin/env python3
"""Generate dataset standardization report."""

import pandas as pd
from collections import defaultdict

def main():
    domains = {
        'soil': './soil/variable_names.tsv',
        'atmosphere': './atmosphere/variable_names.tsv',
        'marine': './marine/variable_names.tsv'
    }
    
    # Load all data
    data = {}
    for domain, file_path in domains.items():
        df = pd.read_csv(file_path, sep='\t')
        data[domain] = df
    
    # Find variables with formal definitions
    print("Variables with Formal Definitions:")
    print("=" * 70)
    
    for domain, df in data.items():
        with_def = df[df['definition'].notna()]
        print(f"\n{domain.upper()}:")
        print(f"  Total variables: {len(df)}")
        print(f"  With definitions: {len(with_def)} ({len(with_def)/len(df)*100:.1f}%)")
        print(f"  With units: {df['units'].notna().sum()} ({df['units'].notna().sum()/len(df)*100:.1f}%)")
        
        # Show examples
        if len(with_def) > 0:
            print(f"\n  Examples:")
            for _, row in with_def.head(3).iterrows():
                print(f"    • {row['name']}")
                print(f"      Definition: {row['definition'][:80]}...")
                if pd.notna(row['units']):
                    print(f"      Units: {row['units']}")
    
    # Identify standardization opportunities
    print("\n\nStandardization Opportunities:")
    print("=" * 70)
    
    # Find similar variable names across domains
    all_vars = defaultdict(list)
    for domain, df in data.items():
        for var in df['name']:
            all_vars[var.lower().strip()].append(domain)
    
    # Variables that appear in multiple domains but with variations
    print("\nVariables appearing in multiple domains:")
    cross_domain = {k: v for k, v in all_vars.items() if len(set(v)) > 1}
    for var, domains_list in sorted(cross_domain.items(), key=lambda x: len(x[1]), reverse=True)[:20]:
        print(f"  • '{var}' in: {', '.join(set(domains_list))}")
    
    print(f"\n✓ Report complete! Found {len(cross_domain)} cross-domain variables")

if __name__ == "__main__":
    main()
```

---

## Workflow 3: Quality Control Pipeline

This workflow validates variable names and identifies potential data quality issues.

### Step 1: Extract Variables with Quality Metrics

```bash
export ESSDIVE_TOKEN="your-token-here"

bioepic essdive-metadata dois.txt --output ./qc
bioepic essdive-variables --output ./qc --workers 20
```

### Step 2: Validate Against Standard Vocabularies

```python
#!/usr/bin/env python3
"""Validate variables against multiple standard vocabularies."""

from bioepic_skills.trowel_wrapper import match_term_lists
from bioepic_skills.ontology_grounding import search_ontology, ground_terms
import pandas as pd
import json

def create_reference_lists():
    """Create reference lists from multiple ontologies."""
    ontologies = {
        'bervo': 'BERVO (Environmental Research Variables)',
        'envo': 'ENVO (Environmental Features)',
        'chebi': 'ChEBI (Chemical Entities)',
        'po': 'PO (Plant Ontology)'
    }
    
    for ont_id, ont_name in ontologies.items():
        print(f"Fetching terms from {ont_name}...")
        results = search_ontology("", ontology_id=ont_id, limit=10000)
        
        with open(f'./qc/{ont_id}_terms.txt', 'w') as f:
            for _, _, label in results:
                f.write(f"{label}\n")
        
        print(f"  Saved {len(results)} terms")

def validate_variables():
    """Validate extracted variables."""
    variables_file = './qc/variable_names.tsv'
    df = pd.read_csv(variables_file, sep='\t')
    
    validation_results = {
        'total_variables': len(df),
        'with_definitions': df['definition'].notna().sum(),
        'with_units': df['units'].notna().sum(),
        'ontology_matches': {}
    }
    
    # Match against each ontology
    for ont in ['bervo', 'envo', 'chebi', 'po']:
        print(f"\nValidating against {ont.upper()}...")
        matched_file = match_term_lists(
            terms_file=variables_file,
            list_file=f'./qc/{ont}_terms.txt',
            output=f'./qc/matched_{ont}.tsv',
            fuzzy=True,
            similarity_threshold=80.0
        )
        
        matched_df = pd.read_csv(matched_file, sep='\t')
        exact = len(matched_df[matched_df['match_type'] == 'exact_match'])
        fuzzy = len(matched_df[matched_df['match_type'] == 'fuzzy_match'])
        
        validation_results['ontology_matches'][ont] = {
            'exact': exact,
            'fuzzy': fuzzy,
            'none': len(matched_df) - exact - fuzzy
        }
    
    # Generate quality report
    print("\n" + "=" * 70)
    print("VARIABLE QUALITY REPORT")
    print("=" * 70)
    print(f"\nTotal Variables: {validation_results['total_variables']}")
    print(f"With Definitions: {validation_results['with_definitions']} "
          f"({validation_results['with_definitions']/validation_results['total_variables']*100:.1f}%)")
    print(f"With Units: {validation_results['with_units']} "
          f"({validation_results['with_units']/validation_results['total_variables']*100:.1f}%)")
    
    print("\nOntology Mapping Coverage:")
    for ont, matches in validation_results['ontology_matches'].items():
        total_matched = matches['exact'] + matches['fuzzy']
        coverage = total_matched / validation_results['total_variables'] * 100
        print(f"  {ont.upper()}: {total_matched}/{validation_results['total_variables']} "
              f"({coverage:.1f}%) - {matches['exact']} exact, {matches['fuzzy']} fuzzy")
    
    # Save report
    with open('./qc/quality_report.json', 'w') as f:
        json.dump(validation_results, f, indent=2)
    
    print("\n✓ Quality report saved to ./qc/quality_report.json")
    
    # Identify high-quality variables (have definition, units, and ontology match)
    high_quality = df[
        df['definition'].notna() & 
        df['units'].notna()
    ]
    
    print(f"\nHigh-Quality Variables (with definitions and units):")
    print(f"  Count: {len(high_quality)} ({len(high_quality)/len(df)*100:.1f}%)")
    
    if len(high_quality) > 0:
        print("\n  Top examples:")
        for _, row in high_quality.head(5).iterrows():
            print(f"    • {row['name']} ({row['units']})")
            print(f"      {row['definition'][:100]}...")

def main():
    print("Creating reference lists from ontologies...")
    create_reference_lists()
    
    print("\n\nValidating variables...")
    validate_variables()

if __name__ == "__main__":
    main()
```

### Step 3: Flag Potential Issues

```python
#!/usr/bin/env python3
"""Identify potential data quality issues."""

import pandas as pd
import re

def detect_issues():
    """Detect potential issues in variable names."""
    df = pd.read_csv('./qc/variable_names.tsv', sep='\t')
    
    issues = {
        'too_short': [],
        'too_long': [],
        'has_numbers_only': [],
        'special_chars': [],
        'inconsistent_case': [],
        'no_metadata': []
    }
    
    for _, row in df.iterrows():
        name = row['name']
        
        # Check length
        if len(name) < 3:
            issues['too_short'].append(name)
        if len(name) > 100:
            issues['too_long'].append(name)
        
        # Check for numbers only
        if name.replace('.', '').replace('-', '').isdigit():
            issues['has_numbers_only'].append(name)
        
        # Check for excessive special characters
        if len(re.findall(r'[^a-zA-Z0-9\s\-_()]', name)) > 3:
            issues['special_chars'].append(name)
        
        # Check for inconsistent casing (mix of camelCase, snake_case, etc.)
        if re.search(r'[a-z][A-Z]', name):
            issues['inconsistent_case'].append(name)
        
        # Check for no metadata
        if pd.isna(row['definition']) and pd.isna(row['units']):
            issues['no_metadata'].append(name)
    
    print("POTENTIAL DATA QUALITY ISSUES")
    print("=" * 70)
    
    for issue_type, vars_list in issues.items():
        if vars_list:
            print(f"\n{issue_type.replace('_', ' ').title()}: {len(vars_list)}")
            for var in vars_list[:5]:
                print(f"  • {var}")
            if len(vars_list) > 5:
                print(f"  ... and {len(vars_list) - 5} more")
    
    # Generate recommendations
    print("\n\nRECOMMENDATIONS")
    print("=" * 70)
    
    if issues['no_metadata']:
        print(f"\n1. Add metadata for {len(issues['no_metadata'])} variables")
        print("   Consider creating data dictionaries with definitions and units")
    
    if issues['has_numbers_only']:
        print(f"\n2. Replace {len(issues['has_numbers_only'])} numeric-only variable names")
        print("   Use descriptive names instead of numbers")
    
    if issues['inconsistent_case']:
        print(f"\n3. Standardize naming convention for {len(issues['inconsistent_case'])} variables")
        print("   Choose one: snake_case, camelCase, or kebab-case")
    
    print("\n✓ Issue detection complete!")

if __name__ == "__main__":
    detect_issues()
```

---

## Tips for Effective Workflows

### Performance Optimization

1. **Parallel Processing**: Use `--workers` flag to speed up file processing
   ```bash
   bioepic essdive-variables --workers 30  # More workers for large datasets
   ```

2. **Batch Processing**: Process datasets in batches if you have hundreds
   ```bash
   split -l 50 all_dois.txt batch_
   for batch in batch_*; do
       bioepic essdive-metadata $batch --output ./batch_$(basename $batch)
   done
   ```

3. **Caching Results**: Save intermediate results to avoid re-processing
   ```bash
   # Save ontology terms once, reuse multiple times
   bioepic search "" --ontology bervo --output bervo_cache.json
   ```

### Error Handling

1. **Check for Token Expiration**:
   ```bash
   if ! bioepic essdive-metadata test.txt 2>&1 | grep -q "401"; then
       echo "Token valid"
   else
       echo "Token expired - refresh your ESSDIVE_TOKEN"
   fi
   ```

2. **Validate File Existence**:
   ```python
   import os
   required_files = ['dois.txt', 'bervo_terms.txt']
   for f in required_files:
       if not os.path.exists(f):
           raise FileNotFoundError(f"Required file missing: {f}")
   ```

3. **Handle Network Errors**:
   ```python
   from bioepic_skills.trowel_wrapper import get_essdive_metadata
   import time
   
   max_retries = 3
   for attempt in range(max_retries):
       try:
           result = get_essdive_metadata('dois.txt', './output')
           break
       except RuntimeError as e:
           if attempt < max_retries - 1:
               print(f"Attempt {attempt + 1} failed, retrying...")
               time.sleep(5)
           else:
               raise
   ```

### Best Practices

1. **Version Control Your Data**: Keep DOI lists and configuration in git
2. **Document Your Workflow**: Add README.md to each workflow directory
3. **Use Consistent Naming**: Follow a naming convention for output directories
4. **Backup Raw Data**: Keep original TSV files before processing
5. **Log Your Runs**: Redirect output to log files for debugging

```bash
bioepic essdive-metadata dois.txt --output ./data 2>&1 | tee run.log
```
