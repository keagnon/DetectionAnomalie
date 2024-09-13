from kedro.pipeline import Pipeline, pipeline
from meteo.pipelines.data_processing import pipeline as dp
from meteo.pipelines.data_viz import pipeline as dv
from meteo.pipelines.data_science import pipeline as ds

def register_pipelines() -> dict[str, Pipeline]:
    """
    Enregistre et assemble les différents pipelines du projet Kedro.

    Cette fonction crée des pipelines pour le traitement des données, la visualisation des données 
    et la science des données. Les pipelines individuels sont enregistrés sous des clés spécifiques 
    et le pipeline par défaut (__default__) est la combinaison des trois pipelines.

    Returns:
        dict[str, Pipeline]: Un dictionnaire où les clés sont des noms de pipelines et les valeurs 
        sont des instances de `Pipeline`. Les clés sont :
        
        - "dp" : Pipeline de traitement des données.
        - "dv" : Pipeline de visualisation des données.
        - "ds" : Pipeline de science des données.
        - "__default__" : Pipeline combiné exécutant les trois pipelines.
    """
    data_processing_pipeline = dp.create_pipeline()
    data_visualization_pipeline = dv.create_pipeline()
    data_science_pipeline = ds.create_pipeline()

    return {
        "dp": data_processing_pipeline,
        "dv": data_visualization_pipeline,
        "ds": data_science_pipeline,
        "__default__": pipeline([data_processing_pipeline, data_visualization_pipeline, data_science_pipeline]),
    }
