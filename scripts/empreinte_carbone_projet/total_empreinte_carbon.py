"""
Script pour calculer l'empreinte carbone totale d'un projet à partir de plusieurs fichiers d'émissions.

Ce script lit plusieurs fichiers CSV contenant des émissions carbone pour différentes parties d'un projet
et calcule l'empreinte carbone totale du projet. Chaque fichier peut contenir plusieurs runs, et l'utilisateur
peut choisir de soit :
1. Utiliser uniquement le dernier run de chaque fichier (par défaut).
2. Utiliser tous les runs de chaque fichier et les additionner.

Retour :
L'empreinte carbone totale est affichée en kgCO2eq.

"""

import pandas as pd
import os

csv_files = [
    'scripts/empreinte_carbone_projet/emissions/emissions_catboosting.csv',
    'scripts/empreinte_carbone_projet/emissions/emissions_data_fusion_pipeline.csv',
    'scripts/empreinte_carbone_projet/emissions/emissions_dbscan.csv',
    'scripts/empreinte_carbone_projet/emissions/emissions_etl_pipeline.csv',
    'scripts/empreinte_carbone_projet/emissions/emissions_isolationforest.csv',
    'scripts/empreinte_carbone_projet/emissions/emissions_random_forest.csv',
    'scripts/empreinte_carbone_projet/emissions/emissions_ridge_model.csv'
]

def calculate_total_emissions(files, use_last_run=True):
    """
    Calcule l'empreinte carbone totale d'un projet à partir de plusieurs fichiers d'émissions.
    ::params:
        files : Liste des fichiers CSV contenant les émissions carbone.
        use_last_run : Booléen pour indiquer si on doit utiliser uniquement le dernier run de chaque fichier.
    """

    total_emissions = 0.0

    for file in files:
        df = pd.read_csv(file)

        # Vérifier que la colonne des émissions carbone existe
        if 'emissions' in df.columns:
            if use_last_run:
                # Utiliser le dernier run (dernière ligne)
                last_emission = df['emissions'].iloc[-1]
                total_emissions += last_emission
                print(f"{file}: Dernier run: {last_emission} kgCO2eq")
            else:
                # Utiliser tous les runs et les sommer
                sum_emissions = df['emissions'].sum()
                total_emissions += sum_emissions
                print(f"{file}: Somme de tous les runs: {sum_emissions} kgCO2eq")
        else:
            print(f"Le fichier {file} ne contient pas de colonne 'emissions'.")

    return total_emissions

total_emissions = calculate_total_emissions(csv_files, use_last_run=True)

print(f"\nEmpreinte carbone totale du projet: {total_emissions:.5f} kgCO2eq")
