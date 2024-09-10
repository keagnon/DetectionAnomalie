"""
This is a boilerplate pipeline 'emissions_pipeline'
generated using Kedro 0.19.8
"""
import pandas as pd

def load_emissions_data(filepath: str) -> pd.DataFrame:
    """Load emissions data from CSV."""
    return pd.read_csv(filepath, sep=';')

def process_emissions_data(data: pd.DataFrame) -> pd.DataFrame:
    """Process the data by grouping by region and year, and summing emissions."""
    data_grouped = data.groupby(['Territoire', 'Année']).sum().reset_index()
    return data_grouped

def save_processed_data(data: pd.DataFrame, output_filepath: str) -> None:
    """Save the processed data to a CSV file."""
    data.to_csv(output_filepath, index=False)

def load_energy_data(filepath: str) -> pd.DataFrame:
    """Load energy consumption data from CSV."""
    return pd.read_csv(filepath)

def merge_datasets(emissions_data: pd.DataFrame, energy_data: pd.DataFrame) -> pd.DataFrame:
    """Merge the emissions data with energy data based on region and year."""
    # Assuming 'Territoire' from emissions corresponds to 'région' in energy_data
    merged_data = pd.merge(energy_data, emissions_data, left_on=['région', 'year'], right_on=['Territoire', 'Année'], how='left')
    return merged_data
