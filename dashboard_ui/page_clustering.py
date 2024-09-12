"""
Module pour le clustering des données de consommation énergétique.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import mlflow
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px
from dotenv import load_dotenv
import plotly.graph_objects as go

load_dotenv()

# Configurer MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

# Charger le modèle DBSCAN depuis MLflow
LOGGED_MODEL = 'runs:/096e31c04a7e4beaa1054645122fc825/dbscan_model'
loaded_model = mlflow.sklearn.load_model(LOGGED_MODEL)


def local_css(file_name):
    """
    Charge et applique un fichier CSS pour styliser l'application.

    Args:
        file_name (str): Chemin vers le fichier CSS.
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("styles.css")


def preprocess_data(file_path):
    """
    Charger et prétraiter les données du fichier CSV.

    Args:
        file_path (str): Chemin vers le fichier CSV.

    Returns:
        tuple: DataFrame prétraité et liste des colonnes horaires.
    """
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)
    return df, hourly_columns


def log_cluster_metrics(unique_labels, counts):
    """
    Enregistrer les métriques de clustering dans MLflow.

    Args:
        unique_labels (np.ndarray): Labels uniques des clusters.
        counts (np.ndarray): Nombre de points dans chaque cluster.
    """
    with mlflow.start_run() as run:
        for label, count in zip(unique_labels, counts):
            if label == -1:
                mlflow.log_metric('noise_points', count)
            else:
                mlflow.log_metric(f'cluster_{label}_size', count)


def display_cluster_summary(unique_labels, counts):
    """
    Afficher un résumé des clusters avec leur nombre de points.

    Args:
        unique_labels (np.ndarray): Labels uniques des clusters.
        counts (np.ndarray): Nombre de points dans chaque cluster.
    """
    st.subheader("Résumé des clusters")
    for label, count in zip(unique_labels, counts):
        if label == -1:
            st.markdown(f"<span style='color: red;'>• Cluster {label} : {count} points</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color: green;'>• Cluster {label} : {count} points</span>", unsafe_allow_html=True)


def show_clustering():
    """
    Afficher la page de clustering.
    """
    st.title("🌦️Clustering")
    st.write("Ceci est la page pour faire du clustering.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    if uploaded_file is not None:
        df, hourly_columns = preprocess_data(uploaded_file)

        # Appliquer le modèle DBSCAN
        if all(column in df.columns for column in hourly_columns):
            scaler = StandardScaler()
            x_data = scaler.fit_transform(df[hourly_columns])
            df['cluster'] = loaded_model.fit_predict(x_data)

            # Réduction de dimensions pour visualisation
            pca = PCA(n_components=2)
            df_pca = pca.fit_transform(x_data)
            df['pca1'] = df_pca[:, 0]
            df['pca2'] = df_pca[:, 1]

            # Compter le nombre de points dans chaque cluster
            unique_labels, counts = np.unique(df['cluster'], return_counts=True)

            # Enregistrer les métriques dans MLflow
            log_cluster_metrics(unique_labels, counts)

            col1, col2 = st.columns([7, 3], gap="medium")

            with col1:
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
                st.plotly_chart(fig)
                st.markdown('<div style="text-align: center;"><em>Visualisation des clusters</em></div>', unsafe_allow_html=True)

            with col2:
                display_cluster_summary(unique_labels, counts)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            col3, col4 = st.columns([7, 3], gap="medium")

            with col3:
                # Visualisation des points de bruit
                noise_points = df[df['cluster'] == -1]
                if not noise_points.empty:
                    fig_noise = px.scatter(
                        noise_points,
                        x='pca1',
                        y='pca2',
                        title="Points marqués comme bruit",
                        labels={'pca1': 'PCA 1', 'pca2': 'PCA 2'},
                        hover_data=['date', 'région'],
                        size=np.ones(len(noise_points)) * 10,
                        color_discrete_sequence=['red']
                    )
                    st.plotly_chart(fig_noise)
                    st.markdown('<div style="text-align: center;"><em>Visualisation des points de bruit</em></div>', unsafe_allow_html=True)

            with col4:
                if not noise_points.empty:
                    st.dataframe(noise_points[['date', 'région', 'cluster']])
                    st.markdown('<div style="text-align: center;"><em>Tableau des points de bruit</em></div>', unsafe_allow_html=True)

        else:
            st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")
    else:
        st.info("Veuillez charger un fichier CSV pour commencer l'analyse.")
