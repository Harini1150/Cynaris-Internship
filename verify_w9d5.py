from pathlib import Path
import mlflow
from mlflow import MlflowClient

db_path = Path("mlflow.db").resolve().as_posix()
mlflow.set_tracking_uri("sqlite:///" + db_path)

client = MlflowClient()

experiment = client.get_experiment_by_name(
    "W9D5_Tracked_Experiment_Pipeline"
)

if experiment is None:
    print("Experiment not found!")
else:
    print("Experiment:", experiment.name)

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id]
    )

    print("Total recorded runs:", len(runs))

    for run in runs:
        print(
            "Run:", run.info.run_name,
            "| Status:", run.info.status,
            "| Metrics:", run.data.metrics
        )

    versions = client.search_model_versions(
        "name = 'W9D5_Best_Sales_Model'"
    )

    print("\nRegistered model versions:")
    for version in versions:
        print(
            "Name:", version.name,
            "| Version:", version.version,
            "| Status:", version.status
        )
