MYPY_PATHS = data-collection-kedro/src/data_collection_kedro/pipelines/etl_pipeline \
             data-collection-kedro/src/data_collection_kedro/pipelines/data_fusion_pipeline \

PYLINT_PATHS = data-collection-kedro/src/data_collection_kedro/pipelines/etl_pipeline \
               data-collection-kedro/src/data_collection_kedro/pipelines/data_fusion_pipeline \
               dashboard_ui/

ISORT_PATHS = data-collection-kedro/src/data_collection_kedro/pipelines/etl_pipeline \
              data-collection-kedro/src/data_collection_kedro/pipelines/data_fusion_pipeline \
              dashboard_ui/

TEST_PATH = tests/

mypy:
	mypy $(MYPY_PATHS)
pylint:
	pylint $(PYLINT_PATHS)
isort:
	isort $(ISORT_PATHS)
black:
	black $(PYLINT_PATHS)
test:
	pytest $(TEST_PATH) --disable-warnings

# Commande pour exécuter tous les outils (mypy, pylint, isort, black, pytest)
check: mypy pylint isort black test

# Nettoyage des fichiers temporaires
clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
