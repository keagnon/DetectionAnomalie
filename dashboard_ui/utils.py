"""
Module utilitaire pour les fonctions réutilisables dans l'application.
"""

import os

import pandas as pd
import streamlit as st
import psutil
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


def local_css(file_name):
    """
    Charge un fichier CSS local et l'applique à l'application Streamlit.
    """
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

    ::Params:
        file_path (str): Le chemin vers le fichier CSV à traiter.

    Retourne:
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


def send_log_to_elastic(log_data):
    """
    Envoie les logs à Elasticsearch.

    ::Params:
        log_data (dict): Dictionnaire contenant les informations de log.
    """
    es = Elasticsearch(
        [os.getenv("ELASTIC_DEPLOYMENT_ENDPOINT")],
        basic_auth=(os.getenv("ELASTIC_USERNAME"), os.getenv("ELASTIC_PASSWORD")),
    )
    es.index(index="logs_engiewatch", body=log_data)

def get_system_usage():
    """
    Récupère les statistiques d'utilisation du CPU et de la mémoire.

    Retourne:
        tuple: Taux d'utilisation du CPU et de la mémoire en pourcentage.
    """
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    return cpu_usage, memory_usage