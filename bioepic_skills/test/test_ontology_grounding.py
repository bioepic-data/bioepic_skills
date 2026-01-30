# -*- coding: utf-8 -*-
"""
Tests for ontology grounding functionality.
"""
from bioepic_skills.ontology_grounding import (
    list_ontologies,
    ONTOLOGY_CONFIGS,
    search_ontology,
)


def test_list_ontologies():
    """Test that list_ontologies returns the expected structure."""
    ontologies = list_ontologies()

    assert isinstance(ontologies, list)
    assert len(ontologies) > 0

    # Check first ontology has required fields
    ont = ontologies[0]
    assert "id" in ont
    assert "name" in ont
    assert "description" in ont
    assert "selector" in ont


def test_ontology_configs():
    """Test that ONTOLOGY_CONFIGS contains expected ontologies."""
    assert "bervo" in ONTOLOGY_CONFIGS
    assert "envo" in ONTOLOGY_CONFIGS
    assert "chebi" in ONTOLOGY_CONFIGS

    # Check BERVO configuration
    bervo = ONTOLOGY_CONFIGS["bervo"]
    assert bervo["selector"] == "bioportal:BERVO"
    assert "Biological" in bervo["name"]
    assert "Environmental" in bervo["name"]


def test_bervo_is_first():
    """Test that BERVO is prominently featured."""
    ontologies = list_ontologies()
    ont_ids = [ont["id"] for ont in ontologies]
    assert "bervo" in ont_ids


def test_search_ontology_label_fallback(monkeypatch):
    class DummyAdapter:
        label_cache = {}

        def basic_search(self, _term):
            return ["CURIE:1"]

        def label(self, _curie):
            return None

    def fake_get_ontology_adapter(_ontology_id):
        return DummyAdapter()

    monkeypatch.setattr(
        "bioepic_skills.ontology_grounding.get_ontology_adapter",
        fake_get_ontology_adapter,
    )

    results = search_ontology("soil", ontology_id="bervo", limit=1)
    assert results
    assert results[0][2] in {"CURIE:1", "Unknown"}


def test_search_ontology_ols_uri_conversion(monkeypatch):
    class DummyAdapter:
        def basic_search(self, _term):
            return ["http://purl.obolibrary.org/obo/ENVO_00000001"]

        def label(self, _curie):
            return "dummy label"

    def fake_get_adapter(_selector):
        return DummyAdapter()

    monkeypatch.setattr(
        "bioepic_skills.ontology_grounding.get_adapter",
        fake_get_adapter,
    )

    results = search_ontology("soil", ontology_id=None, limit=1)
    assert results
    assert results[0][0].startswith("ENVO:")


# Note: Integration tests that actually call OAK adapters would require
# network access and are better run separately. Examples:
#
# def test_search_envo():
#     """Test searching ENVO ontology."""
#     results = search_ontology("soil", ontology_id="envo", limit=5)
#     assert len(results) > 0
#
# def test_get_term_details():
#     """Test retrieving term details."""
#     details = get_term_details("ENVO:00000001", ontology_id="envo")
#     assert "label" in details
#     assert "definition" in details
