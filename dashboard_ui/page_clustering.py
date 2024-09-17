"""
Affiche l'interface pour le clustering des données de consommation énergétique.

- Permet de charger un fichier CSV et de traiter les données pour le clustering avec le modèle DBSCAN.
- Visualise les clusters et les points de bruit détectés.
- Log les détails des clusters (taille, points de bruit) et les métriques système (CPU/mémoire) dans Elasticsearch.
- Gère les erreurs et log les exceptions en cas d'échec.
"""
import os
import numpy as np
import pandas as pd
import mlflow
import time
import streamlit as st
import psutil
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from utils import configure_google_credentials, local_css, preprocess_data
from utils import send_log_to_elastic, get_system_usage
from datetime import datetime
from elasticsearch import Elasticsearch


local_css("styles.css")
configure_google_credentials()

# Charger le modèle DBSCAN depuis MLflow
LOGGED_MODEL = "runs:/096e31c04a7e4beaa1054645122fc825/dbscan_model"
loaded_model = mlflow.sklearn.load_model(LOGGED_MODEL)


def log_unified(event_status, model_name, model_version, response_time, clusters_logged, inputs, anomalies_count=0, noise_points_count=0):
    """
    Enregistre les logs unifiés dans Elasticsearch.
    ::params:
        event_status (str): Statut de l'événement (ex: "completed", "error").
        model_name (str): Nom du modèle utilisé.
        model_version (str): Version du modèle utilisé.
        response_time (float): Temps de réponse de l'exécution.
        clusters_logged (int): Nombre de clusters enregistrés.
        inputs (dict): Détails des inputs fournis par l'utilisateur.
        anomalies_count (int): Nombre d'anomalies détectées (par défaut 0).
        noise_points_count (int): Nombre de points de bruit (par défaut 0).
    """

    cpu_usage, memory_usage = get_system_usage()

    # Création log unifié avec les détails des inputs
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "model_execution",
        "model_name": model_name,
        "model_version": model_version,
        "application_name": "ClusteringApp",
        "response_time": response_time,
        "log_level": "INFO" if event_status == "completed" else "ERROR",
        "status": event_status,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "details": {
            "clusters_logged": clusters_logged,
            "anomalies_count": anomalies_count,
            "noise_points_count": noise_points_count,
            "inputs": inputs  # Inclure les inputs ici
        }
    }
    send_log_to_elastic(log_data)

def display_clustering_plot(df, hourly_columns):
    """
    Affiche le graphe du clustering en utilisant la réduction de dimensions PCA.

    ::params:
        df (pd.DataFrame): DataFrame contenant les données prétraitées.
        hourly_columns (list): Liste des colonnes horaires.
    """
    scaler = StandardScaler()
    x_data = scaler.fit_transform(df[hourly_columns])
    df["cluster"] = loaded_model.fit_predict(x_data)

    # Réduction de dimensions pour visualisation
    pca = PCA(n_components=2)
    df_pca = pca.fit_transform(x_data)
    df["pca1"] = df_pca[:, 0]
    df["pca2"] = df_pca[:, 1]

    unique_labels, counts = np.unique(df["cluster"], return_counts=True)

    # Enregistrer les métriques dans MLflow
    with mlflow.start_run():
        for label, count in zip(unique_labels, counts):
            if label == -1:
                mlflow.log_metric("noise_points", count)
            else:
                mlflow.log_metric(f"cluster_{label}_size", count)

    # Créer le log unifié avec les informations pertinentes
    response_time = 1.0  # Simulez une durée d'exécution
    inputs = {
        "file_name": "fichier_échantillon.csv",
        "hourly_columns": hourly_columns
    }

    log_unified(
        event_status="completed",
        model_name="DBSCAN",
        model_version="1.0.0",
        response_time=response_time,
        clusters_logged=len(unique_labels),
        inputs=inputs,
        noise_points_count=len(df[df["cluster"] == -1])
    )

    col1, col2 = st.columns([7, 3], gap="medium")

    with col1:
        fig = px.scatter(
            df,
            x="pca1",
            y="pca2",
            color="cluster",
            title="Clustering DBSCAN",
            labels={"pca1": "PCA 1", "pca2": "PCA 2", "cluster": "Cluster"},
            hover_data=[
                "date",
                "région",
                "consommation_moyenne_journalière",
                "cluster",
            ],
            size=np.ones(len(df)) * 10,
        )
        fig.update_layout(coloraxis_colorbar={"title": "Cluster"})
        st.plotly_chart(fig)
        st.markdown(
            '<div style="text-align: center;"><em>Visualisation des clusters</em></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.subheader("Résumé des clusters")
        for label, count in zip(unique_labels, counts):
            if label == -1:
                st.markdown(
                    f"<span style='color: red;'>• Cluster {label} : {count} points</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<span style='color: green;'>• Cluster {label} : {count} points</span>",
                    unsafe_allow_html=True,
                )

    return df, unique_labels

def display_noise_points(df, unique_labels):
    """
    Afficher les points considérés comme bruit dans les clusters et envoyer les logs à Elasticsearch.

    ::params:
        df (pd.DataFrame): DataFrame contenant les données prétraitées.
        unique_labels (np.ndarray): Labels uniques des clusters.
    """
    col3, col4 = st.columns([7, 3], gap="medium")

    with col3:
        noise_points = df[df["cluster"] == -1]
        if not noise_points.empty:
            fig_noise = px.scatter(
                noise_points,
                x="pca1",
                y="pca2",
                title="Points marqués comme bruit",
                labels={"pca1": "PCA 1", "pca2": "PCA 2"},
                hover_data=["date", "région"],
                size=np.ones(len(noise_points)) * 10,
                color_discrete_sequence=["red"],
            )
            st.plotly_chart(fig_noise)
            st.markdown(
                '<div style="text-align: center;"><em>Visualisation des points de bruit</em></div>',
                unsafe_allow_html=True,
            )

    with col4:
        if not noise_points.empty:
            st.dataframe(noise_points[["date", "région", "cluster"]])
            st.markdown(
                '<div style="text-align: center;"><em>Tableau des points de bruit</em></div>',
                unsafe_allow_html=True,
            )

def show_clustering():
    """
    Afficher la page de clustering.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("🌦️Clustering")
    st.write("Ceci est la page pour faire du clustering.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    if uploaded_file is not None:
        df, hourly_columns = preprocess_data(uploaded_file)

        # Logger les inputs du fichier
        inputs = {
            "file_name": uploaded_file.name,
            "hourly_columns": hourly_columns
        }

        if all(column in df.columns for column in hourly_columns):
            df, unique_labels = display_clustering_plot(df, hourly_columns)
            display_noise_points(df, unique_labels)
        else:
            st.error(
                "Les colonnes horaires ne sont pas toutes présentes dans le dataset."
            )
    else:
        st.info("Veuillez charger un fichier CSV pour commencer l'analyse.")
