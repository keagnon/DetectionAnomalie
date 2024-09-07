import streamlit as st
import pandas as pd
import numpy as np
import base64
from datetime import datetime
from streamlit_navigation_bar import st_navbar
import plotly.express as px


# Fonction pour faire la prédiction météorologique (simulation ici)
def predict_meteo(temp_max, temp_min, wind_speed, humidity, visibility, cloud_coverage):
    return np.random.randint(5000, 15000)  # Juste une simulation pour l'exemple

# Fonction pour prédiction des mouvements sociaux (simulation ici)
def predict_social_movement(param1, param2, param3):
    return np.random.choice(['Grève', 'Manifestation', 'Pas de mouvement'])  # Simulation

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# CSS pour mettre un fond noir sur toute la page
page_bg_img = f"""
<style>
/* Arrière-plan pour le conteneur principal */
[data-testid="stAppViewContainer"] > .main {{
    background-color: #F0F2F6;
    max-width: 100%;  /* Assurer que le contenu prenne toute la largeur */
    padding-left: 2rem;  /* Ajuster le padding gauche pour plus d'espace */
    padding-right: 2rem; /* Ajuster le padding droit pour plus d'espace */
}}

/* Arrière-plan pour la barre latérale */
[data-testid="stSidebar"] > div:first-child {{
    background-color: #F0F2F6;
}}

/* En-tête transparent */
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
/* Personnaliser la bordure des champs de texte */
input, textarea {{
    border: 1px solid #d9d9d9 !important;
    border-radius: 5px !important;
    padding: 8px !important;
    font-size: 16px !important;
    width: 100% !important;
}}

input:focus, textarea:focus {{
    border: 1px solid #ff4b4b !important;
    outline: none !important;
}}

/* Réglage de la barre d'outils */
[data-testid="stToolbar"] {{
    right: 2rem;
}}

/* Enlever les limites de largeur du contenu principal */
.block-container {{
    padding: 5rem 1rem 2rem 1rem;
    max-width: 80%;  /* Utiliser toute la largeur disponible */
}}

footer {{
    visibility: hidden;
}}

</style>
"""

styles = {
    "div": {
        "max-width": "60rem",  # Largeur maximale du conteneur
        "border-radius": "0.5rem",  # Bords arrondis
        "border": "2px solid white",  # Bordure blanche
        "padding": "10px",  # Espacement intérieur
        "background-color": "#F0F2F6",  # Assurer un fond clair
    },
    "span": {
        "border-radius": "0.5rem",  # Bords arrondis pour les éléments
        "color": "rgb(49, 51, 63)",  # Couleur du texte
        "margin": "0 0.125rem",  # Espacement entre les éléments
        "padding": "0.4375rem 0.625rem",  # Espacement intérieur
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",  # Fond légèrement transparent pour l'élément actif
        "border-radius": "0.5rem",  # Bords arrondis pour l'élément actif
        "padding": "0.5rem",  # Espacement intérieur pour l'élément actif
        "border": "2px solid white",  # Contour blanc autour de l'élément actif
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",  # Fond légèrement plus opaque au survol
        "border-radius": "0.5rem",  # Bords arrondis au survol
        "border": "2px solid white",  # Contour blanc lors du survol
    },
}


# Injecter le CSS dans la page
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
# Navbar pour navigation
menu = st_navbar(["Prédiction Météo", "Anomalie Détection", "Prédiction conso", "Clustering","Feedback", "Tracking"],styles=styles)
# st.markdown("""
# <div style="text-align: center; font-size: 2.5em;">
#     🔮 Dashboard de EngieWatch avec IA
# </div>
# """, unsafe_allow_html=True)

# Function to launch MLflow UI from Streamlit
def open_mlflow_ui():
    url = os.getenv("MLFLOW_TRACKING_URI")
    webbrowser.open_new_tab(url)

# 1. Prédiction Météo
if menu == "Prédiction Météo":
    st.markdown("""
        <div style="text-align: center; font-size: 2.5em;">
            🌦️ Prédiction Météo
        </div>
        """, unsafe_allow_html=True)
    #st.header("🌦️ Prédiction Météo")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

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

# 2. Anomalie Détection
elif menu == "Anomalie Détection":
    st.markdown("""
    <div style="text-align: center; font-size: 2.5em;">
        🌦️ Détection d'anomalies dans la consommation énergétique
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    with st.expander("Voir les données brutes"):
        if uploaded_file is not None:
            # Lecture du fichier CSV
            df = pd.read_csv(uploaded_file)
            # Affichage des données dans un DataFrame Streamlit
            st.dataframe(df)
        else:
            st.write("Aucun fichier chargé")

    # Create donut charts for each concern
    col1, col2 = st.columns(2)

    with col1:
        fig_trust = px.pie(values=[36, 64], names=["Trust", ""], hole=0.6)
        fig_trust.update_traces(textinfo='percent+label', marker=dict(colors=['#00BFFF', '#e8e8e8']))
        fig_trust.update_layout(
            showlegend=False,
            annotations=[dict(text='36%', x=0.5, y=0.5, font_size=20, showarrow=False)],
            paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent pour le papier
            plot_bgcolor='rgba(0,0,0,0)'    # Fond transparent pour le graphique
        )
        st.plotly_chart(fig_trust, use_container_width=True)

    with col2:
        fig_privacy = px.pie(values=[28, 72], names=["Privacy", ""], hole=0.6)
        fig_privacy.update_traces(textinfo='percent+label', marker=dict(colors=['#00FF00', '#e8e8e8']))
        fig_privacy.update_layout(
            showlegend=False,
            annotations=[dict(text='28%', x=0.5, y=0.5, font_size=20, showarrow=False)],
            paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent pour le papier
            plot_bgcolor='rgba(0,0,0,0)'    # Fond transparent pour le graphique
        )
        st.plotly_chart(fig_privacy, use_container_width=True)

# 3. Prédiction Mouvements Sociaux
elif menu == "Prédiction conso":
    st.markdown("""
        <div style="text-align: center; font-size: 2.5em;">
            📊 Prédiction des Mouvements Sociaux
        </div>
        """, unsafe_allow_html=True)
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

# 4. Clustering
elif menu == "Clustering":
    st.markdown("""
        <div style="text-align: center; font-size: 2.5em;">
            🌦️ Clustering des Consommations Énergétiques avec DBSCAN
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    with st.expander("Voir les données brutes"):
        if uploaded_file is not None:
            # Lecture du fichier CSV
            df = pd.read_csv(uploaded_file)
            # Affichage des données dans un DataFrame Streamlit
            st.dataframe(df)
        else:
            st.write("Aucun fichier chargé")

# 4. Feedback Utilisateurs
elif menu == "Feedback":
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
