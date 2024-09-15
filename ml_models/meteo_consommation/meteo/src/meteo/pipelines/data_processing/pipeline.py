from kedro.pipeline import Pipeline, node
from .nodes import preprocess_energy_data

def create_pipeline(**kwargs) -> Pipeline:
    """
    Crée un pipeline Kedro qui exécute le prétraitement des données énergétiques.

    Le pipeline se compose d'un seul nœud qui applique la fonction `preprocess_energy_data`
    pour nettoyer et transformer les données énergétiques.

    Args:
        **kwargs: Arguments supplémentaires pouvant être fournis pour configurer le pipeline.

    Returns:
        Pipeline: Un objet `Pipeline` de Kedro, comprenant un nœud qui exécute la fonction 
        `preprocess_energy_data`.
    """
    return Pipeline(
        [
            node(
                func=preprocess_energy_data,
                inputs="energy_data",
                outputs="preprocessed_energy_data",
                name="preprocess_energy_data_node",
            ),
        ]
    )
