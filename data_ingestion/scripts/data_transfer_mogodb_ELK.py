import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

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
        return self.collection.find()

class ElasticsearchClient:
    def __init__(self):
        
        self.es = Elasticsearch(
            ['http://localhost:9200']
        )

        # Tester la connexion

        try:
            info = self.es.info()
            print(f"Connexion à Elasticsearch réussie : {info}")
        except Exception as e:
            print(f"Erreur de connexion à Elasticsearch: {e}")
            raise  

    def transform_document(self, doc):
        es_doc = doc.copy()
        es_doc.pop('_id', None)  
        return es_doc

    def index_documents(self, documents, index_name):
        actions = []
        for doc in documents:
            action = {
                "_index": index_name,
                "_id": str(doc['_id']),
                "_source": self.transform_document(doc)
            }
            actions.append(action)
        
        try:
            helpers.bulk(self.es, actions)
            print(f"{len(actions)} documents transférés avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'indexation des documents: {e}")

class DataTransfer:
    def __init__(self, mongo_client, es_client, index_name):
        self.mongo_client = mongo_client
        self.es_client = es_client
        self.index_name = index_name

    def transfer_data(self):
        try:
            documents = self.mongo_client.get_documents()
            self.es_client.index_documents(documents, self.index_name)
        except Exception as e:
            print(f"Erreur lors du transfert des données: {e}")

if __name__ == "__main__":
    mongo_client = MongoDBClient()
    es_client = ElasticsearchClient()
    index_name = "consommation"  

    data_transfer = DataTransfer(mongo_client, es_client, index_name)
    data_transfer.transfer_data()
