import streamlit as st
import pandas as pd
import numpy as np
import base64
from datetime import datetime
from streamlit_navigation_bar import st_navbar
import plotly.express as px
from dotenv import load_dotenv
import os
import subprocess
import webbrowser

import mlflow
import mlflow.sklearn

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

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

# Configurer les credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials

# Configurer MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

# Charger le modèle MLflow pour la détection d'anomalies
logged_model = 'runs:/a01b4b5c87f14c55b24cd5910fc7a874/isolation_forest_model'
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Fonction de prétraitement des données
def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)
    return df, hourly_columns

# Function to launch MLflow UI from Streamlit
def open_mlflow_ui():
    url = os.getenv("MLFLOW_TRACKING_URI")
    webbrowser.open_new_tab(url)


page_bg_img = f"""
<style>
/* Ensure the entire app container scrolls with the page */
[data-testid="stAppViewContainer"] {{
    overflow: auto;
}}
.stDataFrame div[data-testid="stHorizontalBlock"] {{
        width: 100% !important;
}}

/* Make the header scroll with the page */
[data-testid="stHeader"] {{
    position: relative !important;
    background: rgba(0,0,0,0);
    z-index: 1 !important;
    top: auto;
}}

/* Custom styling for the main container */
[data-testid="stAppViewContainer"] > .main {{
    background-color: #F0F2F6;
    max-width: 100%;
    padding-left: 2rem;
    padding-right: 2rem;
    overflow: auto;
    position: relative !important;
}}

/* Remove any fixed positioning of the toolbar */
[data-testid="stToolbar"] {{
    right: 2rem;
    position: relative !important;
}}

.block-container {{
    padding: 5rem 1rem 2rem 1rem;
    max-width: 80%;
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


# Custom CSS for the result display
st.markdown(
    """
    <style>
    .result-line {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #1f1f1f;
        color: white;
        padding: 10px;
        border-radius: 8px;
        margin: 20px 0;
    }
    .result-line .label {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .result-line .value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #66ff66;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if uploaded_file is not None:
        # Charger et prétraiter les données
        df, hourly_columns = preprocess_data(uploaded_file)

        if all(column in df.columns for column in hourly_columns):
            # Effectuer la prédiction des anomalies
            data = df[hourly_columns]
            df['anomaly'] = loaded_model.predict(data)

            # Calcul du pourcentage de lignes avec et sans anomalies
            total_rows = len(df)
            anomalies_count = len(df[df['anomaly'] == -1])
            non_anomalies_count = total_rows - anomalies_count

            anomalies_percentage = (anomalies_count / total_rows) * 100
            non_anomalies_percentage = 100 - anomalies_percentage

            ## Display results in a line format
            st.markdown(
                """
                <div class="result-line">
                    <div class="label">Nombre d'anomalie :</div>
                    <div class="value">{}</div>
                </div>
                <div class="result-line">
                    <div class="label">Nombre de lignes sans anomalie :</div>
                    <div class="value">{}</div>
                </div>
                """.format(anomalies_count, non_anomalies_count),
                unsafe_allow_html=True
            )

            selected_columns = ['date', 'région', 'consommation_moyenne_journalière', 'statut', 'anomaly']

            # Appliquer du style pour mettre en évidence les anomalies
            def highlight_anomalies(row):
                return ['background-color: red' if row.anomaly == -1 else '' for _ in row]

            st.dataframe(df[selected_columns].style.apply(highlight_anomalies, axis=1),width=1400)
            # Add italicized text below the table
            st.markdown('<div style="text-align: center;"><em>Tableau des anomalies détectées</em></div>', unsafe_allow_html=True)



            # Filtrer les lignes avec anomalies
            anomalies_df = df[df['anomaly'] == -1]

            # Laisser l'utilisateur choisir les anomalies à tracer
            if not anomalies_df.empty:
                st.subheader("Visualisation des anomalies")
                selected_rows = st.multiselect(
                    "Choisissez les anomalies à afficher",
                    anomalies_df.index,
                    format_func=lambda idx: f"{anomalies_df.loc[idx, 'date']} - Région: {anomalies_df.loc[idx, 'région']}"
                )

                if selected_rows:
                    for i, row in enumerate(selected_rows):
                        anomaly_row = anomalies_df.loc[row]
                        fig = go.Figure()

                        fig.add_trace(go.Scatter(x=hourly_columns,
                                                y=anomaly_row[hourly_columns],
                                                mode='lines+markers',
                                                line=dict(color='red'),
                                                marker=dict(size=6)))
                        fig.update_layout(
                            title=f"Anomalie détectée le {anomaly_row['date']} - Région : {anomaly_row['région']}",
                            xaxis_title="Heure",
                            yaxis_title="Consommation (MWh)",
                            paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent
                            plot_bgcolor='rgba(0,0,0,0)'   # Fond transparent
                        )

                        # Display 2 charts per row
                        if i % 2 == 0:
                            col1, col2 = st.columns(2)
                            col1.plotly_chart(fig, use_container_width=True)
                        else:
                            col2.plotly_chart(fig, use_container_width=True)

            else:
                st.info("Aucune anomalie détectée.")
        else:
            st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")

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
elif menu == "Tracking":
    open_mlflow_ui()