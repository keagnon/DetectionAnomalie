import os
import mlflow
from dotenv import load_dotenv

load_dotenv()

google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
experiment_name = "mouvement_social_prediction"


client = mlflow.tracking.MlflowClient()

# Récupérer l'expérience supprimée
experiment = client.get_experiment_by_name(experiment_name)

if experiment and experiment.lifecycle_stage == 'deleted':
    # Restaurer l'expérience
    client.restore_experiment(experiment.experiment_id)
    print(f"L'expérience '{experiment_name}' a été restaurée avec succès.")
else:
    print(f"L'expérience '{experiment_name}' est soit active, soit elle n'existe pas.")
