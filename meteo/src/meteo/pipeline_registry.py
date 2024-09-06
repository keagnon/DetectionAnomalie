# src/meteo/pipeline_registry.py

from kedro.pipeline import Pipeline, pipeline
from meteo.pipelines.data_processing import pipeline as dp
from meteo.pipelines.data_viz import pipeline as dv
from meteo.pipelines.data_science import pipeline as ds

def register_pipelines() -> dict[str, Pipeline]:
    data_processing_pipeline = dp.create_pipeline()
    data_visualization_pipeline = dv.create_pipeline()
    data_science_pipeline = ds.create_pipeline()

    return {
        "dp": data_processing_pipeline,
        "dv": data_visualization_pipeline,
        "ds": data_science_pipeline,
        "__default__": pipeline([data_processing_pipeline, data_visualization_pipeline,data_science_pipeline]),
    }
