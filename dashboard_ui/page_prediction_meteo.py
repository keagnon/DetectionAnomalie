import numpy as np
import streamlit as st
from utils import configure_google_credentials, local_css

local_css("styles.css")
configure_google_credentials()


def show_prediction_meteo():
    """
    Affiche le formulaire de prédiction météo."""

    st.title("🌦️  Prédiction Météo")
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Ceci est la page de Prédiction Météo.")
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
        prediction = predict_meteo(
            temp_max, temp_min, wind_speed, humidity, visibility, cloud_coverage
        )
        st.success(f"La consommation énergétique prévue est de {prediction} MWh.")

    # Affichage d'une image météo pour l'esthétique
    st.image(
        "https://cdn-icons-png.flaticon.com/512/1146/1146869.png",
        width=100,
        caption="Prévision Météo",
    )


def predict_meteo(temp_max, temp_min, wind_speed, humidity, visibility, cloud_coverage):
    return np.random.randint(5000, 15000)  # Juste une simulation pour l'exemple
