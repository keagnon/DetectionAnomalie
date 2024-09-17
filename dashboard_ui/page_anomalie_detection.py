"""
Affiche l'interface de détection d'anomalies dans les données de consommation.

- Permet de charger un fichier CSV pour détecter les anomalies via un modèle IsolationForest.
- Affiche les résultats sous forme de tableau et de graphiques.
- Log les détails (temps de réponse, anomalies, utilisation CPU/mémoire) dans Elasticsearch.
- Gère les erreurs et log les exceptions en cas d'échec.
"""

import os
import mlflow
import pandas as pd
import time
import plotly.graph_objects as go
import streamlit as st
import psutil
from utils import configure_google_credentials, local_css, preprocess_data
from utils import send_log_to_elastic, get_system_usage
from datetime import datetime
from elasticsearch import Elasticsearch


local_css("styles.css")
configure_google_credentials()

# Configuration MLflow
mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

LOGGED_MODEL = "runs:/a01b4b5c87f14c55b24cd5910fc7a874/isolation_forest_model"
MODEL_NAME = "IsolationForest"
MODEL_VERSION = "1.0.0"
loaded_model = mlflow.pyfunc.load_model(LOGGED_MODEL)


def show_anomalie_detection():
    """Affiche la page de détection d'anomalies."""

    st.markdown("<br>", unsafe_allow_html=True)
    st.title("💬 Détection d'anomalies dans les données")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    start_time = time.time()
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "model_execution",
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "application_name": "AnomalyDetectionApp",
        "status": "started",
        "log_level": "INFO"
    }

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if uploaded_file is not None:
        df, hourly_columns = preprocess_data(uploaded_file)

        # Log des inputs utilisateur
        log_data.update({
            "details": {
                "inputs": {
                    "file_name": uploaded_file.name,
                    "columns": hourly_columns,
                }
            }
        })

        if all(column in df.columns for column in hourly_columns):
            try:
                data = df[hourly_columns]
                df["anomaly"] = loaded_model.predict(data)
                end_time = time.time()

                response_time = end_time - start_time
                cpu_usage, memory_usage = get_system_usage()

                # Log en cas de succès
                anomalies_count = len(df[df["anomaly"] == -1])
                log_data.update({
                    "status": "completed",
                    "response_time": response_time,
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage,
                    "details": {
                        "anomalies_count": anomalies_count,
                        "successful_predictions": len(df) - anomalies_count,
                        "failed_predictions": 0,
                        "inputs": {
                            "file_name": uploaded_file.name,
                            "columns": hourly_columns,
                        }
                    }
                })

            except Exception as e:
                end_time = time.time()
                response_time = end_time - start_time

                # Log en cas d'échec
                log_data.update({
                    "status": "failed",
                    "response_time": response_time,
                    "error_message": str(e),
                    "error_type": type(e).__name__,
                    "details": {
                        "anomalies_count": 0,
                        "successful_predictions": 0,
                        "failed_predictions": len(df),
                        "inputs": {
                            "file_name": uploaded_file.name,
                            "columns": hourly_columns,
                        }
                    }
                })

            # Envoi du log à Elasticsearch
            send_log_to_elastic(log_data)

            display_anomalies_info(df)

            selected_columns = [
                "date",
                "région",
                "consommation_moyenne_journalière",
                "statut",
                "anomaly",
            ]
            st.dataframe(
                df[selected_columns].style.apply(highlight_anomalies, axis=1),
                width=1400,
            )

            st.markdown(
                '<div style="text-align: center;"><em>Tableau des anomalies détectées</em></div>',
                unsafe_allow_html=True,
            )

            anomalies_df = df[df["anomaly"] == -1]
            if not anomalies_df.empty:
                st.subheader("Visualisation des anomalies")
                selected_rows = st.multiselect(
                    "Choisissez les anomalies à afficher",
                    anomalies_df.index,
                    format_func=lambda idx: f"{anomalies_df.loc[idx, 'date']} - Région: {anomalies_df.loc[idx, 'région']}",
                )

                if selected_rows:
                    display_anomalies_graph(selected_rows, hourly_columns, anomalies_df)
            else:
                st.info("Aucune anomalie détectée.")
        else:
            st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")

def display_anomalies_info(df):
    """Affiche les informations sur les anomalies détectées."""
    total_rows = len(df)
    anomalies_count = len(df[df["anomaly"] == -1])
    non_anomalies_count = total_rows - anomalies_count

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 20px;">
            <div>
                <strong>Nombre d'anomalies :</strong>
                <span style="color: red;">{anomalies_count}</span>
            </div>
            <div>
                <strong>Nombre de lignes sans anomalies :</strong>
                <span style="color: green;">{non_anomalies_count}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def highlight_anomalies(row):
    """Met en surbrillance les lignes contenant des anomalies."""
    return ["background-color: red" if row.anomaly == -1 else "" for _ in row]

def display_anomalies_graph(selected_rows, hourly_columns, anomalies_df):
    """
    Affiche les graphiques des anomalies détectées.
    ::params :
        selected_rows : Les indices des lignes sélectionnées par l'utilisateur.
        hourly_columns : Les colonnes horaires.
        anomalies_df : Le DataFrame contenant les anomalies.

    """
    for i, row in enumerate(selected_rows):
        anomaly_row = anomalies_df.loc[row]
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hourly_columns,
                y=anomaly_row[hourly_columns],
                mode="lines+markers",
                line={"color": "red"},
                marker={"size": 6},
            )
        )

        fig.update_layout(
            title=f"Anomalie détectée le {anomaly_row['date']} - Région : {anomaly_row['région']}",
            xaxis_title="Heure",
            yaxis_title="Consommation (MWh)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        if i % 2 == 0:
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig, use_container_width=True)
        else:
            col2.plotly_chart(fig, use_container_width=True)
