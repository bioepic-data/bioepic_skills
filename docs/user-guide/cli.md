# Command-Line Interface

The `bioepic` command-line tool provides convenient access to the BioEPIC Skills API directly from your terminal.

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
