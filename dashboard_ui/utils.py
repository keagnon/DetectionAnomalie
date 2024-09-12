"""
Module utilitaire pour les fonctions réutilisables dans l'application.
Contient les fonctions pour charger les styles CSS et configurer les credentials Google Cloud.
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def local_css(file_name):
    """
    Charge et applique un fichier CSS pour styliser l'application.

    Args:
        file_name (str): Chemin vers le fichier CSS.
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def configure_google_credentials():
    """
    Configure les credentials Google Cloud à partir des variables d'environnement.
    """
    google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if google_credentials:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
