from elasticsearch import Elasticsearch
import os

# Connexion à Elasticsearch
es = Elasticsearch(
    "https://a95637e713d24921bde1e4c95d058bb2.us-central1.gcp.cloud.es.io",
    basic_auth=("engiewatchproject", "Engie2024")
)
update_query = {
    "script": {
        "source": "ctx._source.model_name = 'CatBoost'",
        "lang": "painless"
    },
    "query": {
        "match": {
            "model_name": "BestEstimator"
        }
    }
}

# Exécuter la requête de mise à jour
response = es.update_by_query(index="logs_engiewatch", body=update_query)
print(response)