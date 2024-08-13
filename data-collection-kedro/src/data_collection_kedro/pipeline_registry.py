from kedro.pipeline import Pipeline
from data_collection_kedro.pipelines.data_engineering import create_pipeline as create_data_engineering_pipeline
from data_collection_kedro.pipelines.data_fusion_pipeline import create_pipeline as create_data_fusion_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.
    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    data_engineering_pipeline = create_data_engineering_pipeline()
    data_fusion_pipeline = create_data_fusion_pipeline()

    return {
        "data_engineering_pipeline": data_engineering_pipeline,
        "data_fusion_pipeline": data_fusion_pipeline,
        "__default__": data_engineering_pipeline + data_fusion_pipeline,
    }
