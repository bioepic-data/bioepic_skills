# -*- coding: utf-8 -*-
"""
Export utilities for BioEPIC Skills.

Handles exporting records to various formats (JSON, CSV, TSV) with smart handling
of nested data structures.
"""
import json
import csv
from pathlib import Path
from typing import Any, List, Dict
import logging

logger = logging.getLogger(__name__)


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Flatten a nested dictionary.
    
    Parameters
    ----------
    d : dict
        Dictionary to flatten
    parent_key : str
        Parent key name for recursion
    sep : str
        Separator for nested keys
        
    Returns
    -------
    dict
        Flattened dictionary
        
    Examples
    --------
    >>> flatten_dict({'a': 1, 'b': {'c': 2, 'd': 3}})
    {'a': 1, 'b_c': 2, 'b_d': 3}
    
    >>> flatten_dict({'lat_lon': {'latitude': 34.5, 'longitude': -118.2}})
    {'lat_lon_latitude': 34.5, 'lat_lon_longitude': -118.2}
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Handle lists by joining with | or creating count/ids columns
            if v and isinstance(v[0], dict):
                # List of dicts - create _count and _ids columns
                items.append((f"{new_key}_count", len(v)))
                if all('id' in item for item in v):
                    ids = [item['id'] for item in v]
                    items.append((f"{new_key}_ids", '|'.join(ids)))
            else:
                # Simple list - join with |
                items.append((new_key, '|'.join(str(x) for x in v) if v else ''))
        else:
            items.append((new_key, v))
    
    return dict(items)


def export_to_json(records: List[Dict], output_path: Path):
    """
    Export records to JSON file.
    
    Parameters
    ----------
    records : list[dict]
        Records to export
    output_path : Path
        Path to output file
    """
    with open(output_path, 'w') as f:
        json.dump(records, f, indent=2)


def export_to_csv(records: List[Dict], output_path: Path, delimiter: str = ','):
    """
    Export records to CSV/TSV file with flattened nested structures.
    
    Parameters
    ----------
    records : list[dict]
        Records to export
    output_path : Path
        Path to output file
    delimiter : str
        Field delimiter (default: ',')
    """
    if not records:
        # Create empty file
        output_path.touch()
        return
    
    # Flatten all records
    flattened = [flatten_dict(record) for record in records]
    
    # Get all unique field names across all records
    fieldnames = set()
    for record in flattened:
        fieldnames.update(record.keys())
    
    fieldnames = sorted(fieldnames)  # Sort for consistent column order
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(flattened)


def detect_format(output_path: Path, format_hint: str = "auto") -> str:
    """
    Detect output format from file extension or format hint.
    
    Parameters
    ----------
    output_path : Path
        Output file path
    format_hint : str
        Format hint ('auto', 'json', 'csv', 'tsv')
        
    Returns
    -------
    str
        Detected format ('json', 'csv', or 'tsv')
    """
    if format_hint != "auto":
        return format_hint.lower()
    
    # Detect from extension
    suffix = output_path.suffix.lower()
    if suffix == '.json':
        return 'json'
    elif suffix == '.csv':
        return 'csv'
    elif suffix == '.tsv':
        return 'tsv'
    else:
        # Default to JSON
        logger.warning(f"Unknown file extension '{suffix}', defaulting to JSON format")
        return 'json'


def export_records(records: List[Dict], output_path: Path, format: str = "auto"):
    """
    Export records to file in specified format.
    
    Parameters
    ----------
    records : list[dict]
        Records to export
    output_path : Path
        Path to output file
    format : str
        Format ('auto', 'json', 'csv', or 'tsv')
        
    Examples
    --------
    >>> records = [{'id': '1', 'name': 'Sample 1'}, {'id': '2', 'name': 'Sample 2'}]
    >>> export_records(records, Path('output.csv'), 'csv')  # doctest: +SKIP
    >>> export_records(records, Path('output.json'))  # doctest: +SKIP
    """
    output_path = Path(output_path).resolve()
    detected_format = detect_format(output_path, format)
    
    if detected_format == 'json':
        export_to_json(records, output_path)
    elif detected_format == 'csv':
        export_to_csv(records, output_path, delimiter=',')
    elif detected_format == 'tsv':
        export_to_csv(records, output_path, delimiter='\t')
    else:
        raise ValueError(f"Unsupported format: {detected_format}")
    
    logger.info(f"Exported {len(records)} records to {output_path}")
