import streamlit as st
import webbrowser
import os

from dotenv import load_dotenv

load_dotenv()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")


# Fonction pour afficher la page de tracking
def open_mlflow_ui():
    url = os.getenv("MLFLOW_TRACKING_URI")
    webbrowser.open_new_tab(url)

def show_tracking_page():
    st.title("Tracking........")