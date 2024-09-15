"""
Script pour la détection des anomalies dans les données de consommation énergétique à l'aide d'Isolation Forest,
avec suivi de l'empreinte carbone via CodeCarbon et enregistrement des résultats dans MLflow.

Fonctionnalités principales :
- Chargement et prétraitement des données.
- Détection des anomalies via Isolation Forest.
- Suivi des métriques et enregistrement du modèle dans MLflow.
- Suivi de l'empreinte carbone des tâches de calcul via CodeCarbon.
"""

import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import IsolationForest
from mlflow.tracking import MlflowClient
from mlflow_utils import create_mlflow_experiment, get_mlflow_experiment
from utils import configure_env_settings
from codecarbon import EmissionsTracker


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
    :params
        df: DataFrame contenant les données
        hourly_columns: Liste des colonnes horaires
        contamination: Taux de contamination pour Isolation Forest
        experiment_id: ID de l'expérience MLflow
    """
    data = df[hourly_columns]
    model = IsolationForest(contamination=0.01, random_state=42)

    with mlflow.start_run(run_name="IsolationForest_Anomaly_Detection_increase_contamination", experiment_id=experiment_id):
        mlflow.sklearn.autolog()
        model.fit(data)
        df['anomaly'] = model.predict(data)

        # Enregistrement du modèle dans MLflow
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
    :params
        file_path: Chemin du fichier CSV
    """

    log_dir = "log/log_carbon_anomalie"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    tracker = EmissionsTracker(output_dir=log_dir)

    try:
        # Démarrer le traqueur d'émissions
        tracker.start()

        # Prétraiter les données
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

        # Détecter les anomalies
        df = detect_anomalies(df, hourly_columns, contamination=0.01, experiment_id=experiment_id)
        anomalies_df = df[df['anomaly'] == -1]  # Garder uniquement les anomalies

    finally:
        emissions = tracker.stop()
        print(f"Emissions (kg CO₂eq): {emissions}")
    return df

if __name__ == "__main__":
    configure_env_settings()
    file_path = '/home/grace/Projects_training_CDI/Projet_Master2/DetectionAnomalie/ml_models/mouvements_consommation/tests_models/data_test/merge_courbe_mouvement.csv'
    df_with_anomalies = main(file_path)
    print(df_with_anomalies.head())
    print(df_with_anomalies['anomaly'].value_counts())
