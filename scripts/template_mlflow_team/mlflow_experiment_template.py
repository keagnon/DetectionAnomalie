# Prérequis:
# 1. Créez un environnement virtuel Python :
#    python -m venv mlflow-env
# 2. Activez l'environnement virtuel :
#    - Sur Windows : mlflow-env\Scripts\activate
#    - Sur Linux/Mac : source mlflow-env/bin/activate
# 3. Installez les bibliothèques nécessaires :
#    pip install mlflow scikit-learn python-dotenv
# 4. Assurez-vous que le serveur MLflow est configuré et fonctionne.
#    Si vous avez configuré MLflow avec un backend SQLite et un bucket GCS, assurez-vous que tout est en place.

import os
from dotenv import load_dotenv  # Ajoutez cette ligne
import mlflow
from mlflow import MlflowClient
from mlflow_utils import create_mlflow_experiment, get_mlflow_experiment
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def optimize_model(model, param_grid, X_train, y_train):
    """
    Optimiser un modèle avec GridSearchCV.
    ::params
        model: Modèle à optimiser
        param_grid: Grille des hyperparamètres
        X_train: Features d'entraînement
        y_train: Target d'entraînement

    """
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    return best_model, grid_search.best_params_

if __name__ == "__main__":
    mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))

    # Création ou récupération d'une expérience MLflow
    experiment_id = create_mlflow_experiment(
        experiment_name="MlflowTeamTemplate",  # Nom de l'expérience
        artifact_location=os.getenv('MLFLOW_ARTEFACTS_LOCATION'),  # Emplacement pour stocker les artefacts
        tags={"env": "dev", "version": "1.0.0"}  # Tags optionnels
    )

    client = MlflowClient()

    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

    # Définition des hyperparamètres pour chaque modèle
    rf_params = {'n_estimators': [100, 200], 'max_depth': [8, 10, None]}
    lr_params = {'C': [0.1, 1, 10]}
    gb_params = {'n_estimators': [100, 200], 'learning_rate': [0.05, 0.1]}

    # Random Forest Classifier
    with mlflow.start_run(run_name="logging_models_rf", experiment_id=experiment_id):
        mlflow.sklearn.autolog()  # Auto-enregistrement des paramètres, métriques, et modèle
        rf_model = RandomForestClassifier(random_state=42)
        best_rf, best_rf_params = optimize_model(rf_model, rf_params, X_train, y_train)
        y_pred_rf = best_rf.predict(X_test)
        mlflow.log_params(best_rf_params)
        mlflow.log_metric("accuracy_rf", accuracy_score(y_test, y_pred_rf))

    # Logistic Regression
    with mlflow.start_run(run_name="logging_models_lr", experiment_id=experiment_id):
        mlflow.sklearn.autolog()
        lr_model = LogisticRegression(random_state=42, max_iter=200)
        best_lr, best_lr_params = optimize_model(lr_model, lr_params, X_train, y_train)
        y_pred_lr = best_lr.predict(X_test)
        mlflow.log_params(best_lr_params)
        mlflow.log_metric("accuracy_lr", accuracy_score(y_test, y_pred_lr))

    # Gradient Boosting Classifier
    with mlflow.start_run(run_name="logging_models_gb", experiment_id=experiment_id):
        mlflow.sklearn.autolog()
        gb_model = GradientBoostingClassifier(random_state=42)
        best_gb, best_gb_params = optimize_model(gb_model, gb_params, X_train, y_train)
        y_pred_gb = best_gb.predict(X_test)
        mlflow.log_params(best_gb_params)
        mlflow.log_metric("accuracy_gb", accuracy_score(y_test, y_pred_gb))

    # Étape 5: Créer une version de modèle enregistrée
    # Remplacez source et run_id par les valeurs spécifiques à votre run et artefact
    #source=f"{os.getenv('MLFLOW_ARTEFACTS_LOCATION')}/artifacts/best_estimator"
    #run_id = "run_id_à_remplacer_par_votre_run_id"

    # model_name = "logging_models_rf_choosen"
    # client.create_registered_model(model_name)  # Crée un modèle enregistré
    # client.create_model_version(name=model_name, source=source, run_id=run_id)  # Crée une version du modèle
    # client.transition_model_version_stage(name=model_name, version=1, stage="Production")  # Passe en production
