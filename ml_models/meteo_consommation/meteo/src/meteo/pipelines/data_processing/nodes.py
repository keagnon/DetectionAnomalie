import pandas as pd

def preprocess_energy_data(energy_data: pd.DataFrame) -> pd.DataFrame:
    """
    Prétraite les données énergétiques fournies en effectuant les opérations suivantes :
    
    1. Remplace les valeurs manquantes dans les colonnes `TempMax_Deg`, `TempMin_Deg` et 
       `CloudCoverage_percent` par la médiane de chaque colonne respective.
    2. Convertit la colonne `Dayduration_hour` en secondes et crée une nouvelle colonne 
       `Dayduration_seconds` pour stocker cette valeur.

    Args:
        energy_data (pd.DataFrame): Un DataFrame contenant les données énergétiques, 
        incluant les colonnes 'TempMax_Deg', 'TempMin_Deg', 'CloudCoverage_percent', et 'Dayduration_hour'.

    Returns:
        pd.DataFrame: Le DataFrame prétraité avec les valeurs manquantes remplies et la colonne 
        `Dayduration_seconds` ajoutée.
    """
    
    # Remplacer les valeurs manquantes par la médiane des colonnes concernées
    energy_data['TempMax_Deg'].fillna(energy_data['TempMax_Deg'].median(), inplace=True)
    energy_data['TempMin_Deg'].fillna(energy_data['TempMin_Deg'].median(), inplace=True)
    energy_data['CloudCoverage_percent'].fillna(energy_data['CloudCoverage_percent'].median(), inplace=True)
    
    # Convertir la colonne Dayduration_hour en secondes pour faciliter l'analyse
    energy_data['Dayduration_seconds'] = pd.to_timedelta(energy_data['Dayduration_hour']).dt.total_seconds()
    
    return energy_data
