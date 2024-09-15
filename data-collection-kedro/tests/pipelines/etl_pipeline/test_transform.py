"""
This is a boilerplate test file for pipeline 'etl_pipeline'
generated using Kedro 0.19.5.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""
import pytest
import pandas as pd
from src.data_collection_kedro.pipelines.etl_pipeline.transform import Transform

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Column One': [1, 2, 3],
        'Column Two': ['A', 'B', 'C'],
        'Column One': [1, 2, 2]
    })

def test_normalize_column_names(sample_data):
    normalized_df = Transform.normalize_column_names(sample_data)
    assert all(col.islower() for col in normalized_df.columns), "Columns should be lowercased"
    assert all(" " not in col for col in normalized_df.columns), "Columns should not have spaces"

def test_remove_duplicates(sample_data):
    clean_data = Transform.remove_duplicates(sample_data)
    assert clean_data.shape[0] == 3, "Duplicate rows should be removed"

def test_clean_data(sample_data):
    clean_data = Transform.clean_data(sample_data)
    assert clean_data.shape[0] == 3, "Duplicate rows should be removed after cleaning"
    assert all(col.islower() for col in clean_data.columns), "Columns should be lowercased after cleaning"
