import os
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

class MongoDBClient:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('MONGODB_USERNAME')
        self.password = os.getenv('MONGODB_PASSWORD')
        self.cluster = os.getenv('MONGODB_CLUSTER')
        self.dbname = os.getenv('MONGODB_DBNAME')
        self.collection_name = os.getenv('MONGODB_COLLECTION')
        
        # Construire l'URI de connexion MongoDB
        self.uri = f"mongodb+srv://{self.username}:{self.password}@{self.cluster}/?appName=Energy"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        
        # Tester la connexion
        try:
            self.client.admin.command('ping')
            print("Ping réussi. Connexion à MongoDB réussie !")
        except Exception as e:
            print(f"Erreur de connexion à MongoDB: {e}")
            raise  
        
        self.db = self.client[self.dbname]
        self.collection = self.db[self.collection_name]

    def get_documents(self):
        return list(self.collection.find())  

    def save_to_csv(self, documents, file_name):
        try:
            # Convert to DataFrame
            df = pd.DataFrame(documents)
            # Optionally remove MongoDB's default '_id' field
            if '_id' in df.columns:
                df.drop('_id', axis=1, inplace=True)
            # Save to CSV
            df.to_csv(file_name, index=False)
            print(f"Données sauvegardées dans le fichier CSV: {file_name}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde en CSV: {e}")
            raise

if __name__ == "__main__":
    mongo_client = MongoDBClient()
    documents = mongo_client.get_documents()
    
    # Specify the CSV file name
    csv_file_name = "output_data.csv"
    
    # Save the documents to a CSV file
    mongo_client.save_to_csv(documents, csv_file_name)
