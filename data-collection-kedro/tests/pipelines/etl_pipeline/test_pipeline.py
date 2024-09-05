"""
This is a boilerplate test file for pipeline 'etl_pipeline'
generated using Kedro 0.19.5.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""
import pytest
import requests
from unittest.mock import patch,MagicMock
import pandas as pd
from src.data_collection_kedro.pipelines.etl_pipeline.nodes import fetch_data_from_api, read_csv_file, store_in_mongodb, display_data,etl_api_data,etl_csv_data

# Mock pour l'API
@patch('requests.get')
def test_fetch_data_from_api(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {'results': [{'col1': 1, 'col2': 2}]}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = fetch_data_from_api('http://fakeapi.com')
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 2), "Should have fetched one row and two columns"


@patch("requests.get")
def test_fetch_data_from_api_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"results": [{"col1": 1, "col2": 2}]}

    df = fetch_data_from_api("http://fakeapi.com")

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 2)

@patch("requests.get")
def test_fetch_data_from_api_no_results(mock_get):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}

    df = fetch_data_from_api("http://fakeapi.com")

    assert isinstance(df, pd.DataFrame)
    assert df.empty

@patch("requests.get")
def test_fetch_data_from_api_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("API failure")

    df = fetch_data_from_api("http://fakeapi.com")

    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_read_csv_file(tmpdir):
    csv_file = tmpdir.join("test.csv")
    csv_file.write("col1;col2\n1;A\n2;B")

    df = read_csv_file(str(csv_file))

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)

@patch("builtins.print")
def test_display_data(mock_print):
    data = pd.DataFrame({
        "col1": [1, 2],
        "col2": ["A", "B"]
    })

    display_data(data)

    assert mock_print.call_count == 2

@patch("src.data_collection_kedro.pipelines.etl_pipeline.nodes.fetch_data_from_api")
@patch("src.data_collection_kedro.pipelines.etl_pipeline.nodes.store_in_mongodb")
@patch("src.data_collection_kedro.pipelines.etl_pipeline.nodes.display_data")
def test_etl_api_data(mock_display, mock_store, mock_fetch):
    mock_fetch.return_value = pd.DataFrame({
        "col1": [1, 2],
        "col2": ["A", "B"]
    })

    etl_api_data(["http://fakeapi.com"], "test_db", ["test_collection"])

    mock_fetch.assert_called_once_with("http://fakeapi.com")
    mock_display.assert_called_once()
    mock_store.assert_called_once()

@patch("src.data_collection_kedro.pipelines.etl_pipeline.nodes.read_csv_file")
@patch("src.data_collection_kedro.pipelines.etl_pipeline.nodes.store_in_mongodb")
@patch("src.data_collection_kedro.pipelines.etl_pipeline.nodes.display_data")
def test_etl_csv_data(mock_display, mock_store, mock_read):
    mock_read.return_value = pd.DataFrame({
        "col1": [1, 2],
        "col2": ["A", "B"]
    })

    etl_csv_data(["/path/to/file.csv"], "test_db", ["test_collection"])

    mock_read.assert_called_once_with("/path/to/file.csv")
    mock_display.assert_called_once()
    mock_store.assert_called_once()