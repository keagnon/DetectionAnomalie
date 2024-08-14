"""
This is a boilerplate pipeline 'etl_pipeline'
generated using Kedro 0.19.5
"""
from kedro.pipeline import Pipeline, node
from .nodes import process_api_data,process_csv_data

def create_pipeline(**kwargs) -> Pipeline:
    """
    Create a Kedro pipeline for the ETL process with multiple API sources.
    Returns::
          Pipeline: The constructed Kedro pipeline.
    """
    return Pipeline(
        [
            node(
                func=process_api_data,
                inputs=["params:api_urls", "params:db_name", "params:collection_names"],
                outputs=None,
                name="process_api_data_node",
            ),
            node(
                func=process_csv_data,
                inputs=["params:csv_file_paths", "params:db_name", "params:collection_names"],
                outputs=None,
                name="process_csv_data_node",
            ),
        ]
    )
