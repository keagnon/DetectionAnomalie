import os
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from catboost import CatBoostRegressor
import mlflow
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv

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

# Définition des hyperparamètres pour la recherche aléatoire
param_grid = {
    'iterations': [500, 1000, 1500],
    'learning_rate': [0.005, 0.01, 0.03],
    'depth': [4, 6, 10, 12],
    'l2_leaf_reg': [1, 3, 10, 20],
    'bagging_temperature': [0, 1, 2, 5],
    'random_strength': [0, 1, 5, 10],
    'boosting_type': ['Plain', 'Ordered'],
    'feature_border_type': ['GreedyLogSum', 'Median']
}

# Fonction d'entraînement et d'évaluation du modèle CatBoost avec RandomizedSearchCV
def train_and_evaluate_catboost(X_train, X_test, y_train, y_test, param_grid):
    with mlflow.start_run(run_name="CatBoost Regressor (Tuned)", experiment_id=experiment_id) as run:
        mlflow.sklearn.autolog()  # Enregistrer automatiquement les paramètres et les métriques

        # Initialisation du modèle CatBoost
        catboost_model = CatBoostRegressor(verbose=0, random_state=42)

        # Randomized Search pour trouver les meilleurs hyperparamètres
        random_search = RandomizedSearchCV(
            estimator=catboost_model,
            param_distributions=param_grid,
            n_iter=20,
            cv=5,
            verbose=2,
            random_state=42,
            n_jobs=-1
        )

        # Entraîner le modèle avec la recherche des hyperparamètres
        random_search.fit(X_train, y_train)

        # Meilleur modèle trouvé
        best_model = random_search.best_estimator_

        # Prédictions sur le jeu de test
        y_pred = best_model.predict(X_test)

        # Calcul des métriques
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        r2 = r2_score(y_test, y_pred)

        # Enregistrer les meilleurs hyperparamètres et métriques dans MLflow
        mlflow.log_params(random_search.best_params_)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        # Récupérer le run_id
        run_id = run.info.run_id
        print(f"Best Parameters: {random_search.best_params_}")
        print(f"RMSE: {rmse}")
        print(f"R²: {r2}")
        print(f"Run ID: {run_id}")

        # Enregistrer le modèle comme une nouvelle version dans MLflow
        model_uri = f"runs:/{run_id}/model"
        model_version = mlflow.register_model(model_uri, "CatBoostEnergyModel")

        print(f"Model registered with version: {model_version.version}")

# Entraîner et évaluer le modèle CatBoost amélioré
train_and_evaluate_catboost(X_train, X_test, y_train, y_test, param_grid)
