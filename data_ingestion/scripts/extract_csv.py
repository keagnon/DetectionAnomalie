import os
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus

class CSVtoMongoDB:
    def __init__(self):
        # Charger les variables d'environnement depuis le fichier .env
        load_dotenv()

        # Récupérer les informations d'identification depuis les variables d'environnement

        self.username = os.getenv('MONGODB_USERNAME')
        self.password = os.getenv('MONGODB_PASSWORD')
        self.dbname = os.getenv('MONGODB_DBNAME')
        self.collection_name = os.getenv('MONGODB_COLLECTION')
        cluster = os.getenv('MONGODB_CLUSTER')

        # Construire l'URI de connexion à MongoDB Atlas

        self.mongodb_uri =  f"mongodb+srv://{self.username}:{quote_plus(self.password)}@{cluster}/?retryWrites=true&w=majority&appName=Energy"

    def read_csv(self, csv_file_path):
        try:
            data = pd.read_csv(csv_file_path, delimiter=';')  
            return data
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
            return None

    def load_data_to_mongodb(self, data):
        try:
            client = MongoClient(self.mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
            db = client[self.dbname]
            collection = db[self.collection_name]
            collection.insert_many(data.to_dict('records'))
            print(f"{len(data)} enregistrements insérés avec succès dans la collection {self.collection_name}.")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données : {e}")

# Spécifiez le chemin de votre fichier CSV ici

csv_file_path = '/home/santoudllo/Downloads/prod-region-annuelle-enr.csv'

# Créer une instance du convertisseur CSV vers MongoDB

csv_to_mongodb = CSVtoMongoDB()

# Lire le CSV

data = csv_to_mongodb.read_csv(csv_file_path)

# Si la lecture a réussi, charger les données dans MongoDB

if data is not None:
    csv_to_mongodb.load_data_to_mongodb(data)
