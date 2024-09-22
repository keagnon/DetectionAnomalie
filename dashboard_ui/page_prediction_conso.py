"""
Affiche l'interface de prédiction de la consommation d'énergie en tenant compte des mouvements sociaux.

- Permet de saisir des données utilisateur (région, mouvement social, etc.) pour la prédiction.
- Effectue une prédiction via un modèle RandomForest.
- Affiche le résultat de la prédiction et log les détails (entrée utilisateur, consommation prédite, utilisation CPU/mémoire) dans Elasticsearch.
- Gère les erreurs et log les exceptions en cas d'échec.

"""
import os
import mlflow
import pandas as pd
import streamlit as st
import psutil
import time
from datetime import datetime
from utils import configure_google_credentials, local_css, preprocess_data
from utils import send_log_to_elastic, get_system_usage
import psutil
from datetime import datetime
from elasticsearch import Elasticsearch


local_css("styles.css")
configure_google_credentials()

regions_list = [
    "Hauts-de-France", "Bretagne", "Centre-Val de Loire", "Grand Est",
    "Provence-Alpes-Côte d'Azur", "Occitanie", "Normandie", "Nouvelle-Aquitaine",
    "Pays de la Loire", "Île-de-France", "Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté"
]

moyenne_conso_horaire = 0.0

def load_model():
    """
    Charge le modèle MLflow pour la prédiction de la consommation.

    Retourne:
        Un modèle MLflow chargé.
    """
    logged_model = 'runs:/5b7b79817fae4f79932eaf8285ee593e/ridge_model'
    return mlflow.pyfunc.load_model(logged_model)

def show_prediction_conso():
    """
    Affiche la page de prédiction de la consommation journalière avec mouvements sociaux.
    """
    start_time = time.time()  # Démarre le chronométrage
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("⚡ Prédiction d'énergie consommée ")
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Dans cette section, nous faisons la prédiction en prenant en compte les mouvements sociaux.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # UI pour entrer les données de prédiction
    col1, col2 = st.columns(2)

    with col1:
        date_input = st.date_input("Choisissez une date", datetime.now())
        selected_month = date_input.month
        selected_day_of_week = date_input.weekday()
        st.markdown("<br>", unsafe_allow_html=True)
        region_input = st.selectbox("Choisissez une région", regions_list)

    with col2:
        social_movement_input = st.checkbox("Y a-t-il un mouvement social ?")
        st.markdown("<br>", unsafe_allow_html=True)
        moyenne_conso_horaire = st.number_input(
            "Entrez la plage horaire souhaitée (0-23h59)",
            min_value=0.0,
            max_value=23.59,
            value=0.0,
        )


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Vérification avant de permettre la prédiction
    if moyenne_conso_horaire >= 24:
        st.error("La valeur de la plage horaire ne peut pas dépasser 23h59.")
    else:
        # Prédiction lorsque l'utilisateur clique sur le bouton
        if st.button("🔍 Prédire la Consommation"):
            with st.spinner("Prédiction en cours..."):
                model = load_model()

                input_data = pd.DataFrame(
                    {
                        "région": [region_input],
                        "movement_social": [social_movement_input],
                        "mois": [selected_month],
                        "jour_semaine": [selected_day_of_week],
                        "moyenne_conso_horaire": [moyenne_conso_horaire],
                    }
                )

                try:
                    prediction = model.predict(input_data)
                    st.success(f"Consommation journalière prédite : {prediction[0]:.2f} kWh")

                    end_time = time.time()
                    response_time = end_time - start_time
                    cpu_usage, memory_usage = get_system_usage()

                    # Création du log complet pour Elasticsearch
                    log_data = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "event": "model_execution",
                        "model_name": "RandomForest",
                        "model_version": "1.0.0",
                        "application_name": "PredictionConsoApp",
                        "status": "completed",
                        "response_time": response_time,
                        "cpu_usage": cpu_usage,
                        "memory_usage": memory_usage,
                        "details": {
                            "inputs": {
                                "region": region_input,
                                "social_movement": 1 if social_movement_input else 0,
                                "month": selected_month,
                                "day_of_week": selected_day_of_week,
                                "moyenne_conso_horaire": moyenne_conso_horaire
                            },
                            "predicted_consumption": prediction[0]
                        },
                        "log_level": "INFO"
                    }

                except Exception as e:
                    end_time = time.time()
                    response_time = end_time - start_time

                    # Log en cas d'échec
                    log_data = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "event": "model_execution",
                        "model_name": "RandomForest",
                        "model_version": "1.0.0",
                        "application_name": "PredictionConsoApp",
                        "status": "failed",
                        "response_time": response_time,
                        "error_message": str(e),
                        "error_type": type(e).__name__,
                        "cpu_usage": cpu_usage,
                        "memory_usage": memory_usage,
                        "details": {
                            "inputs": {
                                "region": region_input,
                                "social_movement": 1 if social_movement_input else 0,
                                "month": selected_month,
                                "day_of_week": selected_day_of_week,
                                "moyenne_conso_horaire": moyenne_conso_horaire
                            },
                            "predicted_consumption": None
                        },
                        "log_level": "ERROR"
                    }

                # Envoi du log à Elasticsearch
                send_log_to_elastic(log_data)

    st.image(
        "https://cdn-icons-png.flaticon.com/512/1146/1146884.png",
        width=100,
        caption="Prédiction Mouvements Sociaux",
    )
