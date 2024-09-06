# src/meteo/pipelines/data_viz/pipeline.py

from kedro.pipeline import Pipeline, node
from .nodes import correlation_matrix, scatter_plot, box_plot

def create_pipeline(**kwargs) -> Pipeline:
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
