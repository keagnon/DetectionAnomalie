"""
Ce script entraîne deux modèles (Ridge et Random Forest) pour la prédiction de la consommation énergétique
en fonction de caractéristiques telles que les mouvements sociaux et les données temporelles.
Les résultats sont enregistrés dans MLflow, avec un suivi de l'empreinte carbone via CodeCarbon.

Étapes principales :
1. Prétraitement des données et encodage des variables catégorielles.
2. Entraînement des modèles Ridge et Random Forest, avec optimisation des hyperparamètres pour Ridge.
3. Suivi des émissions de carbone pendant l'entraînement.
4. Enregistrement des modèles et des métriques dans MLflow et Google Cloud Storage (GCS).

Variables d'environnement :
- GOOGLE_APPLICATION_CREDENTIALS : Chemin vers les clés d'authentification Google Cloud.
- MLFLOW_TRACKING_URI : URI du serveur MLflow.
- MLFLOW_ARTEFACTS_LOCATION : Emplacement des artefacts MLflow dans GCS.
"""


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import mlflow
import mlflow.sklearn
from google.cloud import storage
from dotenv import load_dotenv
import os
import shutil
from mlflow.tracking import MlflowClient
from mlflow_utils import create_mlflow_experiment
from codecarbon import EmissionsTracker

load_dotenv()

# Recupérer les credentials Google Cloud et Mlflow
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
else:
    print("Warning: GOOGLE_APPLICATION_CREDENTIALS non défini dans .env")

mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)
else:
    print("Warning: MLFLOW_TRACKING_URI non défini dans .env")

mlflow_artifacts_location = os.getenv('MLFLOW_ARTEFACTS_LOCATION')
if not mlflow_artifacts_location:
    print("Warning: MLFLOW_ARTEFACTS_LOCATION non défini dans .env")


experiment_name = "mouvement_social_prediction"
artifact_location = mlflow_artifacts_location
tags = {"env": "dev", "version": "1.0.0"}

experiment_id = create_mlflow_experiment(
    experiment_name=experiment_name,
    artifact_location=artifact_location,
    tags=tags
)

def upload_to_gcs(local_model_path, gcs_path, timeout=600):
    """
    Téléversement d'un fichier local vers Google Cloud Storage.
    """
    client = storage.Client()
    bucket_name = mlflow_artifacts_location.split('//')[1].split('/')[0]
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_model_path, timeout=timeout)
    print(f"Modèle uploadé vers {gcs_path} dans GCS avec succès.")

def log_and_upload_model(model, model_name, experiment_id):
    """
    Enregistrement et téléversement d'un modèle dans MLflow et GCS.
    """
    local_model_path = f"{model_name}.pkl"
    if os.path.isdir(local_model_path):
        shutil.rmtree(local_model_path)
    elif os.path.exists(local_model_path):
        os.remove(local_model_path)
    mlflow.sklearn.save_model(model, local_model_path)
    if os.path.isfile(local_model_path):
        gcs_model_path = f"models/{model_name}.pkl"
        upload_to_gcs(local_model_path, gcs_model_path)

def train_and_log_model(model, model_name, X_train, y_train, experiment_id):
    """
    Entraînement et enregistrement d'un modèle dans MLflow et GCS, suivi des émissions de carbone.
    """
    log_dir = f"log/log_carbon_{model_name}"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    tracker = EmissionsTracker(output_dir=log_dir)
    tracker.start()

    with mlflow.start_run(run_name=model_name, experiment_id=experiment_id):
        mlflow.sklearn.autolog()
        model.fit(X_train, y_train)
        log_and_upload_model(model, model_name, experiment_id)

        emissions = tracker.stop()
        if emissions is not None:
            mlflow.log_metric("carbon_emissions", emissions)
        else:
            print(f"Warning: Emissions for {model_name} were not calculated.")

        print(f"Modèle {model_name} enregistré et téléversé dans GCS.")

df = pd.read_csv('tests_models/data_test/fusion_courbe_mouvement.csv', delimiter=';', encoding='utf-8')
df.columns = df.columns.str.strip()

# Ajout de caractéristiques temporelles
df['mois'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.month
df['jour_semaine'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.dayofweek
df['moyenne_conso_horaire'] = df[['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
                                  '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
                                  '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']].mean(axis=1)

df_clean = df.dropna(subset=['Consommation_journaliere'])

# Mise à jour des features et de la target
features = df_clean[["région", "movement_social", "mois", "jour_semaine", "moyenne_conso_horaire"]]
target = df_clean['Consommation_journaliere']

# Encodage des variables catégorielles
categorical_cols = ["région"]
numerical_cols = ['movement_social', 'mois', 'jour_semaine', 'moyenne_conso_horaire']

# Transformation des colonnes catégorielles avec OneHotEncoder
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(), categorical_cols)
    ]
)

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# Modèle Ridge
ridge_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', Ridge())
])
param_grid = {'model__alpha': [0.1, 1.0, 10.0, 100.0]}
grid_search = GridSearchCV(ridge_model, param_grid, cv=5)
grid_search.fit(X_train, y_train)
best_ridge_model = grid_search.best_estimator_
train_and_log_model(best_ridge_model, "ridge_model", X_train, y_train, experiment_id)

# Modèle Random Forest
random_forest_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(n_estimators=100, random_state=42))
])
train_and_log_model(random_forest_model, "random_forest_model", X_train, y_train, experiment_id)
