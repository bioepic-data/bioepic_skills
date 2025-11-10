# Data Processing

The `DataProcessing` class provides utilities for transforming and analyzing data retrieved from APIs.

## Overview

Data processing capabilities include:

- Converting data to pandas DataFrames
- Building MongoDB-style filters
- Merging and transforming data
- Extracting specific fields
- Chunking large datasets

## Converting to DataFrames

### Basic Conversion

```python
from bioepic_skills.data_processing import DataProcessing

dp = DataProcessing()

# Convert list of dictionaries to DataFrame
records = [
    {"id": "1", "name": "Sample 1", "value": 10},
    {"id": "2", "name": "Sample 2", "value": 20},
]

df = dp.convert_to_df(records)
print(df)
```

Output:
```
  id      name  value
0  1  Sample 1     10
1  2  Sample 2     20
```

### Working with API Results

```python
from bioepic_skills.api_search import APISearch

api_client = APISearch(collection_name="samples")
records = api_client.get_records(max_page_size=100)

# Convert to DataFrame for analysis
df = dp.convert_to_df(records)

# Now use pandas operations
print(df.describe())
print(df.info())
```

## Building Filters

### Regex Filters (Partial Match)

```python
# Build a filter for partial matches
filter_dict = dp.build_filter(
    {
        "name": "sample",
        "type": "biological"
    },
    exact_match=False
)

# Use with API
api_client = APISearch(collection_name="samples")
results = api_client.get_record_by_filter(filter_dict)
```

The filter will match records where:
- `name` contains "sample" (case-insensitive)
- `type` contains "biological" (case-insensitive)

### Exact Match Filters

```python
# Build a filter for exact matches
filter_dict = dp.build_filter(
    {
        "id": "sample-12345",
        "status": "active"
    },
    exact_match=True
)
```

### Special Characters in Filters

Special characters are automatically escaped:

```python
# This works correctly with special characters
filter_dict = dp.build_filter(
    {
        "title": "GC-MS (2009)",  # Parentheses will be escaped
    },
    exact_match=False
)
```

## Extracting Fields

### Extract Single Field

```python
# Extract IDs from records
ids = dp.extract_field(records, "id")
print(f"Found {len(ids)} IDs: {ids[:5]}")

# Extract names
names = dp.extract_field(records, "name")
```

### Extract Multiple Fields

```python
# Extract different fields
ids = dp.extract_field(records, "id")
names = dp.extract_field(records, "name")
values = dp.extract_field(records, "value")

# Create a new DataFrame with selected fields
import pandas as pd
df_selected = pd.DataFrame({
    "id": ids,
    "name": names,
    "value": values
})
```

## Merging Data

### Simple Merge

Merge two DataFrames on a common column:

```python
# Two DataFrames with common 'id' column
df1 = dp.convert_to_df(samples)
df2 = dp.convert_to_df(metadata)

# Merge on 'id'
merged = dp.merge_dataframes("id", df1, df2)
```

### Advanced Merge

Merge with different column names:

```python
# df1 has 'sample_id', df2 has 'id'
merged = dp.merge_df(
    df1=samples_df,
    df2=metadata_df,
    key1="sample_id",
    key2="id"
)
```

This method also:
- Automatically handles list-type columns by exploding them
- Removes duplicate rows
- Performs inner join by default

## List Operations

### Split into Chunks

```python
# Split a large list into smaller chunks
large_list = list(range(250))
chunks = dp.split_list(large_list, chunk_size=100)

print(f"Split into {len(chunks)} chunks")
# Output: Split into 3 chunks

# Process each chunk
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {len(chunk)} items")
```

Use case - batch processing:

```python
# Get a large list of IDs
all_ids = dp.extract_field(records, "id")

# Process in batches of 50
for batch in dp.split_list(all_ids, chunk_size=50):
    # Process this batch
    batch_data = api_client.get_batch_records(batch)
    # ... process batch_data
```

## Renaming Columns

```python
# Original DataFrame
df = dp.convert_to_df(records)
print(df.columns)
# Output: Index(['id', 'name', 'type'], dtype='object')

# Rename all columns
new_names = ["ID", "Sample Name", "Sample Type"]
df_renamed = dp.rename_columns(df, new_names)
print(df_renamed.columns)
# Output: Index(['ID', 'Sample Name', 'Sample Type'], dtype='object')
```

!!! warning "Column Count Must Match"
    The number of new column names must exactly match the number of columns in the DataFrame.

## Complete Workflow Example

### Data Retrieval and Processing

```python
from bioepic_skills.api_search import APISearch
from bioepic_skills.data_processing import DataProcessing
import pandas as pd

# Initialize
api_client = APISearch(collection_name="samples")
dp = DataProcessing()

# Step 1: Retrieve data with filter
filter_dict = dp.build_filter(
    {"category": "research", "status": "active"},
    exact_match=False
)

records = api_client.get_record_by_filter(
    filter=filter_dict,
    all_pages=True
)

print(f"Retrieved {len(records)} records")

# Step 2: Convert to DataFrame
df = dp.convert_to_df(records)

# Step 3: Extract and process specific fields
sample_ids = dp.extract_field(records, "id")
print(f"Sample IDs: {len(sample_ids)}")

# Step 4: Get related data
related_records = []
for chunk in dp.split_list(sample_ids, chunk_size=50):
    # Get related data for this chunk
    chunk_filter = dp.build_filter(
        {"sample_id": chunk[0]},  # Simplified example
        exact_match=True
    )
    batch = api_client.get_record_by_filter(chunk_filter)
    related_records.extend(batch)

# Step 5: Merge datasets
related_df = dp.convert_to_df(related_records)
final_df = dp.merge_df(
    df1=df,
    df2=related_df,
    key1="id",
    key2="sample_id"
)

# Step 6: Process and export
final_df["date"] = pd.to_datetime(final_df["date"])
final_df = final_df.sort_values("date")
final_df.to_csv("research_samples_processed.csv", index=False)

print(f"Exported {len(final_df)} processed records")
```

### Batch Processing Large Datasets

```python
def process_large_dataset(api_client, dp, total_records):
    """Process a large dataset in manageable chunks"""
    chunk_size = 100
    all_results = []
    
    for offset in range(0, total_records, chunk_size):
        # Get chunk
        records = api_client.get_records(
            max_page_size=chunk_size,
            # Implement pagination based on your API
        )
        
        # Process chunk
        df_chunk = dp.convert_to_df(records)
        
        # Filter and transform
        df_chunk = df_chunk[df_chunk["status"] == "active"]
        df_chunk["processed"] = True
        
        # Store results
        all_results.append(df_chunk)
        
        print(f"Processed {offset + len(records)}/{total_records}")
    
    # Combine all chunks
    final_df = pd.concat(all_results, ignore_index=True)
    return final_df
```

## Performance Tips

### 1. Use Chunking for Large Datasets

```python
# Instead of loading everything at once
big_list = range(10000)
for chunk in dp.split_list(big_list, chunk_size=100):
    # Process manageable chunks
    pass
```

### 2. Select Only Needed Fields

```python
# Get only required fields from API
records = api_client.get_records(
    max_page_size=100,
    fields="id,name,date"  # Only get what you need
)
```

### 3. Filter Early

```python
# Filter at the API level, not in pandas
filter_dict = dp.build_filter({"status": "active"})
records = api_client.get_record_by_filter(filter_dict)

# Better than:
# all_records = api_client.get_records()
# df = dp.convert_to_df(all_records)
# df = df[df["status"] == "active"]  # Slower!
```

## API Reference

For detailed API documentation, see:

- [DataProcessing API](../api/data-processing.md)
