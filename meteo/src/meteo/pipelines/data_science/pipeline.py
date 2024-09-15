from kedro.pipeline import Pipeline, node
from .nodes import (
    split_data,
    train_model,
    evaluate_model,
    predict,
    train_random_forest,
    train_xgboost,
    save_predictions_to_text,
    display_results
)

def create_pipeline(**kwargs) -> Pipeline:
    """
    Crée un pipeline Kedro pour la préparation des données, l'entraînement de plusieurs modèles, 
    et l'évaluation des performances.

    Le pipeline contient les étapes suivantes :
    
    1. `split_data_node`: Sépare les données en ensembles d'entraînement et de test.
    2. `train_linear_model_node`: Entraîne un modèle linéaire sur les données d'entraînement.
    3. `evaluate_linear_model_node`: Évalue les performances du modèle linéaire sur les données de test.
    4. `train_rf_model_node`: Entraîne un modèle de forêt aléatoire (Random Forest).
    5. `evaluate_rf_model_node`: Évalue les performances du modèle de forêt aléatoire.
    6. `train_xgb_model_node`: Entraîne un modèle XGBoost.
    7. `evaluate_xgb_model_node`: Évalue les performances du modèle XGBoost.
    8. `predict_xgb_node`: Utilise le modèle XGBoost pour faire des prédictions sur les données de test.
    9. `display_results_node`: Affiche les résultats d'évaluation des différents modèles (RMSE, R², prédictions).
    10. `save_predictions_node`: Sauvegarde les prédictions du modèle XGBoost dans un fichier texte.

    Args:
        **kwargs: Arguments supplémentaires pour la configuration du pipeline.

    Returns:
        Pipeline: Un objet `Pipeline` de Kedro, comprenant des nœuds pour le traitement des données, 
        l'entraînement et l'évaluation de plusieurs modèles, ainsi que la sauvegarde des résultats.
    """
    return Pipeline(
        [
            node(
                func=split_data,
                inputs=["preprocessed_energy_data", "params:test_size", "params:random_state"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="linear_model",
                name="train_linear_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["linear_model", "X_test", "y_test"],
                outputs=["linear_rmse", "linear_r2"],
                name="evaluate_linear_model_node",
            ),
            node(
                func=train_random_forest,
                inputs=["X_train", "y_train"],
                outputs="rf_model",
                name="train_rf_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["rf_model", "X_test", "y_test"],
                outputs=["rf_rmse", "rf_r2"],
                name="evaluate_rf_model_node",
            ),
            node(
                func=train_xgboost,
                inputs=["X_train", "y_train"],
                outputs="xgb_model",
                name="train_xgb_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["xgb_model", "X_test", "y_test"],
                outputs=["xgb_rmse", "xgb_r2"],
                name="evaluate_xgb_model_node",
            ),
            node(
                func=predict,
                inputs=["xgb_model", "X_test"],
                outputs="xgb_predictions",
                name="predict_xgb_node",
            ),
            node(
                func=display_results,
                inputs=["linear_rmse", "linear_r2", "rf_rmse", "rf_r2", "xgb_rmse", "xgb_r2", "xgb_predictions"],
                outputs=None,
                name="display_results_node",
            ),
            node(
                func=save_predictions_to_text,
                inputs=["xgb_predictions", "params:output_path"],
                outputs=None,
                name="save_predictions_node",
            ),
        ]
    )
