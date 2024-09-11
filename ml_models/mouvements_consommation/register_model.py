import os
import mlflow
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv

load_dotenv()

google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if google_credentials:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
else:
    print("Warning: GOOGLE_APPLICATION_CREDENTIALS non défini dans .env")


mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
mlflow.set_tracking_uri(mlflow_tracking_uri)

client = MlflowClient()

model_name = "clustering_dbscan_choosen"
run_id = "096e31c04a7e4beaa1054645122fc825"
source = f"{os.getenv('MLFLOW_ARTEFACTS_LOCATION')}/artifacts/best_estimator"

try:
    client.get_registered_model(model_name)
    print(f"Le modèle '{model_name}' existe déjà.")
except mlflow.exceptions.RestException:
    client.create_registered_model(model_name)
    print(f"Modèle '{model_name}' créé.")

# Créer une version du modèle
model_version = client.create_model_version(
    name=model_name,
    source=source,
    run_id=run_id
)
print(f"Version du modèle '{model_name}' créée : Version {model_version.version}")

# Passer la version du modèle en production
client.transition_model_version_stage(
    name=model_name,
    version=model_version.version,
    stage="Production"
)
print(f"Le modèle '{model_name}' Version {model_version.version} est maintenant en Production.")
