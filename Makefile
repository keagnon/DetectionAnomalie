# Variables pour les répertoires à vérifier
MYPY_PATHS = data-collection-kedro/src/data_collection_kedro/pipelines/etl_pipeline \
             data-collection-kedro/src/data_collection_kedro/pipelines/data_fusion_pipeline \

PYLINT_PATHS = data-collection-kedro/src/data_collection_kedro/pipelines/etl_pipeline \
               data-collection-kedro/src/data_collection_kedro/pipelines/data_fusion_pipeline \
               dashboard_ui/

ISORT_PATHS = data-collection-kedro/src/data_collection_kedro/pipelines/etl_pipeline \
              data-collection-kedro/src/data_collection_kedro/pipelines/data_fusion_pipeline \
              dashboard_ui/

# Répertoire contenant les tests unitaires
TEST_PATH = tests/

# Commande pour lancer mypy
mypy:
	mypy $(MYPY_PATHS)

# Commande pour lancer Pylint
pylint:
	pylint $(PYLINT_PATHS)

# Commande pour trier les imports avec isort
isort:
	isort $(ISORT_PATHS)

# Commande pour formater le code avec black
black:
	black $(PYLINT_PATHS)

# Commande pour exécuter les tests unitaires avec pytest
test:
	pytest $(TEST_PATH) --disable-warnings

# Commande pour exécuter tous les outils (mypy, pylint, isort, black, pytest)
check: mypy pylint isort black test

# Nettoyage des fichiers temporaires
clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
