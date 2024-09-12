from typing import Any

import pandas as pd

# mypy: ignore-errors
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
        data = Transform.remove_duplicates(data)
        return data
