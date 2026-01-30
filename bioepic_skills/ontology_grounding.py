# -*- coding: utf-8 -*-
"""
Ontology grounding utilities using the Ontology Access Kit (OAK).

This module provides functions for searching ontologies, retrieving term details,
and grounding text terms to ontology concepts, with special support for BERVO
(Biofuel and Biobased Ecomanufacturing Research Vocabulary Ontology).
"""
import logging
import re
from typing import Optional
import urllib.error

from oaklib import get_adapter
from oaklib.interfaces import OboGraphInterface

logger = logging.getLogger(__name__)


def _uri_to_curie(uri: str) -> str | None:
    """Convert a full URI to a CURIE if it matches known patterns.

    Handles URIs like:
      https://w3id.org/bervo/BERVO_8000100 -> BERVO:8000100
      http://purl.obolibrary.org/obo/ENVO_00000001 -> ENVO:00000001
    """
    # w3id.org pattern: https://w3id.org/<ontology>/<PREFIX>_<id>
    m = re.match(r'https?://w3id\.org/\w+/([A-Za-z]+)_([A-Za-z0-9]+)$', uri)
    if m:
        return f"{m.group(1)}:{m.group(2)}"
    # OBO pattern: http://purl.obolibrary.org/obo/<PREFIX>_<id>
    m = re.match(r'https?://purl\.obolibrary\.org/obo/([A-Za-z]+)_([A-Za-z0-9]+)$', uri)
    if m:
        return f"{m.group(1)}:{m.group(2)}"
    return None


# Common ontology configurations
ONTOLOGY_CONFIGS = {
    "bervo": {
        "selector": "bioportal:BERVO",
        "name": "Biological and Environmental Research Variable Ontology",
        "description": "BERVO models experimental variables, conditions, and concepts in environmental research, earth science, plant science, and geochemistry",
    },
    "envo": {
        "selector": "sqlite:obo:envo",
        "name": "Environment Ontology",
        "description": "ENVO covers environmental entities and processes",
    },
    "chebi": {
        "selector": "sqlite:obo:chebi",
        "name": "Chemical Entities of Biological Interest",
        "description": "CHEBI covers chemical compounds and molecular entities",
    },
    "ncbitaxon": {
        "selector": "sqlite:obo:ncbitaxon",
        "name": "NCBI Taxonomy",
        "description": "Taxonomy database from NCBI",
    },
    "como": {
        "selector": "bioportal:COMO",
        "name": "Context and Measurement Ontology",
        "description": "COMO provides terms for describing experimental data in environmental microbiology",
    },
    "po": {
        "selector": "sqlite:obo:po",
        "name": "Plant Ontology",
        "description": "PO covers plant anatomy, morphology, and developmental stages",
    },
    "mixs": {
        "selector": "bioportal:MIXS",
        "name": "Minimal Information about any Sequence",
        "description": "MIXS provides standards for describing genomic and metagenomic sequences",
    },
}


def get_ontology_adapter(ontology_id: str) -> Optional[OboGraphInterface]:
    """
    Get an OAK adapter for the specified ontology.
    
    Parameters
    ----------
    ontology_id : str
        Ontology identifier (e.g., 'bervo', 'envo', 'chebi')
        Can also be a full selector string (e.g., 'sqlite:obo:envo')
        
    Returns
    -------
    OboGraphInterface or None
        OAK adapter instance, or None if unavailable
        
    Examples
    --------
    >>> adapter = get_ontology_adapter("envo")  # doctest: +SKIP
    >>> adapter = get_ontology_adapter("bioportal:BERVO")  # doctest: +SKIP
    """
    # If it's a known ontology ID, use the config
    if ontology_id.lower() in ONTOLOGY_CONFIGS:
        selector = ONTOLOGY_CONFIGS[ontology_id.lower()]["selector"]
    else:
        # Assume it's a direct selector string
        selector = ontology_id
    
    try:
        adapter = get_adapter(selector)
        return adapter
    except (ValueError, urllib.error.URLError) as e:
        logger.error(f"Failed to get adapter for {selector}: {e}")
        return None


