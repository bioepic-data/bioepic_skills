# Command-Line Interface

The `bioepic` command-line tool provides convenient access to ontology grounding operations using the Ontology Access Kit (OAK).

## Installation

After installing the `bioepic_skills` package, the `bioepic` command will be available:

```bash
pip install bioepic_skills
```

Verify the installation:

```bash
bioepic --help
```

## Global Options

All commands support the following global options:

- `--verbose` / `-v`: Enable verbose logging (can be used multiple times: `-v`, `-vv`)
- `--help`: Show help message and exit

## Commands

### `bioepic version`

Display the version of bioepic_skills.

```bash
bioepic version
```

**Output:**
```
BioEPIC Skills version 0.2.0
```

---

### `bioepic ontologies`

List all available ontologies with their configurations.

```bash
bioepic ontologies
```

**Output:**
```
                              Available Ontologies                              
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID        ┃ Name                   ┃ Description            ┃ Selector             ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ bervo     │ BERVO                  │ Biofuel research terms │ bioportal:BERVO      │
│ envo      │ Environment Ontology   │ Environmental terms    │ sqlite:obo:envo      │
│ chebi     │ ChEBI                  │ Chemical entities      │ sqlite:obo:chebi     │
│ ...       │ ...                    │ ...                    │ ...                  │
└───────────┴────────────────────────┴────────────────────────┴──────────────────────┘
```

---

### `bioepic search`

Search for ontology terms matching your query.

```bash
bioepic search QUERY [OPTIONS]
```

**Arguments:**
- `QUERY`: Search term to look up (plain text)

**Options:**
- `--ontology` / `-o`: Specific ontology to search (e.g., 'bervo', 'envo', 'chebi')
- `--limit` / `-n`: Maximum number of results (default: 10)
- `--output`: Save results to JSON file
- `--verbose` / `-v`: Enable verbose logging

**Examples:**

Search BERVO for soil moisture:
```bash
bioepic search "soil moisture" --ontology bervo
```

Search all ontologies for temperature:
```bash
bioepic search "temperature" --limit 5
```

Save search results to file:
```bash
bioepic search "precipitation" --ontology bervo --output results.json
```

**Output:**
```
Searching for: soil moisture
Ontology: bervo

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Term ID       ┃ Ontology ┃ Label                  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ BERVO:0000123 │ BERVO    │ soil moisture          │
│ BERVO:0000456 │ BERVO    │ soil water content     │
└───────────────┴──────────┴────────────────────────┘

Found 2 results
```

---

### `bioepic term`

Get detailed information about a specific ontology term.

```bash
bioepic term TERM_ID [OPTIONS]
```

**Arguments:**
- `TERM_ID`: Term identifier in CURIE format (e.g., 'ENVO:00000001')

**Options:**
- `--ontology` / `-o`: Ontology containing the term
- `--output`: Save details to JSON file
- `--verbose` / `-v`: Enable verbose logging

**Examples:**

Get details for an ENVO term:
```bash
bioepic term ENVO:00000001
```

Get details with explicit ontology:
```bash
bioepic term CHEBI:17234 --ontology chebi
```

Save term details:
```bash
bioepic term ENVO:00000001 --output term_details.json
```

**Output:**
```
Retrieving details for: ENVO:00000001

╭─────────────── Term Details ───────────────╮
│ ENVO:00000001                              │
│ environmental material                     │
│                                            │
│ A portion of environmental material is a  │
│ portion of matter that is...              │
╰────────────────────────────────────────────╯

Synonyms:
  • environmental substance
  • portion of environmental material

Relationships:

  subClassOf:
    → BFO:0000040: material entity
```

---

### `bioepic ground`

Ground text terms to ontology concepts with confidence scores.

```bash
bioepic ground TERM1 [TERM2 ...] [OPTIONS]
```

**Arguments:**
- `TERM1`, `TERM2`, ...: Text terms to ground (space-separated)

**Options:**
- `--ontology` / `-o`: Target ontology (e.g., 'bervo', 'envo')
- `--threshold` / `-t`: Minimum confidence threshold 0.0-1.0 (default: 0.8)
- `--limit` / `-n`: Maximum matches per term (default: 3)
- `--output`: Save grounding results to JSON file
- `--verbose` / `-v`: Enable verbose logging

**Examples:**

Ground terms to BERVO:
```bash
bioepic ground "soil moisture" "air temperature" "precipitation" --ontology bervo
```

Ground with custom threshold:
```bash
bioepic ground "pH" "salinity" --threshold 0.9
```

Save grounding results:
```bash
bioepic ground "soil" "water" --ontology envo --output grounding.json
```

