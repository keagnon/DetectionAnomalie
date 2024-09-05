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


@patch('pymongo.MongoClient')
def test_load_collections(mock_mongo_client):
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_collection.find.return_value = [{"col1": 1, "col2": 2}]

    mock_db.__getitem__.return_value = mock_collection
    mock_mongo_client.return_value.__getitem__.return_value = mock_db

    collection_names = ["test_collection"]
    db_name = "test_db"

    result = load_collections(collection_names, db_name)

    assert isinstance(result[0], pd.DataFrame)
    assert len(result[0]) == 0

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

@patch("elasticsearch.Elasticsearch.ping", return_value=True)
@patch("elasticsearch.helpers.bulk")
@patch("elasticsearch.Elasticsearch")
def test_merge_data_store_in_elastic(mock_es, mock_bulk, mock_ping):
    # Mock DataFrames
    df_meteo = pd.DataFrame({
        "date": ["2021-01-01"],
        "région": ["alsace"],
        "TempMax_Deg": [None],  # Valeur NaN à remplacer
        "TempMin_Deg": [None],  # Valeur NaN à remplacer
        "CloudCoverage_percent": [None]  # Valeur NaN à remplacer
    })

    df_courbe = pd.DataFrame({
        "date": ["2021-01-01"],
        "région": ["alsace"],
        "00:00": [100]
    })

    df_mouvement = pd.DataFrame({
        "date": ["2021-01-01"],
        "motif": [None]  # Valeur NaN à remplacer
    })

    dataframes = [df_meteo, df_courbe, df_mouvement]

    # Appeler la fonction de fusion et de stockage
    merge_meteo_courbe, merge_courbe_mouvement = merge_data_store_in_elastic(dataframes)

    # Vérifier que les colonnes NaN ont bien été remplacées dans merge_meteo_courbe
    assert merge_meteo_courbe["TempMax_Deg"].iloc[0] == 0
    assert merge_meteo_courbe["TempMin_Deg"].iloc[0] == 0
    assert merge_meteo_courbe["CloudCoverage_percent"].iloc[0] == 0

    # Vérifier que la colonne NaN 'motif' a bien été remplacée dans merge_courbe_mouvement
    assert merge_courbe_mouvement["motif"].iloc[0] == "inconnu"

    # Vérifier que la méthode bulk a été appelée
    assert mock_bulk.called

    # Vérifier que la longueur des DataFrames fusionnés est correcte
    assert len(merge_meteo_courbe) == 1
    assert len(merge_courbe_mouvement) == 1

