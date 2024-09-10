"""
This is a boilerplate pipeline 'emissions_pipeline'
generated using Kedro 0.19.8
"""

from kedro.pipeline import Pipeline, pipeline,node
from .nodes import load_emissions_data, process_emissions_data, save_processed_data, load_energy_data, merge_datasets

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=load_emissions_data,
                inputs="raw_emissions_data",
                outputs="emissions_data",
                name="load_emissions_data_node"
            ),
            node(
                func=process_emissions_data,
                inputs="emissions_data",
                outputs="processed_emissions_data",
                name="process_emissions_data_node"
            ),
            node(
                func=load_energy_data,
                inputs="raw_energy_data",
                outputs="energy_data",
                name="load_energy_data_node"
            ),
            node(
                func=merge_datasets,
                inputs=["processed_emissions_data", "energy_data"],
                outputs="merged_data",
                name="merge_datasets_node"
            ),
            node(
                func=save_processed_data,
                inputs="merged_data",
                outputs=None,
                name="save_merged_data_node"
            )
        ]
    )

