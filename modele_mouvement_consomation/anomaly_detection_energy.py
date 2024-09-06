# anomaly_detection_energy_mlflow.py

import os
from dotenv import load_dotenv  # Import de dotenv pour charger les variables d'environnement

import pandas as pd
from sklearn.ensemble import IsolationForest
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer les credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
else:
    print("Warning: GOOGLE_APPLICATION_CREDENTIALS non défini dans .env")

# Configurer MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)
else:
    print("Warning: MLFLOW_TRACKING_URI non défini dans .env")

# Définir une fonction pour créer ou récupérer une expérience MLflow
def create_mlflow_experiment(experiment_name, artifact_location, tags=None):
    client = MlflowClient()
    try:
        experiment = client.get_experiment_by_name(experiment_name)
        if experiment:
            experiment_id = experiment.experiment_id
            print(f"Expérience existante trouvée : {experiment_name} (ID: {experiment_id})")
        else:
            experiment_id = client.create_experiment(
                name=experiment_name,
                artifact_location=artifact_location,
                tags=tags
            )
            print(f"Nouvelle expérience créée : {experiment_name} (ID: {experiment_id})")
    except Exception as e:
        print(f"Erreur lors de la création ou récupération de l'expérience : {e}")
        experiment_id = None
    return experiment_id

# Fonction de nettoyage et prétraitement des données
def preprocess_data(file_path):
    df = pd.read_csv(file_path)

    # Supprimer la colonne 'Unnamed' si elle existe
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Convertir la colonne 'date' en format datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Sélectionner les colonnes horaires (00:00 à 23:00) et s'assurer qu'elles sont de type float
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce')

    # Supprimer les lignes avec des valeurs manquantes dans les colonnes horaires
    df.dropna(subset=hourly_columns, inplace=True)

    # Créer une variable agrégée pour chaque jour et chaque région (moyenne des consommations horaires)
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)

    return df, hourly_columns

# Fonction de détection d'anomalies avec Isolation Forest et suivi avec MLflow
def detect_anomalies(df, hourly_columns, contamination=0.01, experiment_id=None):
    # Sélectionner les colonnes horaires pour l'entraînement
    data = df[hourly_columns]

    # Initialisation du modèle Isolation Forest
    model = IsolationForest(contamination=contamination, random_state=42)

    # Démarrage d'un run MLflow
    with mlflow.start_run(run_name="IsolationForest_Anomaly_Detection", experiment_id=experiment_id):
        # Entraînement du modèle
        model.fit(data)

        # Prédiction des anomalies
        df['anomaly'] = model.predict(data)

        # Enregistrer le modèle et les paramètres dans MLflow
        mlflow.log_param("contamination", contamination)
        anomalies_detected = df['anomaly'].value_counts().get(-1, 0)
        normal_data = df['anomaly'].value_counts().get(1, 0)
        mlflow.log_metric("anomalies_detected", anomalies_detected)
        mlflow.log_metric("normal_data", normal_data)

        # Enregistrement du modèle dans MLflow
        mlflow.sklearn.log_model(model, "isolation_forest_model")

        print(f"Run ID: {mlflow.active_run().info.run_id}")
        print("Modèle enregistré dans MLflow")

    return df

# Fonction principale qui orchestre le nettoyage, la détection d'anomalies et l'enregistrement dans MLflow
def main(file_path):
    # Prétraitement des données
    df, hourly_columns = preprocess_data(file_path)

    # Création ou récupération de l'expérience MLflow
    experiment_name = "Anomaly_Detection_model"
    artifact_location = os.getenv('MLFLOW_ARTEFACTS_LOCATION')
    tags = {"env": "dev", "version": "1.0.0"}

    if not artifact_location:
        print("Warning: MLFLOW_ARTEFACTS_LOCATION non défini dans .env")

    experiment_id = create_mlflow_experiment(
        experiment_name=experiment_name,
        artifact_location=artifact_location,
        tags=tags
    )

    if not experiment_id:
        print("Erreur : Impossible de créer ou récupérer l'expérience MLflow.")
        return df  # Retourner le DataFrame sans enregistrer les anomalies

    # Détection des anomalies avec enregistrement dans MLflow
    df = detect_anomalies(df, hourly_columns, contamination=0.01, experiment_id=experiment_id)

    # Filtrer et afficher les anomalies détectées avec date et région
    anomalies_df = df[df['anomaly'] == -1]  # Garder uniquement les anomalies

    # Retourner le DataFrame avec les anomalies détectées
    return df

if __name__ == "__main__":
    file_path = 'merge_courbe_mouvement.csv'
    df_with_anomalies = main(file_path)
    print(df_with_anomalies.head())
    print(df_with_anomalies['anomaly'].value_counts())
