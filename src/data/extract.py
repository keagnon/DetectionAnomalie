import os
import requests
import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
from typing import List, Union

class extract:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('MONGODB_USERNAME')
        self.password = os.getenv('MONGODB_PASSWORD')
        self.dbname = os.getenv('MONGODB_DBNAME')
        self.collection_name = os.getenv('MONGODB_COLLECTION')
        self.cluster = os.getenv('MONGODB_CLUSTER')

        self.mongodb_uri = f"mongodb+srv://{self.username}:{quote_plus(self.password)}@{self.cluster}/?retryWrites=true&w=majority&appName=Energy"

    def fetch_data_from_api(self, api_url :str) -> List[dict]:
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            return data['results']
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête API : {e}")
            return None

    def read_csv(self, csv_file_path : str) -> pd.DataFrame:
        try:
            data = pd.read_csv(csv_file_path, delimiter=';')
            return data
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
            return None

    def load_data_to_mongodb(self, data: Union[List[dict], pd.DataFrame]) -> None:
        """
        Charge les données dans MongoDB.

        Cette fonction prend une liste ou un DataFrame pandas
        Puis insère les données dans une collection MongoDB.
        Si les données sont un DataFrame, elles sont converties en une liste de dictionnaires avant l'insertion.

        Param:
            data (List[dict] ou pd.DataFrame): Les données à insérer.
            Si c'est un DataFrame, chaque ligne est convertie en un dictionnaire.

        """
        try:
            client = MongoClient(self.mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
            db = client[self.dbname]
            collection = db[self.collection_name]

            if isinstance(data, pd.DataFrame):
                data = data.to_dict('records')

            collection.insert_many(data)
            print(f"{len(data)} enregistrements insérés avec succès dans la collection {self.collection_name}.")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données : {e}")

    def get_data_from_user_choice(self):

        data_source = input("Veuillez choisir le type de source de données (API ou CSV) : ")

        if data_source.lower() == "api":
            api_url = input("Veuillez entrer l'URL de l'API : ")
            data = self.fetch_data_from_api(api_url)

            # Si la requête a réussi, charger les données dans MongoDB
            if data is not None:
                self.load_data_to_mongodb(data)

        elif data_source.lower() == "csv":
            csv_file_path = input("Veuillez entrer le chemin du fichier CSV : ")
            data = self.read_csv(csv_file_path)

            # Si la lecture a réussi, charger les données dans MongoDB
            if data is not None:
                self.load_data_to_mongodb(data)

        else:
            print("Type de source de données non reconnu. Veuillez choisir entre 'API' et 'CSV'.")

extract.get_data_from_user_choice()
