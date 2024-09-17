"""
Affiche l'interface de prédiction de la consommation énergétique en fonction des conditions météorologiques.

- Permet de saisir les données météo (température, vent, humidité, etc.).
- Effectue une prédiction énergétique à partir du modèle MLflow chargé.
- Affiche les résultats et log les détails des entrées utilisateur et de la prédiction dans Elasticsearch.
- Gère les erreurs et log les exceptions en cas d'échec.
"""
import os
import numpy as np
import pandas as pd
import mlflow
import streamlit as st
import psutil
import time
from dotenv import load_dotenv
from utils import configure_google_credentials, local_css, preprocess_data
from utils import send_log_to_elastic, get_system_usage
from elasticsearch import Elasticsearch
from datetime import datetime


load_dotenv()
local_css("styles.css")
configure_google_credentials()


def load_model():
    """
    Charge le modèle MLflow pour la prédiction.

    Retourne:
        Un modèle MLflow chargé.
    """
    logged_model = 'runs:/b1b9458f76a245e192fca44a3c1d22cc/best_estimator'
    return mlflow.pyfunc.load_model(logged_model)

def show_prediction_meteo():
    """
    Affiche le formulaire de prédiction météo avec MLflow intégré pour la prédiction énergétique.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("🌦️ Prédiction d'énergie consommée")
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Dans cette section, nous faisons la prédiction en prenant en compte des conditions météorologiques.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Mise en page avec colonnes
    col1, col2 = st.columns(2)

    with col1:
        temp_max = st.number_input(
            "Température Max (°C)", min_value=-50.0, max_value=50.0, value=25.0
        )
        temp_min = st.number_input(
            "Température Min (°C)", min_value=-50.0, max_value=50.0, value=15.0
        )
        wind_speed = st.number_input(
            "Vitesse du vent (km/h)", min_value=0, max_value=200, value=10
        )

    with col2:
        humidity = st.number_input("Humidité (%)", min_value=0, max_value=100, value=50)
        visibility = st.number_input(
            "Visibilité (km)", min_value=0, max_value=50, value=10
        )
        cloud_coverage = st.slider("Couverture Nuageuse (%)", 0, 100, 50)

    # Log des données d'entrée utilisateur
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "prediction_input",
        "temp_max": temp_max,
        "temp_min": temp_min,
        "wind_speed": wind_speed,
        "humidity": humidity,
        "visibility": visibility,
        "cloud_coverage": cloud_coverage,
        "log_level": "INFO"
    }
    send_log_to_elastic(log_data)

    # Bouton de prédiction
    if st.button("🔍 Prédire la Consommation Énergétique"):
        try:
            with st.spinner("Chargement du modèle et prédiction en cours..."):
                model = load_model()

                # Préparer les données pour la prédiction
                input_data = pd.DataFrame({
                    'TempMax_Deg': [temp_max],
                    'TempMin_Deg': [temp_min],
                    'Wind_kmh': [wind_speed],
                    'Wet_percent': [humidity],
                    'Visibility_km': [visibility],
                    'CloudCoverage_percent': [cloud_coverage]
                })

                input_data = input_data.astype(float)

                # Faire la prédiction via le modèle MLflow
                prediction = model.predict(input_data)
                st.success(f"La consommation énergétique prévue est de {prediction[0]:.2f} MWh")

                # Récupérer les informations système
                cpu_usage, memory_usage = get_system_usage()

                # Log du résultat de la prédiction avec les inputs utilisateur
                log_data.update({
                    "event": "model_execution",
                    "model_name": "BestEstimator",
                    "model_version": "1.0.0",
                    "status": "completed",
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage,
                    "details": {
                        "predicted_energy": prediction[0],
                        "inputs": {
                            "temp_max": temp_max,
                            "temp_min": temp_min,
                            "wind_speed": wind_speed,
                            "humidity": humidity,
                            "visibility": visibility,
                            "cloud_coverage": cloud_coverage
                        }
                    },
                    "log_level": "INFO"
                })

        except Exception as e:
            # En cas d'erreur, définir les valeurs par défaut pour éviter l'UnboundLocalError
            cpu_usage, memory_usage = 0, 0

            # Log en cas d'erreur
            log_data.update({
                "event": "model_execution",
                "model_name": "BestEstimator",
                "model_version": "1.0.0",
                "status": "failed",
                "error_message": str(e),
                "error_type": type(e).__name__,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "log_level": "ERROR"
            })

        send_log_to_elastic(log_data)

