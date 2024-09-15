from kedro.pipeline import Pipeline
from data_collection_kedro.pipelines.data_fusion_pipeline import create_pipeline as create_data_fusion_pipeline
from data_collection_kedro.pipelines.etl_pipeline import create_pipeline as create_etl_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    """
    Register the project's pipelines.
    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    data_fusion_pipeline = create_data_fusion_pipeline()
    etl_pipeline = create_etl_pipeline()

    return {
        "data-fusion-pipeline": data_fusion_pipeline,
        "etl_pipeline": etl_pipeline,
        "__default__": etl_pipeline + data_fusion_pipeline,
    }

