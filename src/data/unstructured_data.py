import pandas as pd
import re

 

# Lecture du fichier texte
with open('consommation_energie.txt', 'r', encoding='utf-8') as file:
    
    text = file.read()

 

# Extraction des données avec des expressions régulières

total_energy = int(re.search(r'consommé un total de (\d+)', text).group(1))

electricity = int(re.search(r'consommation électrique en 2022 s\'est élevée à (\d+)', text).group(1))

gas = int(re.search(r'La consommation de gaz naturel a atteint (\d+)', text).group(1))

oil = int(re.search(r'La consommation de pétrole en 2022 était de (\d+)', text).group(1))

coal = int(re.search(r'La consommation de charbon a été de (\d+)', text).group(1))

renewables = int(re.search(r'Les énergies renouvelables ont contribué à hauteur de (\d+)', text).group(1))

 

# Création du DataFrame

data = {

    'Type d\'énergie': ['Total', 'Électricité', 'Gaz naturel', 'Pétrole', 'Charbon', 'Énergies renouvelables'],

    'Consommation (TWh)': [total_energy, electricity, gas, oil, coal, renewables],

    'Répartition (%)': ['100%', '45%', '30%', '15%', '5%', '5%'],

    'Secteur résidentiel (%)': [35, 40, 50, 15, 20, 50],

    'Secteur industriel (%)': [25, 30, 30, 20, 70, 25],

    'Secteur des transports (%)': [20, 0, 0, 60, 0, 0],

    'Secteur tertiaire (%)': [15, 20, 15, 5, 10, 15],

    'Autres usages (%)': [5, 10, 5, 0, 0, 10]

}

 

df = pd.DataFrame(data)

 

# Sauvegarde du DataFrame en fichier Excel

df.to_excel('consommation_energie_france.xlsx', index=False)

 

print("Données sauvegardées dans le fichier 'consommation_energie_france.xlsx'")