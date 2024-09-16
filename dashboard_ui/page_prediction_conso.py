import os
import mlflow
import pandas as pd
import streamlit as st
from datetime import datetime
from utils import configure_google_credentials, local_css

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

    Returns:
        Un modèle MLflow chargé.
    """
    logged_model = "runs:/df3f426ffdc248cdb89089905b2bf8ad/random_forest_model"
    return mlflow.pyfunc.load_model(logged_model)

def show_prediction_conso():
    """
    Affiche la page de prédiction de la consommation journalière avec mouvements sociaux.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("⚡ Prédiction d'énergie consommée ")
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Dans cette section, nous faisons la prédiction en prenant en compte les mouvements sociaux.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Interface utilisateur pour entrer les données de prédiction
    col1, col2 = st.columns(2)

    with col1:
        date_input = st.date_input("Choisissez une date", datetime.now())
        selected_month = date_input.month
        selected_day_of_week = date_input.weekday()
        st.markdown("<br>", unsafe_allow_html=True)
        region_input = st.selectbox("Choisissez une région", regions_list)

    with col2:
        social_movement_input = st.selectbox(
            "Y a-t-il un mouvement social ?", options=[0, 1]
        )
        st.markdown("<br>", unsafe_allow_html=True)
        moyenne_conso_horaire = st.number_input(
            "Entrez la plage horaire souhaitée (0-23h59)",
            min_value=0.0,
            max_value=23.59,
            value=0.0,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

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

            prediction = model.predict(input_data)
            st.success(f"Consommation journalière prédite : {prediction[0]:.2f} kWh")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/1146/1146884.png",
        width=100,
        caption="Prédiction Mouvements Sociaux",
    )

show_prediction_conso()
