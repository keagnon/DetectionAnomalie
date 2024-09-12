"""
Module pour la détection d'anomalies dans les données de consommation énergétique.
"""

import os
import streamlit as st
import mlflow
import pandas as pd
import plotly.graph_objects as go

from utils import local_css, configure_google_credentials, preprocess_data

local_css("styles.css")
configure_google_credentials()

# Configuration MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

LOGGED_MODEL = 'runs:/a01b4b5c87f14c55b24cd5910fc7a874/isolation_forest_model'
loaded_model = mlflow.pyfunc.load_model(LOGGED_MODEL)

def display_anomalies_info(df):
    """
    Affiche les informations sur le nombre d'anomalies et de lignes sans anomalies.

    Args:
        df (pd.DataFrame): Le dataframe contenant les données avec les anomalies détectées.
    """
    total_rows = len(df)
    anomalies_count = len(df[df['anomaly'] == -1])
    non_anomalies_count = total_rows - anomalies_count

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 20px;">
            <div>
                <strong>Nombre d'anomalies :</strong>
                <span style="color: green;">{anomalies_count}</span>
            </div>
            <div>
                <strong>Nombre de lignes sans anomalies :</strong>
                <span style="color: green;">{non_anomalies_count}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def highlight_anomalies(row):
    """
    Fonction de style pour mettre en évidence les anomalies dans le dataframe.

    Args:
        row (pd.Series): Une ligne du dataframe.

    Returns:
        list: Liste des styles à appliquer à la ligne.
    """
    return ['background-color: red' if row.anomaly == -1 else '' for _ in row]


def display_anomalies_graph(selected_rows, hourly_columns, anomalies_df):
    """
    Affiche les graphiques des anomalies sélectionnées par l'utilisateur.

    Args:
        selected_rows (list): Liste des indices des anomalies sélectionnées.
        hourly_columns (list): Liste des colonnes horaires.
        anomalies_df (pd.DataFrame): Dataframe contenant uniquement les anomalies.
    """
    for i, row in enumerate(selected_rows):
        anomaly_row = anomalies_df.loc[row]
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=hourly_columns,
            y=anomaly_row[hourly_columns],
            mode='lines+markers',
            line={'color': 'red'},
            marker={'size': 6}
        ))

        fig.update_layout(
            title=f"Anomalie détectée le {anomaly_row['date']} - Région : {anomaly_row['région']}",
            xaxis_title="Heure",
            yaxis_title="Consommation (MWh)",
            paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent
            plot_bgcolor='rgba(0,0,0,0)'
        )

        # Afficher 2 graphiques par ligne
        if i % 2 == 0:
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig, use_container_width=True)
        else:
            col2.plotly_chart(fig, use_container_width=True)


def show_anomalie_detection():
    """
    Affiche la page de détection des anomalies dans les données de consommation énergétique.
    """
    st.title("💬 Détection d'anomalies dans les données")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if uploaded_file is not None:
        df, hourly_columns = preprocess_data(uploaded_file)

        if all(column in df.columns for column in hourly_columns):
            # Effectuer la prédiction des anomalies
            data = df[hourly_columns]
            df['anomaly'] = loaded_model.predict(data)

            # Afficher les informations d'anomalies
            display_anomalies_info(df)

            selected_columns = [
                'date', 'région',
                'consommation_moyenne_journalière',
                'statut', 'anomaly']
            st.dataframe(df[selected_columns].style.apply(highlight_anomalies, axis=1), width=1400)

            st.markdown(
                '<div style="text-align: center;"><em>Tableau des anomalies détectées</em></div>',
                unsafe_allow_html=True
            )

            # Filtrer les lignes avec anomalies
            anomalies_df = df[df['anomaly'] == -1]
            if not anomalies_df.empty:
                st.subheader("Visualisation des anomalies")
                selected_rows = st.multiselect(
                    "Choisissez les anomalies à afficher",
                    anomalies_df.index,
                    format_func=lambda idx:
                    f"{anomalies_df.loc[idx, 'date']} - Région: {anomalies_df.loc[idx, 'région']}"
                )

                if selected_rows:
                    display_anomalies_graph(selected_rows, hourly_columns, anomalies_df)
            else:
                st.info("Aucune anomalie détectée.")
        else:
            st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")
