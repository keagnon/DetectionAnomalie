import mlflow
from mlflow import MlflowClient

def create_mlflow_experiment(experiment_name, artifact_location, tags=None):
    client = MlflowClient()
    try:
        experiment_id = client.create_experiment(name=experiment_name, artifact_location=artifact_location)
        if tags:
            for key, value in tags.items():
                client.set_experiment_tag(experiment_id, key, value)
    except mlflow.exceptions.RestException:
        experiment = client.get_experiment_by_name(experiment_name)
        experiment_id = experiment.experiment_id
    return experiment_id

def get_mlflow_experiment_id(experiment_name):
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment:
        return experiment.experiment_id
    else:
        print(f"L'expérience '{experiment_name}' n'existe pas.")
        return None
