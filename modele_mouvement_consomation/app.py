import streamlit as st
import pandas as pd
import mlflow
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer les credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials

# Configurer MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

# Charger le modèle MLflow
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

# Interface Streamlit
st.title("Détection d'anomalies dans la consommation énergétique")

# Télécharger le fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Charger et prétraiter les données
    df, hourly_columns = preprocess_data(uploaded_file)

    if all(column in df.columns for column in hourly_columns):
        # Effectuer la prédiction des anomalies
        data = df[hourly_columns]
        df['anomaly'] = loaded_model.predict(data)

        # Afficher les données avec anomalies en rouge
        st.subheader("Tableau des anomalies détectées")
        selected_columns = ['date', 'région', 'consommation_moyenne_journalière', 'statut', 'anomaly']

        # Appliquer du style pour mettre en évidence les anomalies
        def highlight_anomalies(row):
            return ['background-color: red' if row.anomaly == -1 else '' for _ in row]

        st.dataframe(df[selected_columns].style.apply(highlight_anomalies, axis=1))

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
