import streamlit as st
import pandas as pd
import numpy as np

# Fonction pour faire la prédiction météorologique (simulation ici)
def predict_meteo(temp_max, temp_min, wind_speed, humidity, visibility, cloud_coverage):
    return np.random.randint(5000, 15000)  # Juste une simulation pour l'exemple

# Fonction pour prédiction des mouvements sociaux (simulation ici)
def predict_social_movement(param1, param2, param3):
    return np.random.choice(['Grève', 'Manifestation', 'Pas de mouvement'])  # Simulation

# Interface Streamlit
st.set_page_config(page_title="Prévision avec IA", layout="wide", initial_sidebar_state="expanded")

# Définir des styles personnalisés
st.markdown(
    """
    <style>
    .main { background-color: #F0F2F6; }
    footer {visibility: hidden;}
    .css-18e3th9 { padding: 5rem 1rem 2rem 1rem; }
    </style>
    """, unsafe_allow_html=True
)

# Titre principal
st.title("🔮 Dashboard de Prédictions avec IA")

# Sidebar pour la navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Aller à",
    ["Prédiction Météo", "Prédiction Mouvements Sociaux", "Feedback Utilisateurs"]
)

# 1. Prédiction Météo
if menu == "Prédiction Météo":
    st.header("🌦️ Prédiction Météo")
    
    # Mise en page avec colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        temp_max = st.number_input("Température Max (°C)", min_value=-50.0, max_value=50.0, value=25.0)
        temp_min = st.number_input("Température Min (°C)", min_value=-50.0, max_value=50.0, value=15.0)
        wind_speed = st.number_input("Vitesse du vent (km/h)", min_value=0, max_value=200, value=10)
    
    with col2:
        humidity = st.number_input("Humidité (%)", min_value=0, max_value=100, value=50)
        visibility = st.number_input("Visibilité (km)", min_value=0, max_value=50, value=10)
        cloud_coverage = st.slider("Couverture Nuageuse (%)", 0, 100, 50)
    
    # Bouton de prédiction
    if st.button("🔍 Prédire la Consommation Énergétique"):
        prediction = predict_meteo(temp_max, temp_min, wind_speed, humidity, visibility, cloud_coverage)
        st.success(f"La consommation énergétique prévue est de {prediction} MWh.")
    
    # Affichage d'une image météo pour l'esthétique
    st.image("https://cdn-icons-png.flaticon.com/512/1146/1146869.png", width=100, caption="Prévision Météo")

# 2. Prédiction Mouvements Sociaux
elif menu == "Prédiction Mouvements Sociaux":
    st.header("📊 Prédiction des Mouvements Sociaux")
    
    # Mise en page avec colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        param1 = st.number_input("Paramètre Économique (ex : PIB)", value=1000)
        param2 = st.number_input("Paramètre Politique (ex : stabilité)", value=50)
    
    with col2:
        param3 = st.slider("Niveau de Satisfaction des Citoyens (%)", 0, 100, value=75)
    
    # Bouton de prédiction
    if st.button("🔍 Prédire le Mouvement Social"):
        social_prediction = predict_social_movement(param1, param2, param3)
        st.success(f"Le mouvement social prévu est : {social_prediction}.")
    
    # Image d'illustration pour la prédiction sociale
    st.image("https://cdn-icons-png.flaticon.com/512/1146/1146884.png", width=100, caption="Prédiction Mouvements Sociaux")

# 3. Feedback Utilisateurs
elif menu == "Feedback Utilisateurs":
    st.header("💬 Feedback des Utilisateurs")
    
    # Formulaire de feedback
    name = st.text_input("Votre nom")
    feedback = st.text_area("Vos commentaires / suggestions")
    if st.button("Envoyer le Feedback"):
        if name and feedback:
            st.success("Merci pour votre feedback ! Nous l'apprécions beaucoup.")
            # Simuler un enregistrement en base de données ou envoi par email
        else:
            st.error("Veuillez remplir tous les champs avant de soumettre.")
    
    # Image de feedback
    st.image("https://cdn-icons-png.flaticon.com/512/1256/1256650.png", width=100, caption="Feedback Utilisateurs")

# Footer personnalisé
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Made with ❤️</p>", unsafe_allow_html=True)
