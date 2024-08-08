import requests
import pandas as pd
from typing import Dict, Any, List
from .transform import Transform
import json

def fetch_data_from_api(api_url: str) -> pd.DataFrame:
    """
    Fetch data from the specified API URL.

    Args:
        api_url (str): The URL of the API to fetch data from.

    Returns:
        pd.DataFrame: DataFrame containing the fetched data.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        try:
            data = response.json()
            if 'results' in data:
                return pd.DataFrame(data['results'])
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

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the CSV data.
    """
    return pd.read_csv(file_path,  delimiter=';', encoding='utf-8')

def store_in_mongodb(data: pd.DataFrame, db_name: str, collection_name: str) -> None:
    """
    Store the cleaned data in MongoDB.

    Args:
        data (pd.DataFrame): The cleaned data to store.
        db_name (str): The name of the MongoDB database.
        collection_name (str): The name of the MongoDB collection.
    """
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_many(data.to_dict('records'))
    client.close()

def display_data(data: pd.DataFrame) -> None:
    """
    Display the first few rows of the DataFrame.

    Args:
        data (pd.DataFrame): The data to display.
    """
    print(data.head())

def process_api_data(api_urls: List[str], db_name: str, collection_names: List[str]) -> None:
    """
    Process multiple API URLs and store data in MongoDB.

    Args:
        api_urls (List[str]): List of API URLs to fetch data from.
        db_name (str): The name of the MongoDB database.
        collection_names (List[str]): List of MongoDB collection names.
    """
    for api_url, collection_name in zip(api_urls, collection_names):
        raw_data = fetch_data_from_api(api_url)
        cleaned_data = Transform.clean_data(raw_data)
        display_data(cleaned_data)
        store_in_mongodb(cleaned_data, db_name, collection_name)


def process_csv_data(file_paths: List[str], db_name: str, collection_names: List[str]) -> None:
    """
    Process multiple CSV files and store data in MongoDB.

    Args:
        file_paths (List[str]): List of file paths to read CSV data from.
        db_name (str): The name of the MongoDB database.
        collection_names (List[str]): List of MongoDB collection names.
    """
    for file_path, collection_name in zip(file_paths, collection_names):
        raw_data = read_csv_file(file_path)
        if not raw_data.empty:
            cleaned_data = Transform.clean_data(raw_data)
            display_data(cleaned_data)
            store_in_mongodb(cleaned_data, db_name, collection_name)