**Output:**
```
Grounding 3 terms
Target ontology: bervo
Threshold: 0.8

'soil moisture'
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Term ID       ┃ Label              ┃ Ontology ┃ Confidence ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│ BERVO:0000123 │ soil moisture      │ BERVO    │       1.00 │
│ BERVO:0000456 │ soil water content │ BERVO    │       0.90 │
└───────────────┴────────────────────┴──────────┴────────────┘

'air temperature'
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Term ID       ┃ Label              ┃ Ontology ┃ Confidence ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│ BERVO:0000789 │ air temperature    │ BERVO    │       1.00 │
│ BERVO:0001011 │ temperature        │ BERVO    │       0.90 │
└───────────────┴────────────────────┴──────────┴────────────┘
```

---

### `bioepic info`

Show information about BioEPIC Skills, OAK, and BERVO.

```bash
bioepic info
```

**Output:**

Displays formatted information including:
- Key features
- BERVO description
- Quick examples
- Documentation links

---

## Working with BERVO

BERVO (Biological and Environmental Research Variable Ontology) provides comprehensive vocabulary for environmental research, earth science, plant science, and geochemistry.

**Common BERVO Use Cases:**

1. **Find environmental variables:**
   ```bash
   bioepic search "soil moisture" --ontology bervo
   bioepic search "air temperature" --ontology bervo
   ```

2. **Ground research measurement terms:**
   ```bash
   bioepic ground "precipitation" "humidity" "wind speed" --ontology bervo
   ```

3. **Explore geochemistry terms:**
   ```bash
   bioepic search "pH" --ontology bervo
   bioepic search "salinity" --ontology bervo
   ```

4. **Look up plant science variables:**
   ```bash
   bioepic search "leaf area" --ontology bervo
   bioepic search "photosynthesis rate" --ontology bervo
   ```

---

## Tips

1. **Use quotes for multi-word terms**: 
   ```bash
   bioepic search "carbon dioxide" --ontology chebi
   ```

2. **Start broad, then narrow**:
   ```bash
   bioepic search "cellulose"           # All ontologies
   bioepic search "cellulose" -o bervo  # Specific to BERVO
   ```

3. **Save results for later analysis**:
   ```bash
   bioepic ground term1 term2 term3 --output results.json
   ```

4. **Use verbose mode for debugging**:
   ```bash
   bioepic search "glucose" -v   # INFO level
   bioepic search "glucose" -vv  # DEBUG level
   ```

5. **Adjust confidence thresholds**:
   ```bash
   bioepic ground "biomass" -t 0.95  # Stricter matching
   bioepic ground "biomass" -t 0.7   # More permissive
   ```

---

## Getting Help

For command-specific help:
```bash
bioepic search --help
bioepic term --help
bioepic ground --help
```

For general help:
```bash
bioepic --help
```

For more information about OAK:
```bash
bioepic info
```

## Installation

After installing the `bioepic_skills` package, the `bioepic` command will be available:

```bash
pip install bioepic_skills
```

Verify the installation:

```bash
bioepic --help
```

## Global Options

All commands support the following global options:

- `--verbose` / `-v`: Enable verbose logging (DEBUG level)
- `--help`: Show help message and exit

## Commands

### `bioepic version`

Display the version of bioepic_skills.

```bash
bioepic version
```

**Output:**
```
BioEPIC Skills version 0.1.0
```

---

### `bioepic info`

Show API configuration and connection information.

```bash
bioepic info
```

**Output:**
```
            BioEPIC API Configuration            
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Setting     ┃ Value                           ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Environment │ prod                            │
│ Base URL    │ https://api.bioepic.example.com │
└─────────────┴─────────────────────────────────┘
```

---

### `bioepic collections`

List all available collections in the API.

```bash
bioepic collections
```

**Options:**
- `--output PATH`: Export results to file (JSON/CSV/TSV)

**Example:**
```bash
bioepic collections --output collections.json
```

---

### `bioepic sample`

Search and retrieve sample records.

```bash
bioepic sample [OPTIONS]
```

**Options:**

- `--id TEXT`: Get a specific sample by ID
- `--filter TEXT`: Filter samples using YAML or JSON syntax
- `--limit INTEGER`: Maximum number of results per page (default: 10)
- `--all-pages`: Fetch all pages of results (not just first page)
- `--output PATH`: Export results to file (JSON/CSV/TSV)

**Examples:**

Get a specific sample by ID:
```bash
bioepic sample --id sample-12345
```

Filter samples using YAML syntax:
```bash
bioepic sample --filter "type: soil"
bioepic sample --filter "location: forest" --limit 20
```

