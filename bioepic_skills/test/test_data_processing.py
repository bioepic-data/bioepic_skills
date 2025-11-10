# -*- coding: utf-8 -*-
from bioepic_skills.data_processing import DataProcessing
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)


def test_convert_to_df():
    """
    Test converting list to DataFrame.
    """
    dp = DataProcessing()
    data = [{"id": "1", "name": "test"}, {"id": "2", "name": "test2"}]
    df = dp.convert_to_df(data)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_split_list():
    """
    Test splitting a list into chunks.
    """
    dp = DataProcessing()
    data = list(range(250))
    chunks = dp.split_list(data, chunk_size=100)
    assert len(chunks) == 3
    assert len(chunks[0]) == 100
    assert len(chunks[2]) == 50


def test_build_filter():
    """
    Test building a MongoDB filter.
    """
    dp = DataProcessing()
    filter_dict = dp.build_filter({"name": "test"})
    assert '"name"' in filter_dict
    assert '"$regex"' in filter_dict


if __name__ == "__main__":
    test_convert_to_df()
    test_split_list()
    test_build_filter()
    print("All tests passed!")
