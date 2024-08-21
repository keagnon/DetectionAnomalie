from kedro.pipeline import Pipeline, node
from .nodes import load_collections, select_columns, display_selected_data, merge_dataframes, store_in_mongodb
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

    ])