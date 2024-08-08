"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.5
"""

from kedro.pipeline import Pipeline, node
from .nodes import fetch_data_from_api, display_data

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=fetch_data_from_api,
                inputs="params:api_url",
                outputs="raw_data",
                name="fetch_data_node",
            ),
            node(
                func=display_data,
                inputs="raw_data",
                outputs=None,
                name="display_data_node",
            ),
        ]
    )

