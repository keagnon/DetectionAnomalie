import pandas as pd
import mlflow
import os
import mlflow.sklearn
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from mlflow_utils import create_mlflow_experiment, get_mlflow_experiment
from dotenv import load_dotenv

load_dotenv()

# Configurer les credentials pour Google et MLflow
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials

mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

def preprocess_data(file_path):
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
    df.columns = df.columns.str.strip()

    df['mois'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.month
    df['jour_semaine'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.dayofweek
    df['moyenne_conso_horaire'] = df[['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
                                      '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
                                      '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']].mean(axis=1)

    df_clean = df.dropna(subset=['Consommation_journaliere'])

    return df_clean

def train_ridge_model(df_clean):
    # Définir les caractéristiques et la cible
    features = df_clean[["région", "movement_social", "mois", "jour_semaine", "moyenne_conso_horaire"]]
    target = df_clean['Consommation_journaliere']

    # Prétraitement des données
    categorical_cols = ["région"]
    numerical_cols = ['movement_social', 'mois', 'jour_semaine', 'moyenne_conso_horaire']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(), categorical_cols)
        ]
    )

    # Pipeline Ridge
    ridge_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', Ridge())
    ])

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

    # Paramètres pour la recherche en grille
    param_grid = {'model__alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}

    experiment_name = "Consommation_Energetique_Prediction"
    artifact_location = os.getenv('MLFLOW_ARTEFACTS_LOCATION')
    tags = {"env": "dev", "version": "1.0.0"}

    if not artifact_location:
        print("Warning: MLFLOW_ARTEFACTS_LOCATION non défini dans .env")

    experiment_id = create_mlflow_experiment(
        experiment_name=experiment_name,
        artifact_location=artifact_location,
        tags=tags
    )

    # Entraînement et suivi MLflow
    with mlflow.start_run(run_name="Ridge_GridSearch", experiment_id=experiment_id):
        mlflow.sklearn.autolog()

        grid_search = GridSearchCV(ridge_pipeline, param_grid, cv=5)
        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_

        # Prédire et enregistrer les métriques
        score = best_model.score(X_test, y_test)
        mlflow.log_metric("test_score", score)

        # Prédictions et calcul des métriques supplémentaires
        y_pred = best_model.predict(X_test)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        mae = mean_absolute_error(y_test, y_pred)

        # Log des métriques supplémentaires dans MLflow
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("MAE", mae)

        # Enregistrer le modèle dans MLflow
        mlflow.sklearn.log_model(best_model, "ridge_model")

        print(f"Modèle enregistré dans MLflow avec un score de {score:.2f}, RMSE: {rmse:.2f}, MAE: {mae:.2f}")
        return best_model, score, rmse, mae

def main(file_path):
    df_clean = preprocess_data(file_path)
    best_model, score, rmse, mae = train_ridge_model(df_clean)
    print(f"Modèle final avec un score de {score:.2f}, RMSE: {rmse:.2f}, MAE: {mae:.2f}")

if __name__ == "__main__":
    file_path = 'fusion_courbe_mouvement.csv'
    main(file_path)
