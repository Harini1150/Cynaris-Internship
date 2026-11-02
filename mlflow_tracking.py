from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
ARTIFACT_DIR = ROOT / "artifacts"
DATA_DIR.mkdir(exist_ok=True)
ARTIFACT_DIR.mkdir(exist_ok=True)

# Create reproducible sample business sales data.
rng = np.random.default_rng(42)
rows = 300

ad_spend = rng.uniform(1000, 20000, rows)
website_visits = rng.integers(500, 10000, rows)
discount = rng.uniform(0, 30, rows)

sales = (
    5000
    + 2.8 * ad_spend
    + 4.5 * website_visits
    - 120 * discount
    + rng.normal(0, 5000, rows)
)

data = pd.DataFrame({
    "ad_spend": ad_spend.round(2),
    "website_visits": website_visits,
    "discount_percent": discount.round(2),
    "sales": sales.round(2),
})

data_path = DATA_DIR / "sample_sales.csv"
data.to_csv(data_path, index=False)

X = data[["ad_spend", "website_visits", "discount_percent"]]
y = data["sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "Linear_Regression": LinearRegression(),
    "Random_Forest": RandomForestRegressor(
        n_estimators=100, max_depth=5, random_state=42
    ),
}

mlflow.set_tracking_uri((ROOT / "mlflow.db").as_uri().replace("file:///", "sqlite:///"))
mlflow.set_experiment("W9D1_MLflow_Tracking")

results = []

for run_name, model in models.items():
    with mlflow.start_run(run_name=run_name):
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
        r2 = r2_score(y_test, predictions)

        params = model.get_params(deep=False)
        mlflow.log_params({
            "model_type": run_name,
            "test_size": 0.2,
            "random_state": 42,
            **{
                key: value
                for key, value in params.items()
                if isinstance(value, (str, int, float, bool))
                or value is None
            },
        })
        mlflow.log_metrics({
            "MAE": float(mae),
            "RMSE": float(rmse),
            "R2": float(r2),
        })

        results.append({
            "model": run_name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        })

        print(
            f"{run_name}: MAE={mae:.2f}, "
            f"RMSE={rmse:.2f}, R2={r2:.4f}"
        )

results_df = pd.DataFrame(results)
results_path = ARTIFACT_DIR / "experiment_results.csv"
results_df.to_csv(results_path, index=False)

# Compare model error scores in a chart.
ax = results_df.set_index("model")[["MAE", "RMSE"]].plot(
    kind="bar", figsize=(9, 5)
)
ax.set_title("W9D1: Sales Model Comparison")
ax.set_ylabel("Error (lower is better)")
ax.set_xlabel("Model")
plt.xticks(rotation=0)
plt.tight_layout()

chart_path = ARTIFACT_DIR / "experiment_comparison.png"
plt.savefig(chart_path, dpi=150)
plt.close()

# Log the comparison outputs as a separate MLflow run.
with mlflow.start_run(run_name="Experiment_Comparison_Artifacts"):
    mlflow.log_artifact(str(results_path))
    mlflow.log_artifact(str(chart_path))
    mlflow.log_artifact(str(data_path))

print("\nExperiment results:")
print(results_df.round(4).to_string(index=False))
print(f"\nDataset saved: {data_path}")
print(f"Results saved: {results_path}")
print(f"Chart saved: {chart_path}")
print(f"MLflow tracking directory: {ROOT / 'mlruns'}")
print("\nSUCCESS: Both experiments and comparison artifacts were logged.")

