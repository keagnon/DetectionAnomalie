from kedro.framework.context import KedroContext
from kedro.framework.hooks import _create_hook_class
from kedro.framework.hooks import _create_hook_method

# Exécutez le pipeline
context = KedroContext(package_name="your_project", project_path="path/to/your/project")
pipeline = context.pipelines["your_pipeline"]
result = context.run(pipeline=pipeline)

# Accédez aux résultats
linear_rmse = result["linear_rmse"]
rf_rmse = result["rf_rmse"]
rf_predictions = result["rf_predictions"]

# Utilisez les résultats comme vous le souhaitez
print(linear_rmse)
print(rf_rmse)
print(rf_predictions)
