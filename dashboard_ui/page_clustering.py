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
from utils import local_css, configure_google_credentials, preprocess_data

local_css("styles.css")
configure_google_credentials()

# Charger le modèle DBSCAN depuis MLflow
LOGGED_MODEL = "runs:/096e31c04a7e4beaa1054645122fc825/dbscan_model"
loaded_model = mlflow.sklearn.load_model(LOGGED_MODEL)


def log_cluster_metrics(unique_labels, counts):
    """
    Enregistrer les métriques de clustering dans MLflow.

    Args:
        unique_labels (np.ndarray): Labels uniques des clusters.
        counts (np.ndarray): Nombre de points dans chaque cluster.
    """
    with mlflow.start_run():
        for label, count in zip(unique_labels, counts):
            if label == -1:
                mlflow.log_metric("noise_points", count)
            else:
                mlflow.log_metric(f"cluster_{label}_size", count)


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
            st.markdown(
                f"<span style='color: red;'>• Cluster {label} : {count} points</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<span style='color: green;'>• Cluster {label} : {count} points</span>",
                unsafe_allow_html=True,
            )


def display_clustering_plot(df, hourly_columns):
    """
    Affiche le graphe du clustering en utilisant la réduction de dimensions PCA.

    Args:
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
    log_cluster_metrics(unique_labels, counts)

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
        display_cluster_summary(unique_labels, counts)

    return df, unique_labels


def display_noise_points(df, unique_labels):
    """
    Afficher les points considérés comme bruit dans les clusters.

    Args:
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
    st.title("🌦️Clustering")
    st.write("Ceci est la page pour faire du clustering.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    if uploaded_file is not None:
        df, hourly_columns = preprocess_data(uploaded_file)

        if all(column in df.columns for column in hourly_columns):
            df, unique_labels = display_clustering_plot(df, hourly_columns)
            display_noise_points(df, unique_labels)
        else:
            st.error(
                "Les colonnes horaires ne sont pas toutes présentes dans le dataset."
            )
    else:
        st.info("Veuillez charger un fichier CSV pour commencer l'analyse.")
