import os
import requests
import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv

class APItoMongoDB:
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
        
        self.mongodb_uri = f"mongodb+srv://{self.username}:{quote_plus(self.password)}@{cluster}/?retryWrites=true&w=majority&appName=Energy"

    def fetch_data_from_api(self, api_url):
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()  
            return data
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête API : {e}")
            return None

    def load_data_to_mongodb(self, data):
        try:
            client = MongoClient(self.mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
            db = client[self.dbname]
            collection = db[self.collection_name]
            collection.insert_many(data)
            print(f"{len(data)} enregistrements insérés avec succès dans la collection {self.collection_name}.")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données : {e}")

# URL de l'API

api_url = ''

# Créer une instance du convertisseur API vers MongoDB

api_to_mongodb = APItoMongoDB()

# Récupérer les données de l'API

data = api_to_mongodb.fetch_data_from_api(api_url)

# Si la requête a réussi, charger les données dans MongoDB

if data is not None:
    api_to_mongodb.load_data_to_mongodb(data)
