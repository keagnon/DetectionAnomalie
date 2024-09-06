from kedro.pipeline import Pipeline, node
from .nodes import preprocess_energy_data

def create_pipeline(**kwargs) -> Pipeline:
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
