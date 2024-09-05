import pandas as pd
import os

# Définir les chemins vers les fichiers CSV
file_paths = [
    "data-collection-kedro/data/meteo/oldReg_MeteoFR_2018-01-01_2018-12-31.csv",
    "data-collection-kedro/data/meteo/oldReg_MeteoFR_2019-01-01_2019-12-31.csv",
    "data-collection-kedro/data/meteo/oldReg_MeteoFR_2020-01-01_2020-12-31.csv",
    "data-collection-kedro/data/meteo/oldReg_MeteoFR_2021-01-01_2021-01-31.csv"
]

# Liste pour stocker les DataFrames
dataframes = []

# Lire chaque fichier CSV et l'ajouter à la liste des DataFrames
for file in file_paths:
    try:
        df = pd.read_csv(file)
        dataframes.append(df)
        print(f"Fichier {file} chargé avec succès.")
    except Exception as e:
        print(f"Erreur lors du chargement du fichier {file}: {e}")

# Combiner tous les DataFrames en un seul
combined_df = pd.concat(dataframes, ignore_index=True)

# Sauvegarder le DataFrame combiné dans un nouveau fichier CSV
combined_df.to_csv("data-collection-kedro/data/combined_meteo_data.csv", index=False,sep=';')

print("Les fichiers CSV ont été fusionnés avec succès.")
