import os
import numpy as np
import pandas as pd
import mlflow
import streamlit as st
from dotenv import load_dotenv
import webbrowser
from utils import configure_google_credentials, local_css

load_dotenv()
local_css("styles.css")
configure_google_credentials()

def load_model():
    logged_model = 'runs:/b1b9458f76a245e192fca44a3c1d22cc/best_estimator'
    return mlflow.pyfunc.load_model(logged_model)

def show_prediction_meteo():
    """
    Affiche le formulaire de prédiction météo avec MLflow intégré pour la prédiction énergétique.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("🌦️ Prédiction d'énergie consommée")
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Dans cette section, nous faisons la prédiction en prenant en compte ds conditions métérologiques.")
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

    # Bouton de prédiction
    if st.button("🔍 Prédire la Consommation Énergétique"):
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
            st.success(f"La consommation énergétique prévue est de {prediction[0]:.2f} MWh.")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/1146/1146869.png",
        width=100,
        caption="Prévision Météo",
    )

