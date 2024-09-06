# import os
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
# from sklearn.metrics import mean_squared_error, r2_score
# import mlflow
# import mlflow.sklearn
# from mlflow.tracking import MlflowClient
# from dotenv import load_dotenv

# # Charger les variables d'environnement depuis le fichier .env
# load_dotenv()

# # Chargement des données
# data = pd.read_csv('/home/adib/DetectionAnomalie/meteo/data/03_primary/preprocessed_energy_data.csv')

# # Conversion des colonnes entières en flottants pour éviter les problèmes de valeurs manquantes
# data = data.astype({'TempMax_Deg': 'float64', 'TempMin_Deg': 'float64', 'Wind_kmh': 'float64', 
#                     'Wet_percent': 'float64', 'Visibility_km': 'float64', 'CloudCoverage_percent': 'float64'})

# # Division des données
# X = data[['TempMax_Deg', 'TempMin_Deg', 'Wind_kmh', 'Wet_percent', 'Visibility_km', 'CloudCoverage_percent']]
# y = data['Consommation journalière (MWh - PCS 0°C)']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Définir l'URI de suivi MLflow
# mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
# if mlflow_tracking_uri is None:
#     raise ValueError("MLFLOW_TRACKING_URI is not set. Please define it in your .env file.")

# # Initialisation du client MLflow
# experiment_id= 6
# client = MlflowClient()

# # Entraînement et logging du modèle Random Forest Regressor
# with mlflow.start_run(run_name="Random Forest Regressor", experiment_id=experiment_id) as run:
#     mlflow.sklearn.autolog()
#     rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
#     rf_model.fit(X_train, y_train)
#     y_pred_rf = rf_model.predict(X_test)
#     rf_rmse = mean_squared_error(y_test, y_pred_rf, squared=False)
#     rf_r2 = r2_score(y_test, y_pred_rf)
#     mlflow.log_metric("rmse", rf_rmse)
#     mlflow.log_metric("r2", rf_r2)

# # Entraînement et logging du modèle Linear Regression
# with mlflow.start_run(run_name="Linear Regression", experiment_id=experiment_id) as run:
#     mlflow.sklearn.autolog()
#     lr_model = LinearRegression()
#     lr_model.fit(X_train, y_train)
#     y_pred_lr = lr_model.predict(X_test)
#     lr_rmse = mean_squared_error(y_test, y_pred_lr, squared=False)
#     lr_r2 = r2_score(y_test, y_pred_lr)
#     mlflow.log_metric("rmse", lr_rmse)
#     mlflow.log_metric("r2", lr_r2)

# # Entraînement et logging du modèle Gradient Boosting Regressor
# with mlflow.start_run(run_name="Gradient Boosting Regressor", experiment_id=experiment_id) as run:
#     mlflow.sklearn.autolog()
#     gbr_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
#     gbr_model.fit(X_train, y_train)
#     y_pred_gbr = gbr_model.predict(X_test)
#     gbr_rmse = mean_squared_error(y_test, y_pred_gbr, squared=False)
#     gbr_r2 = r2_score(y_test, y_pred_gbr)
#     mlflow.log_metric("rmse", gbr_rmse)
#     mlflow.log_metric("r2", gbr_r2)
# import os
# import pandas as pd
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.metrics import mean_squared_error, r2_score
# import mlflow
# import mlflow.sklearn
# from mlflow.tracking import MlflowClient
# from dotenv import load_dotenv

# # Charger les variables d'environnement depuis le fichier .env
# load_dotenv()

# # Chargement des données
# data = pd.read_csv('/home/adib/DetectionAnomalie/meteo/data/03_primary/preprocessed_energy_data.csv')

# # Conversion des colonnes entières en flottants pour éviter les problèmes de valeurs manquantes
# data = data.astype({'TempMax_Deg': 'float64', 'TempMin_Deg': 'float64', 'Wind_kmh': 'float64', 
#                     'Wet_percent': 'float64', 'Visibility_km': 'float64', 'CloudCoverage_percent': 'float64'})

# # Division des données
# X = data[['TempMax_Deg', 'TempMin_Deg', 'Wind_kmh', 'Wet_percent', 'Visibility_km', 'CloudCoverage_percent']]
# y = data['Consommation journalière (MWh - PCS 0°C)']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Définir l'URI de suivi MLflow
# mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
# if mlflow_tracking_uri is None:
#     raise ValueError("MLFLOW_TRACKING_URI is not set. Please define it in your .env file.")

# # Initialisation du client MLflow
# experiment_id = 6
# client = MlflowClient()

# # Définir les hyperparamètres à tester
# param_grid = {
#     'n_estimators': [100, 200, 300],
#     'learning_rate': [0.01, 0.05, 0.1],
#     'max_depth': [3, 4, 5],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'subsample': [0.8, 1.0]
# }

# # Initialisation du modèle
# gbr = GradientBoostingRegressor(random_state=42)

# # Initialisation de GridSearchCV
# grid_search = GridSearchCV(estimator=gbr, param_grid=param_grid, cv=3, n_jobs=-1, scoring='neg_mean_squared_error', verbose=2)

# # Exécution de GridSearchCV
# with mlflow.start_run(run_name="GridSearch Gradient Boosting", experiment_id=experiment_id) as run:
#     mlflow.sklearn.autolog()
#     grid_search.fit(X_train, y_train)
    
