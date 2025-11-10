# Quick Start Guide

This guide will help you get started with BioEPIC Skills quickly.

## Setup

### 1. Install the Package

```bash
pip install bioepic_skills
```

### 2. Configure Environment Variables

Create a `.env` file in your project directory:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```
ENV=prod
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
```

## Basic Usage

### Simple API Query

```python
from bioepic_skills.api_search import APISearch
from bioepic_skills.data_processing import DataProcessing

# Create clients
api_client = APISearch(collection_name="samples")
dp = DataProcessing()

# Get records
records = api_client.get_records(max_page_size=10)
print(f"Retrieved {len(records)} records")

# Convert to DataFrame
df = dp.convert_to_df(records)
print(df.head())
```

### Search by Attribute

```python
# Search for specific records
results = api_client.get_record_by_attribute(
    attribute_name="type",
    attribute_value="biological_sample",
    max_page_size=50,
    all_pages=True
)

print(f"Found {len(results)} matching records")
```

### Get Record by ID

```python
# Retrieve a specific record
record = api_client.get_record_by_id("sample-12345")
print(record)
```

## Using Authentication

For endpoints that require authentication:

```python
from bioepic_skills.auth import BioEPICAuth
from bioepic_skills.api_search import APISearch
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize authentication
auth = BioEPICAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET")
)

# Verify credentials
if auth.has_credentials():
    print("Authentication configured successfully")
    
    # Get token
    token = auth.get_token()
    print("Token acquired")
```

## Data Processing Examples

### Extract Specific Fields

```python
from bioepic_skills.data_processing import DataProcessing

dp = DataProcessing()

# Extract IDs from records
ids = dp.extract_field(records, "id")
print(f"Extracted {len(ids)} IDs")
```

### Build Custom Filters

```python
# Build a MongoDB-style filter
filter_query = dp.build_filter(
    {"name": "test", "status": "active"},
    exact_match=False
)

# Use the filter in a query
filtered_records = api_client.get_record_by_filter(filter_query)
```

### Merge DataFrames

```python
# Merge two DataFrames on a common column
merged_df = dp.merge_dataframes("id", df1, df2)
print(f"Merged dataframe shape: {merged_df.shape}")
```

### Split Lists into Chunks

```python
# Split a large list into smaller chunks
large_list = list(range(250))
chunks = dp.split_list(large_list, chunk_size=100)
print(f"Split into {len(chunks)} chunks")
```

## Debugging

Enable debug logging to see detailed information:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Now run your code - you'll see detailed debug output
api_client = APISearch(collection_name="samples")
records = api_client.get_records(max_page_size=5)
```

## Common Patterns

### Pagination - Get All Pages

```python
# Get all pages of results
all_records = api_client.get_records(
    max_page_size=100,
    all_pages=True
)
print(f"Retrieved {len(all_records)} total records")
```

### Filter and Export

```python
# Filter, convert to DataFrame, and export
results = api_client.get_record_by_attribute(
    attribute_name="category",
    attribute_value="research"
)

df = dp.convert_to_df(results)
df.to_csv("research_samples.csv", index=False)
print("Data exported to research_samples.csv")
```

## Next Steps

- Explore the [User Guide](../user-guide/usage.md) for more detailed examples
- Check the [API Reference](../api/api-search.md) for complete documentation
- Learn about [Authentication](../user-guide/authentication.md) in detail
- Review [Data Processing](../user-guide/data-processing.md) capabilities
