import streamlit as st
import pandas as pd
import mlflow
import plotly.graph_objects as go
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

        # Calcul du pourcentage de lignes avec et sans anomalies
        total_rows = len(df)
        anomalies_count = len(df[df['anomaly'] == -1])
        non_anomalies_count = total_rows - anomalies_count

        anomalies_percentage = (anomalies_count / total_rows) * 100
        non_anomalies_percentage = 100 - anomalies_percentage

        # Créer une disposition avec deux colonnes
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Tableau des anomalies détectées")
            selected_columns = ['date', 'région', 'consommation_moyenne_journalière', 'statut', 'anomaly']

            # Appliquer du style pour mettre en évidence les anomalies
            def highlight_anomalies(row):
                return ['background-color: red' if row.anomaly == -1 else '' for _ in row]

            st.dataframe(df[selected_columns].style.apply(highlight_anomalies, axis=1))

        with col2:
            st.subheader("Distribution des anomalies")
            fig_anomalies = go.Figure(data=[go.Pie(labels=["Avec Anomalies", "Sans Anomalies"],
                                                   values=[anomalies_count, non_anomalies_count],
                                                   hole=.6)])
            fig_anomalies.update_traces(textinfo='percent+label',
                                        marker=dict(colors=['#FF6347', '#e8e8e8']))
            fig_anomalies.update_layout(
                showlegend=False,
                annotations=[dict(text=f'{anomalies_percentage:.1f}%', x=0.5, y=0.5, font_size=20, showarrow=False)],
                paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent pour le papier
                plot_bgcolor='rgba(0,0,0,0)'    # Fond transparent pour le graphique
            )
            st.plotly_chart(fig_anomalies, use_container_width=True)

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
                for i, row in enumerate(selected_rows):
                    anomaly_row = anomalies_df.loc[row]
                    fig = go.Figure()

                    fig.add_trace(go.Scatter(x=hourly_columns,
                                             y=anomaly_row[hourly_columns],
                                             mode='lines+markers',
                                             line=dict(color='red'),
                                             marker=dict(size=6)))
                    fig.update_layout(
                        title=f"Anomalie détectée le {anomaly_row['date']} - Région : {anomaly_row['région']}",
                        xaxis_title="Heure",
                        yaxis_title="Consommation (MWh)",
                        paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent
                        plot_bgcolor='rgba(0,0,0,0)'   # Fond transparent
                    )

                    # Display 2 charts per row
                    if i % 2 == 0:
                        col1, col2 = st.columns(2)
                        col1.plotly_chart(fig, use_container_width=True)
                    else:
                        col2.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Aucune anomalie détectée.")
    else:
        st.error("Les colonnes horaires ne sont pas toutes présentes dans le dataset.")
