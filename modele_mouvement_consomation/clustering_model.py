import os
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)
else:
    print("Warning: MLFLOW_TRACKING_URI non défini dans .env")

# Configurer les credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
else:
    print("Warning: GOOGLE_APPLICATION_CREDENTIALS non défini dans .env")

# Fonction pour créer ou récupérer une expérience MLflow
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

# Création ou récupération de l'expérience MLflow
experiment_name = "clustering_model_mouvement_consommation"
artifact_location = os.getenv('MLFLOW_ARTEFACTS_LOCATION')
tags = {"env": "dev", "version": "1.0.0"}

if not artifact_location:
    print("Warning: MLFLOW_ARTEFACTS_LOCATION non défini dans .env")

experiment_id = create_mlflow_experiment(experiment_name, artifact_location, tags)

# Fonction de prétraitement des données
def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)
    return df, hourly_columns

# Fonction pour exécuter le clustering avec K-means et suivi avec MLflow
def run_kmeans_clustering(df, hourly_columns, num_clusters=3):
    scaler = StandardScaler()
    X = scaler.fit_transform(df[hourly_columns])

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)

    with mlflow.start_run(run_name="KMeans_Clustering", experiment_id=experiment_id):
        df['cluster'] = kmeans.fit_predict(X)

        # Enregistrer le modèle et les paramètres dans MLflow
        mlflow.log_param("num_clusters", num_clusters)
        mlflow.sklearn.log_model(kmeans, "kmeans_model")

        # Log metrics (inertia = somme des distances au centre des clusters)
        mlflow.log_metric("inertia", kmeans.inertia_)

        # Enregistrer le nombre de points dans chaque cluster
        unique, counts = pd.Series(df['cluster']).value_counts().index, pd.Series(df['cluster']).value_counts().values
        for u, c in zip(unique, counts):
            mlflow.log_metric(f"cluster_{u}_size", c)

        # Réduction de dimensions avec PCA pour visualisation
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(X)
        df['pca1'] = df_pca[:, 0]
        df['pca2'] = df_pca[:, 1]

        # Enregistrer un graphique dans MLflow
        plt.figure(figsize=(10, 6))
        plt.scatter(df['pca1'], df['pca2'], c=df['cluster'], cmap='viridis', s=50)
        plt.title("K-means Clustering")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.colorbar(label="Cluster")
        plt.savefig("kmeans_clusters.png")
        mlflow.log_artifact("kmeans_clusters.png")
        
        return df, kmeans

# Fonction pour exécuter le clustering avec DBSCAN et suivi avec MLflow
def run_dbscan_clustering(df, hourly_columns, eps=0.5, min_samples=5):
    scaler = StandardScaler()
    X = scaler.fit_transform(df[hourly_columns])

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)

    with mlflow.start_run(run_name="DBSCAN_Clustering", experiment_id=experiment_id):
        df['cluster'] = dbscan.fit_predict(X)

        # Enregistrer les paramètres dans MLflow
        mlflow.log_param("eps", eps)
        mlflow.log_param("min_samples", min_samples)
        mlflow.sklearn.log_model(dbscan, "dbscan_model")

        # Calcul du nombre de clusters (exclure les outliers marqués comme -1)
        num_clusters = len(set(df['cluster']) - {-1})
        mlflow.log_metric("num_clusters", num_clusters)

        # Enregistrer la proportion de points considérés comme "bruit" (outliers)
        noise_points = df['cluster'].value_counts().get(-1, 0)
        total_points = len(df)
        noise_ratio = noise_points / total_points
        mlflow.log_metric("noise_ratio", noise_ratio)

        # Réduction de dimensions avec PCA pour visualisation
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(X)
        df['pca1'] = df_pca[:, 0]
        df['pca2'] = df_pca[:, 1]

        # Enregistrer un graphique dans MLflow
        plt.figure(figsize=(10, 6))
        plt.scatter(df['pca1'], df['pca2'], c=df['cluster'], cmap='viridis', s=50)
        plt.title("DBSCAN Clustering")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.colorbar(label="Cluster")
        plt.savefig("dbscan_clusters.png")
        mlflow.log_artifact("dbscan_clusters.png")

        return df, dbscan

# Exemple d'utilisation
file_path = 'merge_courbe_mouvement.csv'
df, hourly_columns = preprocess_data(file_path)

# Choisir le modèle à exécuter (K-means ou DBSCAN)
method = 'DBSCAN'  # Changer en 'DBSCAN' pour utiliser DBSCAN

if method == 'K-means':
    num_clusters = 4  # Nombre de clusters
    df, model = run_kmeans_clustering(df, hourly_columns, num_clusters)
else:
    eps = 0.5  # Paramètre de distance pour DBSCAN
    min_samples = 5  # Nombre minimum de points pour former un cluster
    df, model = run_dbscan_clustering(df, hourly_columns, eps, min_samples)
