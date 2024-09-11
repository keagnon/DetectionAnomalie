# anomaly_detection_energy_mlflow.py

import os
from dotenv import load_dotenv

import pandas as pd
from sklearn.ensemble import IsolationForest
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

load_dotenv()


google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
else:
    print("Warning: GOOGLE_APPLICATION_CREDENTIALS non défini dans .env")

mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)
else:
    print("Warning: MLFLOW_TRACKING_URI non défini dans .env")

def create_mlflow_experiment(experiment_name, artifact_location, tags=None):
    """
    Créer une expérience MLflow si elle n'existe pas, sinon récupérer l'ID de l'expérience existante.
    ::params
        experiment_name: Nom de l'expérience
        artifact_location: Emplacement des artefacts
        tags: Dictionnaire de tags à ajouter à l'expérience

    """

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

def preprocess_data(file_path):
    """
    Charger et prétraiter les données du fichier CSV.
    :param file_path: Chemin du fichier CSV
    """
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce')
    df.dropna(subset=hourly_columns, inplace=True)
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)

    return df, hourly_columns

def detect_anomalies(df, hourly_columns, contamination=0.01, experiment_id=None):
    """
    Détecter les anomalies dans les données de consommation énergétique.
    ::params
        df: DataFrame contenant les données
        hourly_columns: Liste des colonnes horaires
        contamination: Taux de contamination pour Isolation Forest
        experiment_id: ID de l'expérience MLflow
    """

    data = df[hourly_columns]
    model = IsolationForest(contamination=contamination, random_state=42)

    with mlflow.start_run(run_name="IsolationForest_Anomaly_Detection_2", experiment_id=experiment_id):
        mlflow.sklearn.autolog()
        model.fit(data)
        df['anomaly'] = model.predict(data)

        #Enregistrement du modèle dans MLflow
        mlflow.log_param("contamination", contamination)
        anomalies_detected = df['anomaly'].value_counts().get(-1, 0)
        normal_data = df['anomaly'].value_counts().get(1, 0)
        mlflow.log_metric("anomalies_detected", anomalies_detected)
        mlflow.log_metric("normal_data", normal_data)

        mlflow.sklearn.log_model(model, "isolation_forest_model")

        print(f"Run ID: {mlflow.active_run().info.run_id}")
        print("Modèle enregistré dans MLflow")

    return df

def main(file_path):
    """
    Fonction principale pour la détection des anomalies dans les données de consommation énergétique.
    ::params
        file_path: Chemin du fichier CSV
    """

    df, hourly_columns = preprocess_data(file_path)
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
        return df

    df = detect_anomalies(df, hourly_columns, contamination=0.01, experiment_id=experiment_id)
    anomalies_df = df[df['anomaly'] == -1]  # Garder uniquement les anomalies

    return df

if __name__ == "__main__":
    file_path = 'tests_models/data_test/merge_courbe_mouvement.csv'
    df_with_anomalies = main(file_path)
    print(df_with_anomalies.head())
    print(df_with_anomalies['anomaly'].value_counts())