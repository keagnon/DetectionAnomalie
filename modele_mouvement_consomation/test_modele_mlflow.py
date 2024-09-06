import mlflow
import pandas as pd
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer les credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
else:
    print("Warning: credential non défini dans .env")

# Configurer MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)
else:
    print("Warning: MLFLOW_TRACKING_URI non défini dans .env")

# Charger le modèle MLflow
logged_model = 'runs:/a01b4b5c87f14c55b24cd5910fc7a874/isolation_forest_model'
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Fonction de prétraitement des données
def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Supprimer les colonnes inutiles
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)
    return df, hourly_columns

# Charger et prétraiter le dataset
file_path = 'merge_courbe_mouvement.csv'
df, hourly_columns = preprocess_data(file_path)

if all(column in df.columns for column in hourly_columns):
    data = df[hourly_columns]
    df['anomaly'] = loaded_model.predict(data)
    print(df[['date', 'région', 'anomaly']])
else:
    print("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")
