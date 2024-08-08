import pandas as pd
from typing import Any

class Transform:
    @staticmethod
    def normalize_column_names(data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize column names by converting them to lower case and replacing spaces with underscores.
        
        Args:
            data (pd.DataFrame): The raw data to normalize.
        
        Returns:
            pd.DataFrame: The data with normalized column names.
        """
        data.columns = [col.lower().replace(" ", "_") for col in data.columns]
        return data
    
    @staticmethod
    def convert_dates(data: pd.DataFrame) -> pd.DataFrame:
        """
        Convert columns that are likely to be dates to datetime objects.
        
        Args:
            data (pd.DataFrame): The data containing date columns to convert.
        
        Returns:
            pd.DataFrame: The data with converted date columns.
        """
        for col in data.columns:
            try:
                data[col] = pd.to_datetime(data[col], errors='ignore')
            except (TypeError, ValueError):
                continue
        return data
    
    @staticmethod
    def fill_missing_values(data: pd.DataFrame) -> pd.DataFrame:
        """
        Fill missing values in the data with appropriate placeholders.
        
        Args:
            data (pd.DataFrame): The data with potential missing values.
        
        Returns:
            pd.DataFrame: The data with missing values filled.
        """
        for col in data.select_dtypes(include=['float64', 'int64']).columns:
            data[col].fillna(0, inplace=True)
        
        for col in data.select_dtypes(include=['object']).columns:
            data[col].fillna('', inplace=True)
        
        return data
    
    @staticmethod
    def remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate rows from the data.
        
        Args:
            data (pd.DataFrame): The data to remove duplicates from.
        
        Returns:
            pd.DataFrame: The data with duplicates removed.
        """
        data.drop_duplicates(inplace=True)
        return data
    
    @staticmethod
    def clean_data(data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and transform the data using various transformation methods.
        
        Args:
            data (pd.DataFrame): The raw data to clean.
        
        Returns:
            pd.DataFrame: The cleaned data.
        """
        data = Transform.normalize_column_names(data)
        data = Transform.convert_dates(data)
        data = Transform.fill_missing_values(data)
        data = Transform.remove_duplicates(data)
        return data
