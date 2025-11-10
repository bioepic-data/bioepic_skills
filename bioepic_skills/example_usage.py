# -*- coding: utf-8 -*-
from bioepic_skills.data_processing import DataProcessing
from bioepic_skills.api_search import APISearch

# Create instances of the classes
api_client = APISearch(collection_name="your_collection_name")
dp_client = DataProcessing()

# Example 1: Get records with a specific attribute
records = api_client.get_record_by_attribute(
    attribute_name="type",
    attribute_value="sample_type",
    max_page_size=100,
    fields="id,name,description",
    all_pages=True,
)

# Clarify names in the results
for record in records:
    record["record_id"] = record.pop("id")
    record["record_name"] = record.pop("name")

# Convert to DataFrame
records_df = dp_client.convert_to_df(records)
print(records_df.head())

# Example 2: Extract specific field from results
record_ids = dp_client.extract_field(records, "record_id")
print(f"Found {len(record_ids)} record IDs")

# Example 3: Build a custom filter
filter_dict = dp_client.build_filter(
    {"name": "example", "description": "test"}, 
    exact_match=False
)
filtered_records = api_client.get_record_by_filter(filter_dict)

# Example 4: Merge dataframes
if len(filtered_records) > 0:
    filtered_df = dp_client.convert_to_df(filtered_records)
    merged_df = dp_client.merge_dataframes("record_id", records_df, filtered_df)
    print(f"Merged dataframe shape: {merged_df.shape}")
