import os
import numpy as np
import pandas as pd
import mlflow
import streamlit as st
from dotenv import load_dotenv
import webbrowser

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'URI de suivi MLflow
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# Fonction pour ouvrir l'interface MLflow
def open_mlflow_ui():
    url = os.getenv("MLFLOW_TRACKING_URI")
    webbrowser.open_new_tab(url)

# Charger le modèle depuis MLflow
def load_model():
    
    logged_model = 'runs:/b1b9458f76a245e192fca44a3c1d22cc/best_estimator'
    return mlflow.pyfunc.load_model(logged_model)

# Interface Streamlit
st.title(" 🌦️ Prédiction de la Consommation Énergétique")
st.sidebar.title("Réglages")

# Bouton pour ouvrir MLflow UI
if st.sidebar.button("Voir le tracking sur MLflow"):
    open_mlflow_ui()

# Entrées utilisateur pour les caractéristiques météorologiques
temp_max = st.number_input("🌡️Température Max (°C)", min_value=-50.0, max_value=50.0, value=25.0)
temp_min = st.number_input("🌡️Température Min (°C)", min_value=-50.0, max_value=50.0, value=15.0)
wind_speed = st.number_input(" 💨 Vitesse du vent (km/h)", min_value=0, max_value=200, value=10)
humidity = st.number_input("💧 Humidité (%)", min_value=0, max_value=100, value=50)
visibility = st.number_input("👁️ Visibilité (km)", min_value=0, max_value=50, value=10)
cloud_coverage = st.slider("☁️ Couverture Nuageuse (%)", 0, 100, 50)

# Bouton de prédiction
if st.button("Prédire"):
    with st.spinner("Chargement du modèle et prédiction en cours..."):
        # Charger le modèle
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
        
        # Convertir les types de données en float64
        input_data = input_data.astype(float)
        
        # Faire la prédiction
        prediction = model.predict(input_data)
        st.success(f"La consommation énergétique prévue est de {prediction[0]:.2f} MWh")
