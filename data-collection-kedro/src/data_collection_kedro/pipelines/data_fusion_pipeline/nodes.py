"""
This is a boilerplate pipeline 'data_fusion_pipeline'
generated using Kedro 0.19.5
"""
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os

def load_collections(collection_names, db_name):
    """
    Charger les collections MongoDB spécifiées et les retourner sous forme de DataFrames.
    """
    load_dotenv()

    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')

    mongodb_uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy"
    client = MongoClient(mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)

    db = client[db_name]
    dataframes = []

    for name in collection_names:
        collection = db[name]
        data = pd.DataFrame(list(collection.find()))
        dataframes.append(data)
        print(f"Collection {name} loaded successfully")
        print(data.head())
        print(data.columns)

    return dataframes


def select_columns(dataframes, columns_to_select):
    """
    Sélectionner les colonnes spécifiques pour chaque DataFrame.
    """
    selected_dataframes = []
    for df, cols in zip(dataframes, columns_to_select):
        print(f"Colonnes disponibles dans le DataFrame: {df.columns}")
        try:
            selected_dataframes.append(df[cols])
        except KeyError as e:
            print(f"Erreur lors de la sélection des colonnes: {e}")
            raise
    return selected_dataframes


def display_selected_data(dataframes):
    """
    Afficher les premières lignes des DataFrames après sélection des colonnes.
    """
    for i, df in enumerate(dataframes):
        print(f"Affichage des données sélectionnées pour la collection {i+1}:")
        print(df.head())
    return dataframes

