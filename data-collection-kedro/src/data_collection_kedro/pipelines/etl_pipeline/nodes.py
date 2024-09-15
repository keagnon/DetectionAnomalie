"""
Pipeline ETL pour les données de consommation d'énergie

Ce pipeline est chargé de récupérer, nettoyer et stocker les données de consommation d'énergie
provenant de différentes sources, notamment des API et des fichiers CSV. Le pipeline réalise les tâches suivantes :

1. Récupère les données à partir de plusieurs points d'API.
2. Lit les fichiers CSV contenant des données de consommation d'énergie.
3. Nettoie et transforme les données en utilisant la logique de transformation définie dans la classe `Transform`.
4. Stocke les données nettoyées dans une base de données MongoDB.
5. Suit et enregistre l'empreinte carbone des opérations de traitement et de stockage des données à l'aide de CodeCarbon.

CodeCarbon est intégré pour surveiller la consommation énergétique et estimer l'empreinte carbone
de chaque nœud (étape de traitement) dans ce pipeline ETL, afin de garantir un traitement des données
respectueux de l'environnement.
"""


import os
import pandas as pd
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import Any, Dict, List
from codecarbon import EmissionsTracker
from .transform import Transform

log_dir = "logs/logs_etl_pipeline"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def fetch_data_from_api(api_url: str) -> pd.DataFrame:
    """
    Fetch data from the specified API URL.

    Params:
    - api_url (str): The URL of the API to fetch data from.

    Returns:
    - pd.DataFrame: DataFrame containing the fetched data.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        try:
            data = response.json()
            if "results" in data:
                return pd.DataFrame(data["results"])
            else:
                print(f"Warning: 'results' key not found in response from {api_url}")
                return pd.DataFrame()
        except ValueError:
            print(f"Error: JSON decoding failed for {api_url}")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed for {api_url} with exception {e}")
        return pd.DataFrame()


def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Read data from a CSV file.

    Params:
    - file_path (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: DataFrame containing the CSV data.
    """
    return pd.read_csv(file_path, delimiter=";", encoding="utf-8")


def store_in_mongodb(
    data: pd.DataFrame,
    db_name: str,
    collection_name: str,
    batch_size: int = 500,
    connect_timeout: int = 200000,
) -> None:
    """
    Store the cleaned data in MongoDB in batches.

    Params:
    - data (pd.DataFrame): The cleaned data to store.
    - db_name (str): The name of the MongoDB database.
    - collection_name (str): The name of the MongoDB collection.
    - batch_size (int, optional): The number of records to insert in each batch. Default is 500.
    - connect_timeout (int, optional): Connection timeout in milliseconds. Default is 200000.
    """
    load_dotenv()

    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    cluster = os.getenv("MONGODB_CLUSTER")

    mongodb_uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy&connectTimeoutMS={connect_timeout}"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            client = MongoClient(
                mongodb_uri, tls=True, tlsAllowInvalidCertificates=True
            )
            break  # Exit the loop if the connection is successful
        except Exception as e:
            print(f"Attempt {attempt + 1} to connect to MongoDB failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print("All connection attempts failed. Exiting.")
                raise e  # Raise the exception if all retries fail

    try:
        db = client[db_name]
        collection = db[collection_name]

        if isinstance(data, pd.DataFrame):
            data = data.to_dict("records")

        # Insert data in batches
        for i in range(0, len(data), batch_size):
            batch = data[i: i + batch_size]
            try:
                collection.insert_many(batch)
                print(
                    f"Batch {i // batch_size + 1} with {len(batch)} records stored successfully in {collection_name}."
                )
            except Exception as e:
                print(f"Error inserting batch {i // batch_size + 1}: {e}")

    except Exception as e:
        print(f"Error when inserting data: {e}")


def display_data(data: pd.DataFrame) -> None:
    """
    Display the first few rows of the DataFrame.

    Params:
    - data (pd.DataFrame): The data to display.
    """
    print(data.head())
    print(data.columns)


def etl_api_data(
    api_urls: List[str], db_name: str, collection_names: List[str]
) -> None:
    """
    Process multiple API URLs and store data in MongoDB.

    Params:
    - api_urls (List[str]): List of API URLs to fetch data from.
    - db_name (str): The name of the MongoDB database.
    - collection_names (List[str]): List of MongoDB collection names.
    """

    tracker = EmissionsTracker(output_dir=log_dir)  # Start tracking carbon emissions
    tracker.start()

    for api_url, collection_name in zip(api_urls, collection_names):
        raw_data = fetch_data_from_api(api_url)
        cleaned_data = Transform.clean_data(raw_data)
        display_data(cleaned_data)
        store_in_mongodb(cleaned_data, db_name, collection_name)

    tracker.stop() # Arrêter le suivi et sauvegarder les émissions


def etl_csv_data(
    file_paths: List[str], db_name: str, collection_names: List[str]
) -> None:
    """
    Process multiple CSV files and store data in MongoDB.

    Params:
    - file_paths (List[str]): List of file paths to read CSV data from.
    - db_name (str): The name of the MongoDB database.
    - collection_names (List[str]): List of MongoDB collection names.
    """

    for file_path, collection_name in zip(file_paths, collection_names):
        print(f"Processing file {file_path} for collection {collection_name}")
        raw_data = read_csv_file(file_path)
        cleaned_data = Transform.clean_data(raw_data)

        try:
            display_data(cleaned_data)
            store_in_mongodb(cleaned_data, db_name, collection_name)
        except Exception as e:
            print(f"Failed to insert data from {file_path} into {collection_name}: {e}")
