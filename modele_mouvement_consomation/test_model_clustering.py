import mlflow
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer les credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials

# Configurer MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)
else:
    print("Warning: MLFLOW_TRACKING_URI non défini dans .env")

# Charger le modèle DBSCAN depuis MLflow
logged_model = 'runs:/faeb99c10bb64fe2880f5d867d8b3cda/dbscan_model'
loaded_model = mlflow.sklearn.load_model(logged_model)

# Fonction de prétraitement des données
def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Colonnes horaires (00:00 à 23:00)
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    
    # Créer une variable de consommation moyenne par jour
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)
    
    return df, hourly_columns

# Charger et prétraiter le fichier de données 'merge_fusion_mouvement.csv'
file_path = 'merge_courbe_mouvement.csv'
df, hourly_columns = preprocess_data(file_path)

# Assurez-vous que toutes les colonnes horaires existent dans le DataFrame
if all(column in df.columns for column in hourly_columns):
    # Préparer les données pour la prédiction
    scaler = StandardScaler()
    X = scaler.fit_transform(df[hourly_columns])

    # Faire une prédiction avec le modèle chargé (DBSCAN)
    df['cluster'] = loaded_model.fit_predict(X)

    # Afficher les résultats : les clusters et les points marqués comme "bruit" (cluster -1)
    print("\nRésultats du clustering DBSCAN :")
    print(df[['date', 'région', 'cluster']].head())  # Afficher les premières lignes avec les clusters
    print(f"\nNombre de clusters détectés : {len(set(df['cluster']) - {-1})}")
    print(f"Proportion de bruit (outliers) : {df['cluster'].value_counts().get(-1, 0) / len(df) * 100:.2f}%")

else:
    print("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")
