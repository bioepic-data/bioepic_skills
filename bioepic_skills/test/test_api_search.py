# -*- coding: utf-8 -*-
from bioepic_skills.api_search import APISearch
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
load_dotenv()
ENV = os.getenv("ENV", "prod")


def test_get_records():
    """
    Test the get_records method.
    """
    api_client = APISearch(collection_name="test_collection", env=ENV)
    # Update with actual test logic
    pass


def test_get_record_by_id():
    """
    Test the get_record_by_id method.
    """
    api_client = APISearch(collection_name="test_collection", env=ENV)
    # Update with actual test logic
    pass


def test_get_record_by_filter():
    """
    Test the get_record_by_filter method.
    """
    api_client = APISearch(collection_name="test_collection", env=ENV)
    # Update with actual test logic
    pass


if __name__ == "__main__":
    test_get_records()
    test_get_record_by_id()
    test_get_record_by_filter()