def search_ontology(
    search_term: str,
    ontology_id: str | None = None,
    limit: int = 10
) -> list[tuple[str, str, str]]:
    """
    Search for ontology terms.
    
    The search_term should be a plain text term that is matched against
    ontology term labels, synonyms, and other text metadata.
    
    Parameters
    ----------
    search_term : str
        Plain text search term
    ontology_id : str or None
        Ontology identifier (e.g., 'bervo', 'envo', 'chebi')
        If None, searches OLS across multiple ontologies
    limit : int
        Maximum number of results to return (default: 10)
        
    Returns
    -------
    list[tuple[str, str, str]]
        List of tuples containing (term_id, ontology_id, label)
        
    Examples
    --------
    >>> results = search_ontology("soil pH", "bervo")  # doctest: +SKIP
    >>> for term_id, ont_id, label in results:  # doctest: +SKIP
    ...     print(f"{term_id} [{ont_id}] {label}")
    
    >>> results = search_ontology("temperature")  # Search all ontologies  # doctest: +SKIP
    """
    try:
        if ontology_id:
            # Search specific ontology
            adapter = get_ontology_adapter(ontology_id)
            if adapter is None:
                return []
            
            # Use basic_search for simple term matching
            results = []
            for curie in adapter.basic_search(search_term):
                # BioPortal may return full URIs instead of CURIEs.
                # Try to convert to CURIE and retrieve the label safely.
                display_id = curie
                if hasattr(adapter, '_converter'):
                    compressed = adapter._converter.compress(curie)
                    if compressed:
                        display_id = compressed
                if display_id == curie:
                    # Converter didn't help; try known URI patterns
                    converted = _uri_to_curie(curie)
                    if converted:
                        display_id = converted

                try:
                    label = adapter.label(curie)
                except Exception as e:
                    logger.debug(f"Could not fetch label for {curie}: {e}")
                    # Fall back to the label cache if available
                    label = getattr(adapter, 'label_cache', {}).get(curie)
                if label is None:
                    label = display_id

                # Extract ontology prefix from CURIE
                ontology_prefix = display_id.split(":")[0] if ":" in display_id else ontology_id
                results.append((display_id, ontology_prefix, label))
                if len(results) >= limit:
                    break
            return results
        else:
            # Search across ontologies using OLS
            adapter = get_adapter("ols:")
            results = []
            for curie in adapter.basic_search(search_term):
                display_id = curie
                if hasattr(adapter, '_converter'):
                    compressed = adapter._converter.compress(curie)
                    if compressed:
                        display_id = compressed
                if display_id == curie:
                    converted = _uri_to_curie(curie)
                    if converted:
                        display_id = converted

                try:
                    label = adapter.label(curie)
                except Exception as e:
                    logger.debug(f"Could not fetch label for {curie}: {e}")
                    label = getattr(adapter, 'label_cache', {}).get(curie)
                if label is None:
                    label = display_id

                ontology_prefix = display_id.split(":")[0] if ":" in display_id else "unknown"
                results.append((display_id, ontology_prefix, label))
                if len(results) >= limit:
                    break
            return results
            
    except (ValueError, urllib.error.URLError, NotImplementedError) as e:
        logger.error(f"Search failed for '{search_term}': {e}")
        return []


