import pandas as pd

def preprocess_energy_data(energy_data: pd.DataFrame) -> pd.DataFrame:
    # Remplacer les valeurs manquantes par la médiane des colonnes concernées
    energy_data['TempMax_Deg'].fillna(energy_data['TempMax_Deg'].median(), inplace=True)
    energy_data['TempMin_Deg'].fillna(energy_data['TempMin_Deg'].median(), inplace=True)
    energy_data['CloudCoverage_percent'].fillna(energy_data['CloudCoverage_percent'].median(), inplace=True)
    
    # Convertir la colonne Dayduration_hour en secondes pour faciliter l'analyse
    energy_data['Dayduration_seconds'] = pd.to_timedelta(energy_data['Dayduration_hour']).dt.total_seconds()
    
    return energy_data
