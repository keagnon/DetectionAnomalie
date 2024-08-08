"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.5
"""
import requests
import pandas as pd
from typing import Dict, Any

def fetch_data_from_api(api_url: str) -> pd.DataFrame:
    """
    Fetch data from the specified API URL.

    Args:
        api_url (str): The URL of the API to fetch data from.

    Returns:
        pd.DataFrame: DataFrame containing the fetched data.
    """
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data['results'])

def display_data(data: pd.DataFrame) -> None:
    print(data.head())

