import streamlit as st
import pandas as pd
import numpy as np
import mlflow
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()

# Configurations des credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials

# Configuration MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

# Chargement du modèle DBSCAN depuis MLflow
logged_model = 'runs:/096e31c04a7e4beaa1054645122fc825/dbscan_model'
loaded_model = mlflow.sklearn.load_model(logged_model)

st.title("Clustering des Consommations Énergétiques avec DBSCAN")

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)
    return df, hourly_columns

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

if uploaded_file is not None:
    df, hourly_columns = preprocess_data(uploaded_file)

    if all(column in df.columns for column in hourly_columns):
        scaler = StandardScaler()
        X = scaler.fit_transform(df[hourly_columns])
        df['cluster'] = loaded_model.fit_predict(X)

        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(X)
        df['pca1'] = df_pca[:, 0]
        df['pca2'] = df_pca[:, 1]

        unique_labels, counts = np.unique(df['cluster'], return_counts=True)

        with mlflow.start_run() as run:
            for label, count in zip(unique_labels, counts):
                if label == -1:
                    mlflow.log_metric('noise_points', count)
                else:
                    mlflow.log_metric(f'cluster_{label}_size', count)

        st.subheader("Résultats du Clustering DBSCAN")
        st.dataframe(df[['date', 'région', 'cluster']].head())

        st.subheader("Nombre de données dans chaque cluster")
        for label, count in zip(unique_labels, counts):
            if label == -1:
                st.write(f"Nombre de points de bruit : {count}")
            else:
                st.write(f"Cluster {label}: {count} points")

        st.subheader("Visualisation des clusters")
        fig = px.scatter(
            df,
            x='pca1',
            y='pca2',
            color='cluster',
            title="Clustering DBSCAN",
            labels={'pca1': 'PCA 1', 'pca2': 'PCA 2', 'cluster': 'Cluster'},
            hover_data=['date', 'région', 'consommation_moyenne_journalière', 'cluster'],
            size=np.ones(len(df)) * 10
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Cluster"))

        for label, count in zip(unique_labels, counts):
            if label != -1:
                label_data = df[df['cluster'] == label]
                centroid_x = label_data['pca1'].mean()
                centroid_y = label_data['pca2'].mean()
                fig.add_annotation(
                    x=centroid_x,
                    y=centroid_y,
                    text=f"Cluster {label}<br>{count} points",
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-30,
                    bgcolor="white",
                    bordercolor="black",
                    font=dict(size=10)
                )

        st.plotly_chart(fig)

        st.subheader("Points marqués comme bruit")
        noise_points = df[df['cluster'] == -1]
        st.dataframe(noise_points[['date', 'région', 'cluster']])

    else:
        st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")
else:
    st.info("Veuillez charger un fichier CSV pour commencer l'analyse.")
