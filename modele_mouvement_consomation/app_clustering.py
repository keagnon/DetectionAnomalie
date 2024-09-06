import streamlit as st
import pandas as pd
import mlflow
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

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

# Charger le modèle DBSCAN depuis MLflow
logged_model = 'runs:/faeb99c10bb64fe2880f5d867d8b3cda/dbscan_model'
loaded_model = mlflow.sklearn.load_model(logged_model)

# Interface Streamlit
st.title("Clustering des Consommations Énergétiques avec DBSCAN")

# Fonction pour prétraiter les données
def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)
    return df, hourly_columns

# Télécharger le fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Charger et prétraiter les données
    df, hourly_columns = preprocess_data(uploaded_file)

    # Appliquer le modèle DBSCAN
    if all(column in df.columns for column in hourly_columns):
        scaler = StandardScaler()
        X = scaler.fit_transform(df[hourly_columns])
        df['cluster'] = loaded_model.fit_predict(X)

        # Réduction de dimensions pour visualisation
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(X)
        df['pca1'] = df_pca[:, 0]
        df['pca2'] = df_pca[:, 1]

        # Afficher les résultats du clustering
        st.subheader("Résultats du Clustering DBSCAN")
        st.dataframe(df[['date', 'région', 'cluster']].head())

        # Visualiser les clusters avec PCA
        st.subheader("Visualisation des clusters")
        plt.figure(figsize=(10, 6))
        plt.scatter(df['pca1'], df['pca2'], c=df['cluster'], cmap='viridis', s=50)
        plt.title("Clustering DBSCAN")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.colorbar(label="Cluster")
        st.pyplot(plt)

        # Afficher les points marqués comme bruit (cluster = -1)
        st.subheader("Points marqués comme bruit")
        noise_points = df[df['cluster'] == -1]
        st.dataframe(noise_points[['date', 'région', 'cluster']])

    else:
        st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")
else:
    st.info("Veuillez charger un fichier CSV pour commencer l'analyse.")
