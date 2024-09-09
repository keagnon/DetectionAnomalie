import os
import streamlit as st
import mlflow
import pandas as pd

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from dotenv import load_dotenv

load_dotenv()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

# Configurer les credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials

# Configuration MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

# Chargement du modèle MLflow pour la détection d'anomalies
logged_model = 'runs:/a01b4b5c87f14c55b24cd5910fc7a874/isolation_forest_model'
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Fonction de prétraitement des données
def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)
    return df, hourly_columns

def show_anomalie_detection():
    """
    Affiche un formulaire pour envoyer des commentaires.
    """

    st.title("💬 Détection d'anomalies dans les données")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if uploaded_file is not None:
        # Charger et prétraiter les données
        df, hourly_columns = preprocess_data(uploaded_file)

        if all(column in df.columns for column in hourly_columns):
            # Effectuer la prédiction des anomalies
            data = df[hourly_columns]
            df['anomaly'] = loaded_model.predict(data)

            # Calcul du nombre de lignes avec et sans anomalies
            total_rows = len(df)
            anomalies_count = len(df[df['anomaly'] == -1])
            non_anomalies_count = total_rows - anomalies_count

            st.markdown("<br>", unsafe_allow_html=True)
            # Afficher les résultats avec des nombres surlignés en vert
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <div>
                        <strong>Nombre d'anomalies :</strong> <span style="color: green;">{anomalies_count}</span>
                    </div>
                    <div>
                        <strong>Nombre de lignes sans anomalies :</strong> <span style="color: green;">{non_anomalies_count}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            selected_columns = ['date', 'région', 'consommation_moyenne_journalière', 'statut', 'anomaly']

            # Appliquer du style pour mettre en évidence les anomalies
            def highlight_anomalies(row):
                return ['background-color: red' if row.anomaly == -1 else '' for _ in row]

            # Afficher le dataframe avec les anomalies
            st.dataframe(df[selected_columns].style.apply(highlight_anomalies, axis=1), width=1400)

            # Ajouter du texte stylé sous la table
            st.markdown('<div style="text-align: center;"><em>Tableau des anomalies détectées</em></div>', unsafe_allow_html=True)

            # Filtrer les lignes avec anomalies
            anomalies_df = df[df['anomaly'] == -1]

            # Laisser l'utilisateur choisir les anomalies à tracer
            if not anomalies_df.empty:
                st.subheader("Visualisation des anomalies")
                selected_rows = st.multiselect(
                    "Choisissez les anomalies à afficher",
                    anomalies_df.index,
                    format_func=lambda idx: f"{anomalies_df.loc[idx, 'date']} - Région: {anomalies_df.loc[idx, 'région']}"
                )

                if selected_rows:
                    for i, row in enumerate(selected_rows):
                        anomaly_row = anomalies_df.loc[row]
                        fig = go.Figure()

                        fig.add_trace(go.Scatter(x=hourly_columns,
                                                y=anomaly_row[hourly_columns],
                                                mode='lines+markers',
                                                line=dict(color='red'),
                                                marker=dict(size=6)))
                        fig.update_layout(
                            title=f"Anomalie détectée le {anomaly_row['date']} - Région : {anomaly_row['région']}",
                            xaxis_title="Heure",
                            yaxis_title="Consommation (MWh)",
                            paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent
                            plot_bgcolor='rgba(0,0,0,0)'   # Fond transparent
                        )

                        # Afficher 2 graphiques par ligne
                        if i % 2 == 0:
                            col1, col2 = st.columns(2)
                            col1.plotly_chart(fig, use_container_width=True)
                        else:
                            col2.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune anomalie détectée.")
        else:
            st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")
