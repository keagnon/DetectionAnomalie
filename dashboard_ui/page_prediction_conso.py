"""
Module pour la prédiction de la consommation journalière d'énergie avec mouvements sociaux.
Il permet d'utiliser un modèle MLflow pour faire des prédictions basées sur les caractéristiques
fournies par l'utilisateur.
"""

from datetime import datetime
import os
import streamlit as st
import pandas as pd
import mlflow

from utils import local_css, configure_google_credentials

local_css("styles.css")
configure_google_credentials()


# Charger le jeu de données
df = pd.read_csv('fusion_courbe_mouvement.csv', delimiter=';', encoding='utf-8')
df.columns = df.columns.str.strip()

# Feature engineering
df['mois'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.month
df['jour_semaine'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.dayofweek
df['moyenne_conso_horaire'] = df[
    ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
     '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
     '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
].mean(axis=1)

# Nettoyage des données
df_clean = df.dropna(subset=['Consommation_journaliere'])


def load_model():
    """
    Charge le modèle MLflow pour la prédiction de la consommation.

    Returns:
        Un modèle MLflow chargé.
    """
    logged_model = 'runs:/df3f426ffdc248cdb89089905b2bf8ad/random_forest_model'
    return mlflow.pyfunc.load_model(logged_model)


def show_prediction_conso():
    """
    Affiche la page de prédiction de la consommation journalière avec mouvements sociaux.
    """
    st.title("⚡ Prédiction de la Consommation Journalière avec Mouvement Social")
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Ceci est la page de Prédiction de la consommation.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        date_input = st.date_input("Choisissez une date", datetime.now())
        selected_month = date_input.month
        selected_day_of_week = date_input.weekday()
        st.markdown("<br>", unsafe_allow_html=True)
        region_input = st.selectbox("Choisissez une région", df_clean['région'].unique())

    with col2:
        social_movement_input = st.selectbox("Y a-t-il un mouvement social ?", options=[0, 1])
        st.markdown("<br>", unsafe_allow_html=True)
        moyenne_conso_horaire = st.number_input(
            "Entrez la moyenne de consommation horaire",
            min_value=0.0, max_value=10000.0, value=0.0
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍 Prédire la Consommation"):
        with st.spinner("Prédiction en cours..."):
            model = load_model()
            input_data = pd.DataFrame({
                'région': [region_input],
                'movement_social': [social_movement_input],
                'mois': [selected_month],
                'jour_semaine': [selected_day_of_week],
                'moyenne_conso_horaire': [moyenne_conso_horaire]
            })

            prediction = model.predict(input_data)
            st.success(f"Consommation journalière prédite : {prediction[0]:.2f} kWh")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/1146/1146884.png",
        width=100,
        caption="Prédiction Mouvements Sociaux"
    )
