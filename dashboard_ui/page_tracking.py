"""
Module pour afficher la page de tracking et ouvrir l'interface utilisateur de MLflow.
"""

import os

import streamlit as st
import webbrowser
from utils import configure_google_credentials, local_css

local_css("styles.css")
configure_google_credentials()


def open_mlflow_ui():
    """
    Ouvre l'interface utilisateur MLflow dans un nouvel onglet du navigateur.
    """
    url = os.getenv("MLFLOW_TRACKING_URI")
    if url:
        webbrowser.open_new_tab(url)
    else:
        st.error("L'URL de MLflow n'est pas définie.")


def show_tracking_page():
    """
    Affiche la page de tracking dans l'application Streamlit.
    """
    st.title("Tracking des Expériences MLflow")
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Vous pouvez suivre les métriques et les performances des modèles ici.")
