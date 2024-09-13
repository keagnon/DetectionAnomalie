from kedro.pipeline import Pipeline, node
from .nodes import correlation_matrix, scatter_plot, box_plot

def create_pipeline(**kwargs) -> Pipeline:
    """
    Crée un pipeline Kedro pour générer des visualisations des données prétraitées.

    Le pipeline contient trois nœuds :
    
    1. `correlation_matrix_node`: Génère une matrice de corrélation pour les données énergétiques prétraitées.
    2. `scatter_plot_node`: Crée un graphique en nuage de points pour visualiser les relations entre deux variables.
    3. `box_plot_node`: Crée un diagramme en boîte (box plot) pour montrer la distribution des variables dans les données.

    Chaque nœud prend les données énergétiques prétraitées en entrée et génère une visualisation 
    selon le type de graphique.

    Args:
        **kwargs: Arguments supplémentaires pour la configuration du pipeline.

    Returns:
        Pipeline: Un objet `Pipeline` de Kedro, constitué de trois nœuds pour générer des visualisations.
    """
    return Pipeline(
        [
            node(
                func=correlation_matrix,
                inputs=["preprocessed_energy_data", "params:correlation_output_path"],
                outputs=None,
                name="correlation_matrix_node",
            ),
            node(
                func=scatter_plot,
                inputs=["preprocessed_energy_data", "params:scatter_output_path"],
                outputs=None,
                name="scatter_plot_node",
            ),
            node(
                func=box_plot,
                inputs=["preprocessed_energy_data", "params:box_output_path"],
                outputs=None,
                name="box_plot_node",
            ),
        ]
    )
