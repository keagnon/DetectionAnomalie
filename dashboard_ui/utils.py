"""
Module utilitaire pour les fonctions réutilisables dans l'application.
Contient les fonctions pour charger les styles CSS et configurer les credentials Google Cloud.
"""

import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()



def local_css(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error(f"Le fichier {file_name} n'a pas été trouvé.")


def configure_google_credentials():
    """
    Configure les credentials Google Cloud à partir des variables d'environnement.
    """
    google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if google_credentials:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials


def preprocess_data(file_path):
    """
    Prétraite les données en chargeant un fichier CSV et en nettoyant les colonnes.

    Args:
        file_path (str): Le chemin vers le fichier CSV à traiter.

    Returns:
        tuple: Un tuple contenant le dataframe prétraité et la liste des colonnes horaires.
    """
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    hourly_columns = [f"{hour:02d}:00" for hour in range(24)]
    df[hourly_columns] = (
        df[hourly_columns]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(df[hourly_columns].mean())
    )
    df["consommation_moyenne_journalière"] = df[hourly_columns].mean(axis=1)
    return df, hourly_columns
