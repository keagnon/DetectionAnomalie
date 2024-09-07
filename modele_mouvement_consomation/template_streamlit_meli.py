import streamlit as st
import pandas as pd
import numpy as np
import base64
import mlflow
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer les credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials

# Configurer MLflow pour les modèles
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

# Charger les modèles MLflow
logged_anomaly_model = 'runs:/a01b4b5c87f14c55b24cd5910fc7a874/isolation_forest_model'
anomaly_model = mlflow.pyfunc.load_model(logged_anomaly_model)

logged_dbscan_model = 'runs:/faeb99c10bb64fe2880f5d867d8b3cda/dbscan_model'
dbscan_model = mlflow.sklearn.load_model(logged_dbscan_model)

# Fonction pour prétraiter les données pour la détection d'anomalies et le clustering
def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    hourly_columns = [f'{hour:02d}:00' for hour in range(24)]
    df[hourly_columns] = df[hourly_columns].apply(pd.to_numeric, errors='coerce').fillna(df[hourly_columns].mean())
    df['consommation_moyenne_journalière'] = df[hourly_columns].mean(axis=1)
    return df, hourly_columns

# Fonction pour la prédiction météorologique (simulation ici)
def predict_meteo(temp_max, temp_min, wind_speed, humidity, visibility, cloud_coverage):
    return np.random.randint(5000, 15000)  # Juste une simulation pour l'exemple

# Fonction pour prédiction des mouvements sociaux (simulation ici)
def predict_social_movement(param1, param2, param3):
    return np.random.choice(['Grève', 'Manifestation', 'Pas de mouvement'])  # Simulation