def get_term_details(term_id: str, ontology_id: str | None = None) -> dict:
    """
    Get detailed information about a specific ontology term.
    
    Parameters
    ----------
    term_id : str
        Term identifier (CURIE format, e.g., 'ENVO:00000001')
    ontology_id : str or None
        Ontology identifier (e.g., 'bervo', 'envo')
        If None, attempts to infer from term_id prefix
        
    Returns
    -------
    dict
        Dictionary with keys: term_id, label, definition, synonyms, ontology_id
        Returns dict with 'error' key if term not found
        
    Examples
    --------
    >>> details = get_term_details("ENVO:00000001", "envo")  # doctest: +SKIP
    >>> print(details['label'])  # doctest: +SKIP
    >>> print(details['definition'])  # doctest: +SKIP
    """
    try:
        # Infer ontology from term_id if not provided
        if ontology_id is None and ":" in term_id:
            ontology_prefix = term_id.split(":")[0].lower()
            ontology_id = ontology_prefix
        
        if ontology_id is None:
            return {"error": "Cannot determine ontology for term"}
        
        adapter = get_ontology_adapter(ontology_id)
        if adapter is None:
            return {"error": f"Cannot access ontology: {ontology_id}"}
        
        # Get basic information
        label = adapter.label(term_id)
        if label is None:
            return {"error": f"Term '{term_id}' not found or does not exist"}
        
        definition = adapter.definition(term_id)
        
        # Get synonyms
        synonyms = []
        try:
            synonyms = list(adapter.entity_aliases(term_id))
        except (NotImplementedError, AttributeError):
            # Some adapters don't support aliases
            pass
        
        # Get relationships
        relationships = {}
        try:
            rel_map = adapter.outgoing_relationship_map(term_id)
            for rel, fillers in rel_map.items():
                rel_label = adapter.label(rel) or rel
                relationships[rel_label] = [
                    {
                        "id": filler,
                        "label": adapter.label(filler)
                    }
                    for filler in fillers
                ]
        except (NotImplementedError, AttributeError):
            pass
        
        ontology_prefix = term_id.split(":")[0] if ":" in term_id else "unknown"
        
        return {
            "term_id": term_id,
            "label": label,
            "definition": definition,
            "synonyms": synonyms,
            "relationships": relationships,
            "ontology_id": ontology_prefix,
        }
        
    except (ValueError, urllib.error.URLError) as e:
        logger.error(f"Unable to get term details for '{term_id}': {e}")
        return {"error": str(e)}


def ground_terms(
    text_terms: list[str],
    ontology_id: str | None = None,
    threshold: float = 0.8,
    limit_per_term: int = 3
) -> dict[str, list[dict]]:
    """
    Ground multiple text terms to ontology concepts.
    
    This function searches for ontology terms matching the input text
    and returns the best matches with confidence scores.
    
    Parameters
    ----------
    text_terms : list[str]
        List of text terms to ground
    ontology_id : str or None
        Target ontology (e.g., 'bervo', 'envo')
        If None, searches across ontologies
    threshold : float
        Minimum confidence threshold (0.0-1.0)
    limit_per_term : int
        Maximum matches per term (default: 3)
        
    Returns
    -------
    dict[str, list[dict]]
        Dictionary mapping each input term to list of matches
        Each match contains: term_id, label, confidence, ontology_id
        
    Examples
    --------
    >>> terms = ["soil moisture", "air temperature", "precipitation"]  # doctest: +SKIP
    >>> results = ground_terms(terms, "bervo")  # doctest: +SKIP
    >>> for term, matches in results.items():  # doctest: +SKIP
    ...     print(f"{term}:")
    ...     for match in matches:
    ...         print(f"  {match['term_id']}: {match['label']} ({match['confidence']})")
    """
    results = {}
    
    for text_term in text_terms:
        matches = []
        search_results = search_ontology(text_term, ontology_id, limit=limit_per_term * 2)
        
        for term_id, ont_id, label in search_results:
            # Calculate simple confidence based on text similarity
            # Exact match = 1.0, contains = 0.9, found = 0.7
            text_lower = text_term.lower()
            label_lower = label.lower() if label else ""
            
            if text_lower == label_lower:
                confidence = 1.0
            elif text_lower in label_lower or label_lower in text_lower:
                confidence = 0.9
            else:
                confidence = 0.7
            
            if confidence >= threshold:
                matches.append({
                    "term_id": term_id,
                    "label": label,
                    "confidence": confidence,
                    "ontology_id": ont_id,
                })
            
            if len(matches) >= limit_per_term:
                break
        
        results[text_term] = matches
    
    return results


def list_ontologies() -> list[dict]:
    """
    List available ontologies with their configurations.
    
    Returns
    -------
    list[dict]
        List of dictionaries with ontology information
        
    Examples
    --------
    >>> ontologies = list_ontologies()  # doctest: +SKIP
    >>> for ont in ontologies:  # doctest: +SKIP
    ...     print(f"{ont['id']}: {ont['name']}")
    """
    return [
        {
            "id": ont_id,
            "name": config["name"],
            "description": config["description"],
            "selector": config["selector"],
        }
        for ont_id, config in ONTOLOGY_CONFIGS.items()
    ]
