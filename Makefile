PYTHON_FILES = data-collection-kedro/src/data_collection_kedro/pipelines/

.PHONY: lint
lint: pylint black-check isort-check mypy

.PHONY: pylint
pylint:
	@echo "Running pylint..."
	pylint $(PYTHON_FILES)

.PHONY: black-check
black-check:
	@echo "Running black check..."
	black --check $(PYTHON_FILES)

.PHONY: isort-check
isort-check:
	@echo "Running isort check..."
	isort --check-only $(PYTHON_FILES)

.PHONY: mypy
mypy:
	@echo "Running mypy..."
	mypy $(PYTHON_FILES)

.PHONY: format
format: black isort

.PHONY: black
black:
	@echo "Running black..."
	black $(PYTHON_FILES)

.PHONY: isort
isort:
	@echo "Running isort..."
	isort $(PYTHON_FILES)

.PHONY: all
all: lint coverage
	@echo "All checks passed!"