# CSS pour la mise en page
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-color: #F0F2F6;
}}
[data-testid="stSidebar"] > div:first-child {{
    background-color: #F0F2F6;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
input, textarea {{
    border: 1px solid #d9d9d9 !important;
    border-radius: 5px !important;
}}
input:focus, textarea:focus {{
    border: 1px solid #ff4b4b !important;
    outline: none !important;
}}
.block-container {{
    padding: 5rem 1rem 2rem 1rem;
    max-width: 100%;
}}
footer {{
    visibility: hidden;
}}
</style>
"""

# Titre principal
st.title("🔮 Dashboard de EngieWatch avec IA")

# Sidebar pour la navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Aller à",
    ["Prédiction Météo", "Prédiction Mouvements Sociaux", "Détection d'Anomalies", "Clustering DBSCAN", "Feedback Utilisateurs"]
)

# 1. Prédiction Météo
if menu == "Prédiction Météo":
    st.header("🌦️ Prédiction Météo")

    col1, col2 = st.columns(2)
    with col1:
        temp_max = st.number_input("Température Max (°C)", min_value=-50.0, max_value=50.0, value=25.0)
        temp_min = st.number_input("Température Min (°C)", min_value=-50.0, max_value=50.0, value=15.0)
        wind_speed = st.number_input("Vitesse du vent (km/h)", min_value=0, max_value=200, value=10)
    with col2:
        humidity = st.number_input("Humidité (%)", min_value=0, max_value=100, value=50)
        visibility = st.number_input("Visibilité (km)", min_value=0, max_value=50, value=10)
        cloud_coverage = st.slider("Couverture Nuageuse (%)", 0, 100, 50)

    if st.button("🔍 Prédire la Consommation Énergétique"):
        prediction = predict_meteo(temp_max, temp_min, wind_speed, humidity, visibility, cloud_coverage)
        st.success(f"La consommation énergétique prévue est de {prediction} MWh.")

# 2. Prédiction Mouvements Sociaux
elif menu == "Prédiction Mouvements Sociaux":
    st.header("📊 Prédiction des Mouvements Sociaux")

    col1, col2 = st.columns(2)
    with col1:
        param1 = st.date_input("Choisissez une date", datetime.now())
        param2 = st.selectbox("Choisissez une région",("Hauts-de-France", "Bretagne", "Centre-Val de Loire", "Grand Est", "Provence-Alpes-Côte d'Azur"))
    with col2:
        param3 = st.radio("Y a-t-il un mouvement social ?", ("True", "False"))

    if st.button("🔍 Prédire le Mouvement Social"):
        social_prediction = predict_social_movement(param1, param2, param3)
        st.success(f"Le mouvement social prévu est : {social_prediction}.")

# 3. Détection d'Anomalies
elif menu == "Détection d'Anomalies":
    st.header("📉 Détection d'anomalies dans la consommation énergétique")

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if uploaded_file is not None:
        df, hourly_columns = preprocess_data(uploaded_file)

        if all(column in df.columns for column in hourly_columns):
            data = df[hourly_columns]
            df['anomaly'] = anomaly_model.predict(data)

            st.subheader("Tableau des anomalies détectées")
            selected_columns = ['date', 'région', 'consommation_moyenne_journalière', 'statut', 'anomaly']

            def highlight_anomalies(row):
                return ['background-color: red' if row.anomaly == -1 else '' for _ in row]

            st.dataframe(df[selected_columns].style.apply(highlight_anomalies, axis=1))

            anomalies_df = df[df['anomaly'] == -1]

            if not anomalies_df.empty:
                st.subheader("Visualisation des anomalies")
                selected_rows = st.multiselect(
                    "Choisissez les anomalies à afficher",
                    anomalies_df.index,
                    format_func=lambda idx: f"{anomalies_df.loc[idx, 'date']} - Région: {anomalies_df.loc[idx, 'région']}"
                )

                if selected_rows:
                    for i in selected_rows:
                        row = anomalies_df.loc[i]
                        plt.figure(figsize=(10, 5))
                        plt.plot(hourly_columns, row[hourly_columns], marker='o', color='red')
                        plt.title(f"Anomalie détectée le {row['date']} - Région : {row['région']}")
                        plt.xlabel('Heure')
                        plt.ylabel('Consommation (MWh)')
                        st.pyplot(plt)
            else:
                st.info("Aucune anomalie détectée.")
        else:
            st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")

# 4. Clustering DBSCAN
elif menu == "Clustering DBSCAN":
    st.header("🔍 Clustering des Consommations Énergétiques avec DBSCAN")

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if uploaded_file is not None:
        df, hourly_columns = preprocess_data(uploaded_file)

        if all(column in df.columns for column in hourly_columns):
            scaler = StandardScaler()
            X = scaler.fit_transform(df[hourly_columns])
            df['cluster'] = dbscan_model.fit_predict(X)

            pca = PCA(n_components=2)
            df_pca = pca.fit_transform(X)
            df['pca1'] = df_pca[:, 0]
            df['pca2'] = df_pca[:, 1]

            st.subheader("Résultats du Clustering DBSCAN")
            st.dataframe(df[['date', 'région', 'cluster']].head())

            st.subheader("Visualisation des clusters")
            plt.figure(figsize=(10, 6))
            plt.scatter(df['pca1'], df['pca2'], c=df['cluster'], cmap='viridis', s=50)
            plt.title("Clustering DBSCAN")
            plt.xlabel("PCA 1")
            plt.ylabel("PCA 2")
            plt.colorbar(label="Cluster")
            st.pyplot(plt)

            st.subheader("Points marqués comme bruit")
            noise_points = df[df['cluster'] == -1]
            st.dataframe(noise_points[['date', 'région', 'cluster']])
        else:
            st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")

# 5. Feedback Utilisateurs
elif menu == "Feedback Utilisateurs":
    st.header("💬 Feedback des Utilisateurs")

    name = st.text_input("Votre nom")
    feedback = st.text_area("Vos commentaires / suggestions")
    if st.button("Envoyer le Feedback"):
        if name and feedback:
            st.success("Merci pour votre feedback !")
        else:
            st.error("Veuillez remplir tous les champs avant de soumettre.")

# Injecter le CSS dans la page
st.markdown(page_bg_img, unsafe_allow_html=True)
