from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv
import pandas as pd
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Chargement des données
data = pd.read_csv('/home/adib/DetectionAnomalie/meteo/data/03_primary/preprocessed_energy_data.csv')

# Conversion des colonnes entières en flottants pour éviter les problèmes de valeurs manquantes
data = data.astype({'TempMax_Deg': 'float64', 'TempMin_Deg': 'float64', 'Wind_kmh': 'float64', 
                    'Wet_percent': 'float64', 'Visibility_km': 'float64', 'CloudCoverage_percent': 'float64'})

# Division des données
X = data[['TempMax_Deg', 'TempMin_Deg', 'Wind_kmh', 'Wet_percent', 'Visibility_km', 'CloudCoverage_percent']]
y = data['Consommation journalière (MWh - PCS 0°C)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialisation du client MLflow
experiment_id = 6
client = MlflowClient()

# Entraînement du modèle Random Forest Regressor
def train_and_evaluate_random_forest(X_train, X_test, y_train, y_test):
    with mlflow.start_run(run_name="Random Forest Regressor", experiment_id=experiment_id) as run:
        mlflow.sklearn.autolog()  # Enregistrement automatique des paramètres et des métriques

        # Initialisation du modèle
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)

        # Prédictions
        y_pred = rf_model.predict(X_test)

        # Calcul des métriques
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        r2 = r2_score(y_test, y_pred)

        # Log des métriques
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        print(f"RMSE: {rmse}")
        print(f"R²: {r2}")

# Entraîner et évaluer le modèle Random Forest
train_and_evaluate_random_forest(X_train, X_test, y_train, y_test)



