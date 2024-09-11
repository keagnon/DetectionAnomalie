import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score
from dotenv import load_dotenv
import os
import subprocess
import webbrowser
from datetime import datetime

load_dotenv()

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
mlflow.set_experiment("Prediction_des_mouvements_sociaux")

df = pd.read_csv('../data_test/fusion_courbe_mouvement.csv', delimiter=';', encoding='utf-8')
df.columns = df.columns.str.strip()
 
# Feature engineering
df['mois'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.month
df['jour_semaine'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.dayofweek
df['moyenne_conso_horaire'] = df[['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
                                  '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
                                  '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']].mean(axis=1)

df_clean = df.dropna(subset=['Consommation_journaliere'])

features = df_clean[["région", "movement_social", "mois", "jour_semaine", "moyenne_conso_horaire"]]
target = df_clean['Consommation_journaliere']
 
# Preprocessing des données
categorical_cols = ["région"]
numerical_cols = ['movement_social', 'mois', 'jour_semaine', 'moyenne_conso_horaire']
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(), categorical_cols)
    ]
)

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

def train_model(exp_name, n_estimators):
    experiment = mlflow.set_experiment(exp_name)
    with mlflow.start_run(experiment_id=experiment.experiment_id):
        # Random Forest model
        rf_model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestRegressor(n_estimators=n_estimators, random_state=42))
        ])
        rf_model.fit(X_train, y_train)
        y_pred_rf = rf_model.predict(X_test)
        mse_rf = mean_squared_error(y_test, y_pred_rf)
        r2_rf = r2_score(y_test, y_pred_rf)
        # Log des metrics
        mlflow.log_param("n_estimators_rf", n_estimators)
        mlflow.log_metric("mse_rf", mse_rf)
        mlflow.log_metric("r2_rf", r2_rf)
        mlflow.sklearn.log_model(rf_model, "random_forest_model")
 
    return mse_rf, r2_rf

def open_mlflow_ui():
    """Opuvrir l'interface utilisateur de MLflow dans un navigateur"""
    url = os.getenv("MLFLOW_TRACKING_URI")
    webbrowser.open_new_tab(url)

def load_model():
    """Charger le modèle MLflow"""
    logged_model = 'runs:/df3f426ffdc248cdb89089905b2bf8ad/random_forest_model'
    return mlflow.pyfunc.load_model(logged_model)

tab1, tab2 = st.tabs(["Entraîner le Modèle", "Faire une Prédiction"])

st.sidebar.title("Réglages")
n_estimators_rf = st.sidebar.slider('Nombre d\'arbres (n_estimators)', 10, 200, step=10, value=100)
if st.sidebar.button("Voir le tracking sur MLflow"):
    open_mlflow_ui()
 
# Onglet 1 : Entraînement du modèle
with tab1:
    st.title("Entraînement du Modèle")
    if st.button("Entraîner les Modèles"):
        with st.spinner("Entraînement en cours..."):
            mse_rf, r2_rf = train_model("Prediction_des_mouvements_sociaux", n_estimators_rf)
        st.success("Entraînement terminé !")
        st.write(f"Random Forest - MSE: {mse_rf:.3f}, R²: {r2_rf:.3f}")
 
# Onglet 2 : Prédiction
with tab2:
    st.title("Prédiction de la Consommation Journalière")

    date_input = st.date_input("Sélectionnez une date", value=datetime.now())
    selected_month = date_input.month
    selected_day_of_week = date_input.weekday()

    region_input = st.selectbox("Sélectionnez une région", options=df_clean['région'].unique())
    social_movement_input = st.selectbox("Y a-t-il un mouvement social ?", options=[0, 1])
    moyenne_conso_horaire = st.number_input("Entrez la moyenne de consommation horaire", min_value=0.0, max_value=10000.0, value=0.0)

    if st.button("Prédire"):
        with st.spinner("Prédiction en cours..."):
            model = load_model()
            input_data = pd.DataFrame({
                'région': [region_input],
                'movement_social': [social_movement_input],
                'mois': [selected_month],
                'jour_semaine': [selected_day_of_week],
                'moyenne_conso_horaire': [moyenne_conso_horaire]
            })

            prediction = model.predict(input_data)
            st.success(f"Consommation journalière prédite : {prediction[0]:.2f} kWh")