#     # Enregistrer les meilleurs hyperparamètres
#     best_params = grid_search.best_params_
#     mlflow.log_params(best_params)

#     # Prédiction et évaluation du modèle
#     best_model = grid_search.best_estimator_
#     y_pred = best_model.predict(X_test)
#     rmse = mean_squared_error(y_test, y_pred, squared=False)
#     r2 = r2_score(y_test, y_pred)

#     # Enregistrer les métriques
#     mlflow.log_metric("rmse", rmse)
#     mlflow.log_metric("r2", r2)

#     print(f"Best Parameters: {best_params}")
#     print(f"RMSE: {rmse}")
#     print(f"R²: {r2}")


# import os
# import pandas as pd
# from sklearn.model_selection import train_test_split, RandomizedSearchCV
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.metrics import mean_squared_error, r2_score
# import mlflow
# import mlflow.sklearn
# from mlflow.tracking import MlflowClient
# from dotenv import load_dotenv

# # Charger les variables d'environnement depuis le fichier .env
# load_dotenv()

# # Chargement des données
# data = pd.read_csv('/home/adib/DetectionAnomalie/meteo/data/03_primary/preprocessed_energy_data.csv')

# # Conversion des colonnes entières en flottants pour éviter les problèmes de valeurs manquantes
# data = data.astype({'TempMax_Deg': 'float64', 'TempMin_Deg': 'float64', 'Wind_kmh': 'float64', 
#                     'Wet_percent': 'float64', 'Visibility_km': 'float64', 'CloudCoverage_percent': 'float64'})

# # Division des données
# X = data[['TempMax_Deg', 'TempMin_Deg', 'Wind_kmh', 'Wet_percent', 'Visibility_km', 'CloudCoverage_percent']]
# y = data['Consommation journalière (MWh - PCS 0°C)']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Définir l'URI de suivi MLflow
# mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
# if mlflow_tracking_uri is None:
#     raise ValueError("MLFLOW_TRACKING_URI is not set. Please define it in your .env file.")

# # Initialisation du client MLflow
# experiment_id = 6
# client = MlflowClient()

# # Entraînement du modèle Gradient Boosting Regressor
# gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, max_depth=3,
#                                 min_samples_split=2, min_samples_leaf=4, subsample=1.0, random_state=42)

# with mlflow.start_run(run_name="Gradient Boosting Regressor with Accuracy", experiment_id=experiment_id) as run:
#     mlflow.sklearn.autolog()
#     gbr.fit(X_train, y_train)
    
#     # Prédiction et évaluation du modèle
#     y_pred = gbr.predict(X_test)
#     rmse = mean_squared_error(y_test, y_pred, squared=False)
#     r2 = r2_score(y_test, y_pred)
    
#     # Calcul de l'accuracy basée sur une tolérance d'erreur
#     tolerance = 0.10  # par exemple, une tolérance de 10%
#     accuracy_within_tolerance = sum(abs(y_test - y_pred) / y_test < tolerance) / len(y_test)
    
#     # Enregistrer les métriques
#     mlflow.log_metric("rmse", rmse)
#     mlflow.log_metric("r2", r2)
#     mlflow.log_metric("accuracy_within_tolerance", accuracy_within_tolerance)
    
#     print(f"RMSE: {rmse}")
#     print(f"R²: {r2}")
#     print(f"Accuracy within {tolerance*100}% tolerance: {accuracy_within_tolerance * 100:.2f}%")


import os
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor

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

# Définition des espaces d'hyperparamètres pour chaque modèle
xgb_param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 4, 5, 6],
    'subsample': [0.8, 1.0]
}

lgb_param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 4, 5, -1],
    'num_leaves': [31, 50, 100],
    'subsample': [0.8, 1.0]
}

catboost_param_grid = {
    'iterations': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'depth': [3, 4, 5, 6],
    'l2_leaf_reg': [3, 5, 7]
}

# Fonction d'entraînement et d'évaluation
def train_and_evaluate(model, param_grid, run_name):
    with mlflow.start_run(run_name=run_name, experiment_id=experiment_id) as run:
        mlflow.sklearn.autolog()
        random_search = RandomizedSearchCV(estimator=model, param_distributions=param_grid, 
                                           n_iter=20, cv=5, verbose=2, random_state=42, n_jobs=-1)
        random_search.fit(X_train, y_train)
        
        best_model = random_search.best_estimator_
        y_pred = best_model.predict(X_test)
        
        # Calcul des métriques
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        r2 = r2_score(y_test, y_pred)
        
        # Log des métriques et des meilleurs hyperparamètres
        mlflow.log_params(random_search.best_params_)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        
        print(f"Best Parameters for {run_name}: {random_search.best_params_}")
        print(f"RMSE for {run_name}: {rmse}")
        print(f"R² for {run_name}: {r2}")

# Entraînement et évaluation pour chaque modèle

# XGBoost
train_and_evaluate(xgb.XGBRegressor(objective='reg:squarederror', random_state=42), xgb_param_grid, "XGBoost Regressor")

# LightGBM
train_and_evaluate(lgb.LGBMRegressor(random_state=42), lgb_param_grid, "LightGBM Regressor")

# CatBoost
train_and_evaluate(CatBoostRegressor(verbose=0, random_state=42), catboost_param_grid, "CatBoost Regressor")

