"""
Application Streamlit pour l'analyse de la consommation d'énergie et la détection d'anomalies.

Ce module définit la structure de l'interface utilisateur et charge les pages en fonction de
la sélection dans la barre latérale.
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
from utils import local_css, configure_google_credentials
from streamlit_option_menu import option_menu

load_dotenv()
local_css("styles.css")
configure_google_credentials()

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