# Usage Guide

This guide covers common usage patterns and best practices for BioEPIC Skills.

## API Client Initialization

### Basic Initialization

```python
from bioepic_skills.api_search import APISearch

# Initialize with a collection name
api_client = APISearch(collection_name="samples")
```

### Environment Configuration

You can specify different environments (production or development):

```python
# Use production environment (default)
api_client = APISearch(collection_name="samples", env="prod")

# Use development environment
api_client = APISearch(collection_name="samples", env="dev")
```

## Querying Data

### Get Records

Retrieve records from a collection:

```python
# Get first 100 records
records = api_client.get_records(max_page_size=100)

# Get all records (with pagination)
all_records = api_client.get_records(max_page_size=100, all_pages=True)

# Get specific fields only
records = api_client.get_records(
    max_page_size=50,
    fields="id,name,description"
)
```

### Filter Records

Use MongoDB-style filters:

```python
# Simple filter
filter_str = '{"type": "sample"}'
records = api_client.get_record_by_filter(filter_str)

# Complex filter with multiple conditions
filter_str = '{"type": "sample", "status": "active"}'
records = api_client.get_record_by_filter(
    filter=filter_str,
    max_page_size=50,
    all_pages=True
)
```

### Search by Attribute

Search for records matching specific attributes:

```python
# Partial match (default)
results = api_client.get_record_by_attribute(
    attribute_name="name",
    attribute_value="test",
    exact_match=False
)

# Exact match
results = api_client.get_record_by_attribute(
    attribute_name="id",
    attribute_value="sample-12345",
    exact_match=True
)
```

### Get Single Record

Retrieve a specific record by ID:

```python
record = api_client.get_record_by_id("sample-12345")
print(f"Record name: {record['name']}")
```

## Working with Results

### Convert to DataFrame

```python
from bioepic_skills.data_processing import DataProcessing

dp = DataProcessing()

# Convert list of dicts to pandas DataFrame
df = dp.convert_to_df(records)

# View first few rows
print(df.head())

# Get summary statistics
print(df.describe())
```

### Extract Specific Fields

```python
# Extract a single field from all records
ids = dp.extract_field(records, "id")
names = dp.extract_field(records, "name")

print(f"Found {len(ids)} IDs")
```

### Process Large Datasets

```python
# Split large lists into manageable chunks
large_id_list = [...]  # Your list of IDs
chunks = dp.split_list(large_id_list, chunk_size=100)

# Process each chunk
for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i+1}/{len(chunks)}")
    # Process chunk...
```

## Building Filters

### Simple Filters

```python
# Build a regex-based filter
filter_dict = dp.build_filter(
    {"name": "sample", "type": "biological"},
    exact_match=False
)

results = api_client.get_record_by_filter(filter_dict)
```

### Exact Match Filters

```python
# Build an exact match filter
filter_dict = dp.build_filter(
    {"id": "sample-12345", "status": "active"},
    exact_match=True
)
```

## Data Transformation

### Merge DataFrames

```python
# Simple merge on a common column
merged_df = dp.merge_dataframes("id", df1, df2)

# Advanced merge with different keys
merged_df = dp.merge_df(
    df1=samples_df,
    df2=metadata_df,
    key1="sample_id",
    key2="id"
)
```

### Rename Columns

```python
# Rename all columns
new_names = ["ID", "Name", "Description"]
df_renamed = dp.rename_columns(df, new_names)
```

## Error Handling

Always include proper error handling:

```python
try:
    records = api_client.get_records(max_page_size=100)
    df = dp.convert_to_df(records)
except RuntimeError as e:
    print(f"API request failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Logging and Debugging

### Enable Debug Logging

```python
import logging

# Set logging level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Now your API calls will show detailed debug information
```

### Custom Logger

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Use in your code
logger.info("Starting data retrieval...")
records = api_client.get_records(max_page_size=100)
logger.info(f"Retrieved {len(records)} records")
```

## Best Practices

### 1. Use Environment Variables

Always store credentials in environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
```

### 2. Handle Pagination Efficiently

For large datasets:

```python
# Process data in chunks instead of loading all at once
def process_in_batches():
    page_size = 100
    records = api_client.get_records(max_page_size=page_size)
    
    while records:
        # Process current batch
        df = dp.convert_to_df(records)
        # ... do something with df
        
        # Get next batch
        # (Implementation depends on your API's pagination)
        break  # Remove this and implement proper pagination
```

### 3. Validate Data

Always validate your data:

```python
# Check for required fields
required_fields = ["id", "name", "type"]
if all(field in record for field in required_fields):
    # Process record
    pass
else:
    print("Missing required fields")
```

### 4. Cache Results

For expensive queries:

```python
import pickle

# Save results
with open("cached_results.pkl", "wb") as f:
    pickle.dump(records, f)

# Load cached results
with open("cached_results.pkl", "rb") as f:
    records = pickle.load(f)
```

## Example Workflows

### Complete Data Retrieval and Analysis

```python
from bioepic_skills.api_search import APISearch
from bioepic_skills.data_processing import DataProcessing
import pandas as pd

# Initialize
api_client = APISearch(collection_name="samples")
dp = DataProcessing()

# Retrieve data
records = api_client.get_record_by_attribute(
    attribute_name="category",
    attribute_value="research",
    all_pages=True
)

# Convert and process
df = dp.convert_to_df(records)

# Filter and transform
df_filtered = df[df["status"] == "active"]
df_filtered["date"] = pd.to_datetime(df_filtered["date"])

# Export results
df_filtered.to_csv("research_samples.csv", index=False)
print(f"Exported {len(df_filtered)} records")
```

## Next Steps

- Learn about [Authentication](authentication.md)
- Explore [Data Processing](data-processing.md) in depth
- Check the [API Reference](../api/api-search.md)
