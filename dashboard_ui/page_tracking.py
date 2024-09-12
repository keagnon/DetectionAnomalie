"""
Module pour afficher la page de tracking et ouvrir l'interface utilisateur de MLflow.
"""

import os
import webbrowser
import streamlit as st
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def local_css(file_name):
    """
    Charge et applique un fichier CSS pour styliser l'application.

    Args:
        file_name (str): Chemin vers le fichier CSS.
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")


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
