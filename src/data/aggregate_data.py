import os
import pandas as pd
from dotenv import load_dotenv

class DataAggregator:
    def __init__(self):
        # Charger les variables d'environnement depuis le fichier .env
        load_dotenv()

    def read_csv_files(self, csv_file_paths):
        data_frames = []
        for path in csv_file_paths:
            try:
                data = pd.read_csv(path, delimiter=';')  # Ajout du délimiteur ';' si nécessaire
                data_frames.append(data)
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {path} : {e}")
        return data_frames

    def aggregate_data(self, data_frames):
        try:
            combined_data = pd.concat(data_frames, ignore_index=True)
            return combined_data
        except Exception as e:
            print(f"Erreur lors de l'agrégation des données : {e}")
            return None

    def save_to_csv(self, data, output_path):
        try:
            data.to_csv(output_path, index=False, sep=';')
            print(f"Données agrégées enregistrées avec succès dans {output_path}")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des données agrégées : {e}")

if __name__ == "__main__":
    # Spécifiez les chemins de vos fichiers CSV ici
    csv_file_paths = [
        '/home/santoudllo/Downloads/prod-region-annuelle-enr-1.csv',
        '/home/santoudllo/Downloads/prod-region-annuelle-enr-2.csv'
    ]
    output_path = '/home/santoudllo/Downloads/combined_data.csv'

    # Créer une instance de DataAggregator
    aggregator = DataAggregator()

    # Lire les fichiers CSV
    data_frames = aggregator.read_csv_files(csv_file_paths)

    # Agréger les données
    combined_data = aggregator.aggregate_data(data_frames)

    # Si l'agrégation a réussi, enregistrer les données dans un fichier CSV
    if combined_data is not None:
        aggregator.save_to_csv(combined_data, output_path)