Filter using JSON/MongoDB syntax:
```bash
bioepic sample --filter '{"depth_cm": {"$gte": 10, "$lte": 50}}'
```

Export filtered results to CSV:
```bash
bioepic sample --filter "year: 2023" --output results.csv
```

Get all pages of results:
```bash
bioepic sample --filter "type: water" --all-pages --output all_water_samples.json
```

---

### `bioepic search`

Search records by specific attribute values.

```bash
bioepic search ATTRIBUTE VALUE [OPTIONS]
```

**Arguments:**
- `ATTRIBUTE`: The attribute name to search by (e.g., "type", "location", "depth_cm")
- `VALUE`: The value to search for

**Options:**
- `--limit INTEGER`: Maximum number of results (default: 10)
- `--output PATH`: Export results to file (JSON/CSV/TSV)

**Examples:**

Search by type:
```bash
bioepic search type soil
```

Search by location with limit:
```bash
bioepic search location "Pacific Ocean" --limit 50
```

Search and export to TSV:
```bash
bioepic search year 2023 --output results.tsv
```

---

## Filter Syntax

The `--filter` option accepts two formats:

### YAML Syntax (Simple)

For basic equality filters:

```bash
bioepic sample --filter "field: value"
bioepic sample --filter "type: soil"
bioepic sample --filter "location: forest"
```

### JSON Syntax (Advanced)

For complex queries with MongoDB operators:

```bash
# Greater than or equal
bioepic sample --filter '{"depth_cm": {"$gte": 10}}'

# Range query
bioepic sample --filter '{"temperature": {"$gte": 15, "$lte": 25}}'

# In list
bioepic sample --filter '{"type": {"$in": ["soil", "sediment"]}}'

# Multiple conditions
bioepic sample --filter '{"type": "soil", "pH": {"$gte": 6.5}}'
```

**Common MongoDB Operators:**
- `$eq`: Equal to
- `$ne`: Not equal to
- `$gt`: Greater than
- `$gte`: Greater than or equal to
- `$lt`: Less than
- `$lte`: Less than or equal to
- `$in`: In array
- `$nin`: Not in array

---

## Output Formats

Results can be exported to different formats based on the file extension:

### JSON (default)

Preserves the full nested data structure:

```bash
bioepic sample --filter "type: soil" --output results.json
```

### CSV

Flattens nested data into columns suitable for spreadsheets:

```bash
bioepic sample --filter "type: soil" --output results.csv
```

Nested objects become prefixed columns:
- `location.latitude` → `location_latitude`
- `location.longitude` → `location_longitude`

Lists are joined with `|` or converted to `_count` and `_ids` columns.

### TSV (Tab-Separated Values)

Same as CSV but with tab delimiters:

```bash
bioepic sample --filter "type: soil" --output results.tsv
```

---

## Examples

### Basic Workflow

1. Check API connection:
```bash
bioepic info
```

2. View available collections:
```bash
bioepic collections
```

3. Search for samples:
```bash
bioepic sample --filter "type: soil" --limit 5
```

4. Export filtered results:
```bash
bioepic sample --filter "year: 2023" --all-pages --output samples_2023.csv
```

### Advanced Queries

Search for soil samples at specific depth range:
```bash
bioepic sample --filter '{"type": "soil", "depth_cm": {"$gte": 10, "$lte": 30}}' \
  --output soil_samples.csv
```

Find all samples from specific locations:
```bash
bioepic sample --filter '{"location": {"$in": ["forest_a", "forest_b", "forest_c"]}}' \
  --all-pages \
  --output forest_samples.json
```

### Debugging

Enable verbose logging to see detailed request/response information:

```bash
bioepic --verbose sample --id sample-12345
```

This shows:
- HTTP request details
- API endpoints being called
- Response status codes
- Detailed error messages

---

## Tips

1. **Quote filters**: Always wrap filter strings in quotes to prevent shell interpretation
   ```bash
   bioepic sample --filter "type: soil"  # Good
   bioepic sample --filter type: soil     # Bad - shell will misinterpret
   ```

2. **Use JSON for complex queries**: For anything beyond simple equality, use JSON syntax with MongoDB operators

3. **Check output before large exports**: Use `--limit` to preview results before using `--all-pages`

4. **Choose the right format**:
   - JSON: When you need full data structure or will process programmatically
   - CSV/TSV: When you'll analyze in Excel, R, or other spreadsheet tools

5. **Enable verbose mode when debugging**: The `--verbose` flag helps troubleshoot API issues

---

## Getting Help

For command-specific help:
```bash
bioepic sample --help
bioepic search --help
```

For general help:
```bash
bioepic --help
```
