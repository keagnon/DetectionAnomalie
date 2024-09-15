import os
import mlflow
from dotenv import load_dotenv

def configure_env_settings():
    """
    Charge les variables d'environnement à partir du fichier .env et configure les
    paramètres pour Google Cloud et MLflow. Si les variables ne sont pas définies,
    un message d'avertissement est affiché.

    Variables requises :
        - GOOGLE_APPLICATION_CREDENTIALS : Chemin vers les credentials Google Cloud.
        - MLFLOW_TRACKING_URI : URI de tracking pour MLflow.

    """
    load_dotenv()

    google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if google_credentials:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
    else:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS non défini dans .env")

    mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
    if mlflow_tracking_uri:
        mlflow.set_tracking_uri(mlflow_tracking_uri)
    else:
        print("Warning: MLFLOW_TRACKING_URI non défini dans .env")
