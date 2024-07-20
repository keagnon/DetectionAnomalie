import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations d'identification depuis les variables d'environnement

username = os.getenv('MONGODB_USERNAME')
password = os.getenv('MONGODB_PASSWORD')
cluster = os.getenv('MONGODB_CLUSTER')

# Construire l'URI de connexion à MongoDB Atlas

uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy"

# Créer un nouveau client et se connecter au serveur

client = MongoClient(uri, server_api=ServerApi('1'))

# Envoyer une commande ping pour confirmer une connexion réussie
try:
    client.admin.command('ping')
    print("Ping réussi. Connexion à MongoDB réussie !")
except Exception as e:
    print(e)
