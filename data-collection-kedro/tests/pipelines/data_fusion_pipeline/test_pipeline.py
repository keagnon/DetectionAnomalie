"""
This is a boilerplate test file for pipeline 'data_fusion_pipeline'
generated using Kedro 0.19.5.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.data_collection_kedro.pipelines.data_fusion_pipeline.nodes import load_collections, select_columns
from src.data_collection_kedro.pipelines.data_fusion_pipeline.nodes import normalize_columns,display_dataframes
from src.data_collection_kedro.pipelines.data_fusion_pipeline.nodes import store_in_elasticsearch, create_index, merge_data_store_in_elastic


def test_select_columns():
    df1 = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df2 = pd.DataFrame({"colA": [5, 6], "colB": [7, 8]})

    dataframes = [df1, df2]
    columns_to_select = [["col1"], ["colA"]]

    selected_dfs = select_columns(dataframes, columns_to_select)

    assert len(selected_dfs) == 2
    assert list(selected_dfs[0].columns) == ["col1"]
    assert list(selected_dfs[1].columns) == ["colA"]

def test_normalize_columns():
    df = pd.DataFrame({
        "date": ["2021-01-01", "2021-01-02"],
        "TempMax_Deg": [20, 22],
        "region": ["alsace", "lorraine"]
    })

    dataframes = [df]

    result = normalize_columns(dataframes)

    assert "région" in result[0].columns
    assert result[0]["région"].iloc[0] == "grand est"

@patch('elasticsearch.helpers.bulk')
def test_store_in_elasticsearch(mock_bulk):
    es = MagicMock()
    df = pd.DataFrame({
        "col1": [1, 2],
        "col2": [3, 4]
    })

    store_in_elasticsearch(df, es, "test_index")

    assert mock_bulk.called
