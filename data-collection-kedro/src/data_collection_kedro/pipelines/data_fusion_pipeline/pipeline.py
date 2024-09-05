from kedro.pipeline import Pipeline, node

from .nodes import (display_dataframes, load_collections,
                    merge_data_store_in_elastic, normalize_columns,
                    select_columns)


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=load_collections,
                inputs=dict(
                    collection_names="params:collection_names1",
                    db_name="params:db_name1",
                ),
                outputs="loaded_dataframes",
                name="load_collections_node",
            ),
            node(
                func=select_columns,
                inputs=dict(
                    dataframes="loaded_dataframes",
                    columns_to_select="params:columns_to_select",
                ),
                outputs="selected_dataframes",
                name="select_columns_node",
            ),
            node(
                func=display_dataframes,
                inputs="selected_dataframes",
                outputs="displayed_selected_data",
                name="display_selected_data_node",
            ),
            node(
                func=normalize_columns,
                inputs="selected_dataframes",
                outputs="normalized_dataframes",
                name="normalize_columns_node",
            ),
            node(
                func=merge_data_store_in_elastic,
                inputs=["normalized_dataframes"],
                outputs=["merged_meteo_courbe", "merged_courbe_mouvement"],
                name="merge_data_node",
            ),
        ]
    )
