import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('MONGODB_USERNAME')
password = os.getenv('MONGODB_PASSWORD')
cluster = os.getenv('MONGODB_CLUSTER')

uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Ping réussi. Connexion à MongoDB réussie !")
except Exception as e:
    print(e)
