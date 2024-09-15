"""
Ce script exécute un clustering (KMeans ou DBSCAN) sur des données de consommation énergétique,
enregistre les modèles et métriques dans MLflow, et mesure l'empreinte carbone avec CodeCarbon.

Principales étapes :
1. Prétraitement des données à partir d'un fichier CSV.
2. Clustering avec KMeans ou DBSCAN.
3. Suivi des émissions carbone pendant l'entraînement.
4. Enregistrement des résultats et des graphiques dans MLflow.

Variables d'environnement :
- MLFLOW_TRACKING_URI : URI du serveur MLflow.
- GOOGLE_APPLICATION_CREDENTIALS : Clés d'authentification Google.
- MLFLOW_ARTEFACTS_LOCATION : Emplacement pour les artefacts MLflow.
"""

import os
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from mlflow_utils import create_mlflow_experiment, get_mlflow_experiment
from codecarbon import EmissionsTracker
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)
else:
    print("Warning: MLFLOW_TRACKING_URI non défini dans .env")

google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
else:
    print("Warning: GOOGLE_APPLICATIONS_CREDENTIALS non défini dans .env")

experiment_name = "clustering_model_mouvement_consommation"
artifact_location = os.getenv('MLFLOW_ARTEFACTS_LOCATION')
tags = {"env": "dev", "version": "1.0.0"}

if not artifact_location:
    print("Warning: MLFLOW_ARTEFACTS_LOCATION non défini dans .env")
experiment_id = create_mlflow_experiment(experiment_name, artifact_location, tags)


def preprocess_data(file_path):
    """
    Prétraiter les données avant clustering.

    ::params:
        file_path (str): Chemin vers le fichier CSV contenant les données à traiter.

    Returns:
        pd.DataFrame: Données prétraitées.
        list: Liste des colonnes horaires à utiliser pour le clustering.
    """
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Créer des colonnes horaires pour la consommation
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)

    return df, hourly_columns


def run_kmeans_clustering(df, hourly_columns, num_clusters=3):
    """
    Exécuter un clustering KMeans sur les données prétraitées.

    ::params:
        df (pd.DataFrame): Données prétraitées.
        hourly_columns (list): Colonnes horaires à utiliser pour le clustering.
        num_clusters (int): Nombre de clusters KMeans.

    Returns:
        pd.DataFrame: Données avec le label de cluster.
        KMeans: Modèle KMeans entraîné.
    """
    scaler = StandardScaler()
    X = scaler.fit_transform(df[hourly_columns])

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)

    # Créer le dossier de log pour KMeans
    log_dir = "log/kmeans/log_carbon_clustering"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    tracker = EmissionsTracker(output_dir=log_dir)

    with mlflow.start_run(run_name="KMeans_Clustering", experiment_id=experiment_id):
        mlflow.sklearn.autolog()
        df['cluster'] = kmeans.fit_predict(X)
        mlflow.log_param("num_clusters", num_clusters)
        mlflow.sklearn.log_model(kmeans, "kmeans_model")
        mlflow.log_metric("inertia", kmeans.inertia_)

        unique, counts = pd.Series(df['cluster']).value_counts().index, pd.Series(df['cluster']).value_counts().values
        for u, c in zip(unique, counts):
            mlflow.log_metric(f"cluster_{u}_size", c)

        # PCA pour visualiser les clusters
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(X)
        df['pca1'] = df_pca[:, 0]
        df['pca2'] = df_pca[:, 1]

        # Enregistrer la figure des clusters
        plt.figure(figsize=(10, 6))
        plt.scatter(df['pca1'], df['pca2'], c=df['cluster'], cmap='viridis', s=50)
        plt.title("K-means Clustering")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.colorbar(label="Cluster")
        plt.savefig("kmeans_clusters.png")
        mlflow.log_artifact("kmeans_clusters.png")

    emissions = tracker.stop()
    mlflow.log_metric("carbon_emissions", emissions)

    return df, kmeans


def run_dbscan_clustering(df, hourly_columns, eps=0.5, min_samples=5):
    """
    Exécuter un clustering DBSCAN sur les données prétraitées.

    ::params:
        df (pd.DataFrame): Données prétraitées.
        hourly_columns (list): Colonnes horaires à utiliser pour le clustering.
        eps (float): Distance maximale entre deux points pour les relier dans un cluster.
        min_samples (int): Nombre minimum de points pour former un cluster.

    Returns:
        pd.DataFrame: Données avec le label de cluster.
        DBSCAN: Modèle DBSCAN entraîné.
    """
    scaler = StandardScaler()
    X = scaler.fit_transform(df[hourly_columns])

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)

    # Créer le dossier de log pour DBSCAN
    log_dir = "log/dbscan/log_carbon_clustering"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    tracker = EmissionsTracker(output_dir=log_dir)
    tracker.start()

    with mlflow.start_run(run_name="DBSCAN_Clustering", experiment_id=experiment_id):
        mlflow.sklearn.autolog()
        df['cluster'] = dbscan.fit_predict(X)
        mlflow.log_param("eps", eps)
        mlflow.log_param("min_samples", min_samples)
        mlflow.sklearn.log_model(dbscan, "dbscan_model")

        num_clusters = len(set(df['cluster']) - {-1})
        mlflow.log_metric("num_clusters", num_clusters)

        # Proportion de bruit (outliers)
        noise_points = df['cluster'].value_counts().get(-1, 0)
        total_points = len(df)
        noise_ratio = noise_points / total_points
        mlflow.log_metric("noise_ratio", noise_ratio)

        # PCA pour visualiser les clusters
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(X)
        df['pca1'] = df_pca[:, 0]
        df['pca2'] = df_pca[:, 1]

        # Enregistrer la figure des clusters
        plt.figure(figsize=(10, 6))
        plt.scatter(df['pca1'], df['pca2'], c=df['cluster'], cmap='viridis', s=50)
        plt.title("DBSCAN Clustering")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.colorbar(label="Cluster")
        plt.savefig("dbscan_clusters.png")
        mlflow.log_artifact("dbscan_clusters.png")

    emissions = tracker.stop()
    mlflow.log_metric("carbon_emissions", emissions)

    return df, dbscan


# Prétraitement des données
file_path = 'tests_models/data_test/merge_courbe_mouvement.csv'
df, hourly_columns = preprocess_data(file_path)

# Choisir la méthode de clustering
method = 'K-means'

if method == 'K-means':
    num_clusters = 4
    df, model = run_kmeans_clustering(df, hourly_columns, num_clusters)
else:
    eps = 0.5
    min_samples = 5
    df, model = run_dbscan_clustering(df, hourly_columns, eps, min_samples)
