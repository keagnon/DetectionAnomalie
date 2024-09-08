import mlflow
from dotenv import load_dotenv
import os
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer MLflow
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)
else:
    print("Warning: MLFLOW_TRACKING_URI non défini dans .env")

# Configurer les credentials Google Cloud
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
else:
    print("Warning: GOOGLE_APPLICATION_CREDENTIALS non défini dans .env")
# Spécifie l'ID de l'expérience supprimée
experiment_id = 0

# Restaurer l'expérience
mlflow.tracking.MlflowClient().restore_experiment(experiment_id)

print(f"L'expérience {experiment_id} a été restaurée.")
