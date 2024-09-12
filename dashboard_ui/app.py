"""
Application Streamlit pour l'analyse de la consommation d'énergie et la détection d'anomalies.
Ce module définit la structure de l'interface utilisateur et charge les pages en fonction de
la sélection.
"""

import os

import streamlit as st
from dotenv import load_dotenv
from page_anomalie_detection import show_anomalie_detection
from page_clustering import show_clustering
from page_feedback import show_feedback
from page_prediction_conso import show_prediction_conso
from page_prediction_meteo import show_prediction_meteo
from page_tracking import open_mlflow_ui, show_tracking_page
from streamlit_option_menu import option_menu

load_dotenv()


def local_css(file_name):
    """
    Charge et applique un fichier CSS pour styliser l'application.

    ::Params:
        file_name (str): Le chemin vers le fichier CSS.
    """
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("styles.css")

# Configurer les credentials Google Cloud
google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if google_credentials:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials

# structure de la page
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=[
            "Prédiction Météo",
            "Anomalie Détection",
            "Prédiction Consommation",
            "Clustering",
            "Feedback",
            "Tracking",
        ],
        icons=[
            "cloud-sun",
            "exclamation-triangle",
            "signal",
            "circle",
            "envelope",
            "map",
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#ffffff"},
            "icon": {"color": "#333333", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#f0f0f0",
            },
            "nav-link-selected": {"background-color": "#e74c3c", "color": "white"},
        },
    )

# Afficher la page sélectionnée
if selected == "Prédiction Météo":
    show_prediction_meteo()
elif selected == "Anomalie Détection":
    show_anomalie_detection()
elif selected == "Prédiction Consommation":
    show_prediction_conso()
elif selected == "Clustering":
    show_clustering()
elif selected == "Feedback":
    show_feedback()
elif selected == "Tracking":
    open_mlflow_ui()
    show_tracking_page()
