import streamlit as st
from datetime import datetime

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Ensuite, appelle cette fonction dans chaque page pour appliquer le style
local_css("styles.css")

def show_prediction_conso():
    st.title("Prédiction conso avec mouvement")
    # Contenu spécifique à la prédiction météo
    st.write("Ceci est la page de conso.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Mise en page avec colonnes
    col1, col2 = st.columns(2)

    with col1:
        # Sélecteur de date
        param1 = st.date_input("Choisissez une date", datetime.now())

        # Liste déroulante pour la sélection de la région
        param2 = st.selectbox("Choisissez une région",("Hauts-de-France", "Bretagne", "Centre-Val de Loire", "Grand Est", "Provence-Alpes-Côte d'Azur"))

    with col2:
        # Sélection du mouvement social (True ou False)
        param3 = st.radio(
            "Y a-t-il un mouvement social ?",
            ("True", "False")
        )

    # Bouton de prédiction
    if st.button("🔍 Prédire le Mouvement Social"):
        social_prediction = predict_social_movement(param1, param2, param3)
        st.success(f"Le mouvement social prévu est : {social_prediction}.")

    # Image d'illustration pour la prédiction sociale
    st.image("https://cdn-icons-png.flaticon.com/512/1146/1146884.png", width=100, caption="Prédiction Mouvements Sociaux")
