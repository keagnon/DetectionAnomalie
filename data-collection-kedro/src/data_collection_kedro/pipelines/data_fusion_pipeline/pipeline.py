"""
This is a boilerplate pipeline 'data_fusion_pipeline'
generated using Kedro 0.19.5
"""
from kedro.pipeline import Pipeline, node
from .nodes import load_collections, select_columns, display_selected_data, merge_dataframes, display_data, store_in_mongodb
def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
                func=load_collections,
                inputs=dict(collection_names="params:collection_names1", db_name="params:db_name1"),
                outputs="loaded_dataframes",
                name="load_collections_node",
            ),
        node(
                func=select_columns,
                inputs=dict(dataframes="loaded_dataframes", columns_to_select="params:columns_to_select"),
                outputs="selected_dataframes",
                name="select_columns_node",
        ),
        node(
                func=display_selected_data,
                inputs="selected_dataframes",
                outputs="displayed_selected_data",
                name="display_selected_data_node",
        ),
        node(
                func=merge_dataframes,
                inputs=dict(dataframes="selected_dataframes", merge_column="params:merge_column"),
                outputs="merged_data",
                name="merge_data_node",
        ),
        node(
                func=display_data,
                inputs="merged_data",
                outputs="displayed_data",
                name="display_data_node",
        ),
        node(
                func=store_in_mongodb,
                inputs=dict(data="displayed_data", db_name="params:db_name", collection_name="params:output_collection_name"),
                outputs=None,
                name="store_in_mongodb_node",
        ),
    ])
