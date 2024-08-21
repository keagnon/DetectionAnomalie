"""
This is a boilerplate pipeline 'data_fusion_pipeline'
generated using Kedro 0.19.5
"""
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os

def load_collections(collection_names, db_name,connect_timeout: int = 20000):
    """
    Charger les collections MongoDB spécifiées et les retourner sous forme de DataFrames.
    """
    load_dotenv()

    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')

    mongodb_uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy&connectTimeoutMS={connect_timeout}"
    client = MongoClient(mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)

    db = client[db_name]
    dataframes = []

    for name in collection_names:
        collection = db[name]
        data = pd.DataFrame(list(collection.find()))
        dataframes.append(data)
        print(f"Collection {name} loaded successfully")
        # print(data.head())
        # print(data.columns)

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

def merge_dataframes(dataframes, merge_column):
    """
    Fusionne les DataFrames sur une colonne commune.
    """
    df1 = dataframes[0]
    df2 = dataframes[1]

    # Assurez-vous que les colonnes de fusion sont au même format
    df1[merge_column] = pd.to_datetime(df1[merge_column])
    df2['période'] = pd.to_datetime(df2['période'])

    # Fusion des deux DataFrames
    merged_data = pd.merge(df1, df2, left_on=merge_column, right_on='période', how='inner')

    return merged_data


def normalize_columns(dataframes):
    """
    Normalise les colonnes avant la fusion des DataFrames.
    Renomme et convertit les colonnes de dates et de régions pour assurer la cohérence.
    """
    for i, df in enumerate(dataframes):
        if 'prevision' in df.columns:
            df.rename(columns={'prevision': 'date', 'commune': 'région'}, inplace=True)
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y - %H h', errors='coerce')
        elif 'période' in df.columns:
            df.rename(columns={'période': 'date'}, inplace=True)
            df['date'] = pd.to_datetime(df['date'], format='%d %B %Y', errors='coerce')
        elif 'date_de_fin' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['date_de_fin'] = pd.to_datetime(df['date_de_fin'], errors='coerce')
        elif 'date' in df.columns and '00:00' in df.columns:
            df['date'] = pd.to_datetime(df['date'], format='%d %B %Y', errors='coerce')
        elif 'début_rupture' in df.columns:
            df['début_rupture'] = pd.to_datetime(df['début_rupture'], format='%d %B %Y %H:%M', errors='coerce')
            df['fin_rupture'] = pd.to_datetime(df['fin_rupture'], format='%d %B %Y %H:%M', errors='coerce')
            df['date'] = df['début_rupture']

        # Remplacer NaT par une date par défaut
        df['date'].fillna(pd.Timestamp('1970-01-01'), inplace=True)

        # Afficher les lignes avec des erreurs de conversion
        if df['date'].isnull().any():
            print(f"Warning: Null values encountered in 'date' column after conversion in DataFrame {i}.")
            print(df[df['date'].isnull()])

    return dataframes

def display_dataframes(dataframes):
    """
    Affiche les premières lignes de chaque DataFrame dans la liste donnée.
    """
    for i, df in enumerate(dataframes):
        print(f"DataFrame {i+1}:")
        print(df.head())
        print("\n")

    return dataframes

def store_in_mongodb(data: pd.DataFrame, db_name: str, collection_name: str) -> None:
    """
    Store the cleaned data in MongoDB.
    """
    load_dotenv()

    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')

    mongodb_uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy"
    try:
        client = MongoClient(mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
        db = client[db_name]
        collection = db[collection_name]

        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')

        collection.insert_many(data)
        print(f"{len(data)} records stored successfully in {collection_name}.")
    except Exception as e:
        print(f"Error when inserting data: {e}")

