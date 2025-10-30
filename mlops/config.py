import os
from pathlib import Path

# MLflow configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "./mlruns")
MLFLOW_EXPERIMENT_NAME = "finsight-stock-analysis"

# Create mlruns directory if it doesn't exist
Path(MLFLOW_TRACKING_URI).mkdir(exist_ok=True)