# -*- coding: utf-8 -*-
from bioepic_skills.api_search import APISearch
import requests
from bioepic_skills.api_base import APIBase
import logging
import json
import yaml

logger = logging.getLogger(__name__)


class Utils:
    def __init__(self):
        pass
    
    # Add utility functions here as needed


def parse_filter(filter_str: str) -> str:
    """
    Parse filter string that can be in YAML or JSON format.
    
    Supports both simple YAML key-value pairs and complex JSON with MongoDB operators.
    
    Parameters
    ----------
    filter_str : str
        Filter string in YAML or JSON format
        
    Returns
    -------
    str
        JSON string representation of the filter
        
    Examples
    --------
    >>> parse_filter('name: test')  # doctest: +SKIP
    '{"name": "test"}'
    
    >>> parse_filter('{"status": {"$eq": "active"}}')  # doctest: +SKIP
    '{"status": {"$eq": "active"}}'
    
    Raises
    ------
    ValueError
        If the filter string cannot be parsed as valid YAML or JSON
    """
    if not filter_str:
        return ""
    
    filter_str = filter_str.strip()
    
    # Try JSON first (for MongoDB-style queries)
    if filter_str.startswith('{'):
        try:
            # Validate JSON and return as-is
            parsed = json.loads(filter_str)
            return json.dumps(parsed)
        except json.JSONDecodeError as e:
            logger.debug(f"Failed to parse as JSON: {e}")
    
    # Try YAML (for simple key:value syntax)
    try:
        parsed = yaml.safe_load(filter_str)
        if isinstance(parsed, dict):
            return json.dumps(parsed)
        else:
            raise ValueError(f"YAML filter must be a dictionary, got {type(parsed).__name__}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid filter syntax: {e}")
