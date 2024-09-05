"""
This is a boilerplate pipeline 'etl_pipeline'
generated using Kedro 0.19.5
"""
import requests
import pandas as pd
from typing import Dict, Any, List
from .transform import Transform
from pymongo import MongoClient
import os
from dotenv import load_dotenv

def fetch_data_from_api(api_url: str) -> pd.DataFrame:
    """
    Fetch data from the specified API URL.
    Params::
          api_url: The URL of the API to fetch data from.
    Returns::
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
    Params::
          file_path : The path to the CSV file.
    Returns::
          pd.DataFrame: DataFrame containing the CSV data.
    """
    return pd.read_csv(file_path, delimiter=';', encoding='utf-8')

def store_in_mongodb(data: pd.DataFrame, db_name: str, collection_name: str, batch_size: int = 500, connect_timeout: int = 200000) -> None:
    """
    Store the cleaned data in MongoDB in batches.

    Params:
    - data: The cleaned data to store.
    - db_name: The name of the MongoDB database.
    - collection_name: The name of the MongoDB collection.
    - batch_size: The number of records to insert in each batch.
    - connect_timeout: Connection timeout in milliseconds.
    """
    load_dotenv()

    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')

    mongodb_uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy&connectTimeoutMS={connect_timeout}"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            client = MongoClient(mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
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
            data = data.to_dict('records')

        # Insert data in batches
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            try:
                collection.insert_many(batch)
                print(f"Batch {i//batch_size + 1} with {len(batch)} records stored successfully in {collection_name}.")
            except Exception as e:
                print(f"Error inserting batch {i//batch_size + 1}: {e}")
                # Optionally, retry the insertion or handle the failure

    except Exception as e:
        print(f"Error when inserting data: {e}")

def display_data(data: pd.DataFrame) -> None:
    """
    Display the first few rows of the DataFrame.
    params::
          data (pd.DataFrame): The data to display.
    """
    print(data.head())
    print(data.columns)

def etl_api_data(api_urls: List[str], db_name: str, collection_names: List[str]) -> None:
    """
    Process multiple API URLs and store data in MongoDB.
    Params::
          api_urls: List of API URLs to fetch data from.
          db_name: The name of the MongoDB database.
          collection_names: List of MongoDB collection names.
    """

    for api_url, collection_name in zip(api_urls, collection_names):
        raw_data = fetch_data_from_api(api_url)
        cleaned_data = Transform.clean_data(raw_data)
        display_data(cleaned_data)
        store_in_mongodb(cleaned_data, db_name, collection_name)

def etl_csv_data(file_paths: List[str], db_name: str, collection_names: List[str]) -> None:
    """
    Process multiple CSV files and store data in MongoDB.
    params::
          file_paths: List of file paths to read CSV data from.
          db_name: The name of the MongoDB database.
          collection_names: List of MongoDB collection names.
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

