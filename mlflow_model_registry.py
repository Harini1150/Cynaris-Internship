
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "sample_sales.csv"
ARTIFACT_DIR = ROOT / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

TRACKING_URI = (ROOT / "mlflow.db").as_uri().replace("file:///", "sqlite:///")
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_registry_uri(TRACKING_URI)

EXPERIMENT_NAME = "W9D2_Model_Registry"
client = MlflowClient()

data = pd.read_csv(DATA_PATH)
features = ["ad_spend", "website_visits", "discount_percent"]
X = data[features]
y = data["sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "W9D2_Linear_Regression": LinearRegression(),
    "W9D2_Random_Forest": RandomForestRegressor(
        n_estimators=100, max_depth=5, random_state=42
    ),
}

mlflow.set_experiment(EXPERIMENT_NAME)
results = []

for registered_name, model in models.items():
    with mlflow.start_run(run_name=registered_name) as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mae = float(mean_absolute_error(y_test, predictions))
        rmse = float(mean_squared_error(y_test, predictions) ** 0.5)
        r2 = float(r2_score(y_test, predictions))

        mlflow.log_params({
            "model_type": registered_name,
            "test_size": 0.2,
            "random_state": 42,
        })
        mlflow.log_metrics({"MAE": mae, "RMSE": rmse, "R2": r2})

        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            input_example=X_train.head(3),
            skops_trusted_types=(
                ["sklearn.tree._tree.Tree"]
                if isinstance(model, RandomForestRegressor)
                else None
            ),
        )

        try:
            client.create_registered_model(
                registered_name,
                description=(
                    "Sales prediction model trained on synthetic demonstration "
                    "data for the W9D2 model registry exercise."
                ),
            )
            print(f"Created registry entry: {registered_name}")
        except MlflowException as exc:
            if "already exists" in str(exc).lower():
                print(f"Registry entry already exists: {registered_name}")
            else:
                raise

        version = client.create_model_version(
            name=registered_name,
            source=model_info.model_uri,
            run_id=run.info.run_id,
            description=(
                f"MAE={mae:.2f}, RMSE={rmse:.2f}, R2={r2:.4f}. "
                "Trained on synthetic demonstration data."
            ),
        )

        client.set_model_version_tag(
            registered_name, version.version, "model_type", registered_name
        )
        client.set_model_version_tag(
            registered_name, version.version, "dataset", "synthetic_sales"
        )
        client.set_registered_model_tag(
            registered_name, "purpose", "W9D2 analyst model registry exercise"
        )

        results.append({
            "registered_model": registered_name,
            "version": version.version,
            "run_id": run.info.run_id,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
            "model_uri": f"models:/{registered_name}/{version.version}",
        })

        print(f"Registered {registered_name}, version {version.version}")
        print(f"MAE={mae:.2f}, RMSE={rmse:.2f}, R2={r2:.4f}")

report_path = ARTIFACT_DIR / "model_registry_report.csv"
pd.DataFrame(results).to_csv(report_path, index=False)

print(f"\nRegistry report saved to: {report_path}")
print("SUCCESS: W9D2 model registration completed.")
