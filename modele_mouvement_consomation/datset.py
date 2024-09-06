import pandas as pd
import numpy as np

# Exemple de régions et de dates
regions = ['Région_A', 'Région_B', 'Région_C']
dates = pd.date_range(start='2023-01-01', periods=3, freq='D')

# Générer des données aléatoires pour les colonnes horaires
data = []
for date in dates:
    for region in regions:
        row = {
            'date': date,
            'région': region,
            '00:00': np.random.uniform(2000, 5000),
            '01:00': np.random.uniform(2000, 5000),
            '02:00': np.random.uniform(2000, 5000),
            '03:00': np.random.uniform(2000, 5000),
            '04:00': np.random.uniform(2000, 5000),
            '05:00': np.random.uniform(2000, 5000),
            '06:00': np.random.uniform(2000, 5000),
            '07:00': np.random.uniform(2000, 5000),
            '08:00': np.random.uniform(2000, 5000),
            '09:00': np.random.uniform(2000, 5000),
            '10:00': np.random.uniform(2000, 5000),
            '11:00': np.random.uniform(2000, 5000),
            '12:00': np.random.uniform(2000, 5000),
            '13:00': np.random.uniform(2000, 5000),
            '14:00': np.random.uniform(2000, 5000),
            '15:00': np.random.uniform(2000, 5000),
            '16:00': np.random.uniform(2000, 5000),
            '17:00': np.random.uniform(2000, 5000),
            '18:00': np.random.uniform(2000, 5000),
            '19:00': np.random.uniform(2000, 5000),
            '20:00': np.random.uniform(2000, 5000),
            '21:00': np.random.uniform(2000, 5000),
            '22:00': np.random.uniform(2000, 5000),
            '23:00': np.random.uniform(2000, 5000)
        }
        data.append(row)

# Convertir en DataFrame
df_example_with_region = pd.DataFrame(data)

# Sauvegarder ce dataset en CSV
df_example_with_region.to_csv("dataset_with_date_region.csv", index=False,sep=';')

