
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

ROOT = Path(__file__).resolve().parent

DATA_PATH = ROOT / "data" / "sample_sales.csv"
ARTIFACTS_DIR = ROOT / "artifacts"

ARTIFACTS_DIR.mkdir(exist_ok=True)

TRACKING_URI = f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}"

EXPERIMENT_NAME = "W9D5_Tracked_Experiment_Pipeline"
REGISTERED_MODEL_NAME = "W9D5_Best_Sales_Model"

RANDOM_STATE = 42


# ==================================================
# 2. LOAD DATASET
# ==================================================

print("\nW9D5: TRACKED DATA ANALYST EXPERIMENT PIPELINE")
print("=" * 55)

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

required_columns = [
    "ad_spend",
    "website_visits",
    "discount_percent",
    "sales",
]

if not all(column in df.columns for column in required_columns):
    raise ValueError("Dataset is missing required columns.")

if df[required_columns].isnull().any().any():
    raise ValueError("Dataset contains missing values.")

X = df[
    ["ad_spend", "website_visits", "discount_percent"]
]

y = df["sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
)

print(f"Dataset loaded: {len(df)} rows")
print(f"Training rows: {len(X_train)}")
print(f"Testing rows: {len(X_test)}")


# ==================================================
# 3. CONFIGURE MLFLOW
# ==================================================

mlflow.set_tracking_uri(TRACKING_URI)

mlflow.set_experiment(EXPERIMENT_NAME)

models = {
    "Linear_Regression": LinearRegression(),

    "Random_Forest": RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        min_samples_split=4,
        random_state=RANDOM_STATE,
    ),
}

results = []


# ==================================================
# 4. TRAIN AND TRACK MODELS
# ==================================================

for model_name, model in models.items():

    print(f"\nTraining: {model_name}")

    with mlflow.start_run(
        run_name=f"W9D5_{model_name}"
    ):

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(
            y_test,
            predictions,
        )

        rmse = mean_squared_error(
            y_test,
            predictions,
        ) ** 0.5

        r2 = r2_score(
            y_test,
            predictions,
        )

        mlflow.log_params(model.get_params())

        mlflow.log_param("model_name", model_name)
        mlflow.log_param("test_size", 0.20)
        mlflow.log_param("random_state", RANDOM_STATE)

        mlflow.log_metrics({
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        })

        mlflow.set_tag(
            "project",
            "W9D5 Tracked Experiment Pipeline",
        )

        mlflow.set_tag("model_type", model_name)

        # Trust only the reviewed Scikit-learn tree type
        # for the Random Forest model created by this script.

        model_log_kwargs = {}

        if model_name == "Random_Forest":
            model_log_kwargs["skops_trusted_types"] = [
                "sklearn.tree._tree.Tree"
            ]

        mlflow.sklearn.log_model(
            model,
            name="model",
            **model_log_kwargs,
        )

        results.append({
            "model_name": model_name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
            "run_id": mlflow.active_run().info.run_id,
        })

        print(f"MAE:  {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R2:   {r2:.4f}")


# ==================================================
# 5. COMPARE EXPERIMENT RESULTS
# ==================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by=["RMSE", "MAE"],
    ascending=True,
).reset_index(drop=True)

best_row = results_df.iloc[0]

best_model_name = best_row["model_name"]
best_run_id = best_row["run_id"]

comparison_path = (
    ARTIFACTS_DIR / "w9d5_experiment_comparison.csv"
)

results_df.to_csv(
    comparison_path,
    index=False,
)

print("\nMODEL COMPARISON")
print("=" * 55)

print(results_df.to_string(index=False))

print(f"\nBest model: {best_model_name}")


# ==================================================
# 6. REGISTER BEST MODEL IN MLFLOW
# ==================================================

model_uri = f"runs:/{best_run_id}/model"

registration = mlflow.register_model(
    model_uri=model_uri,
    name=REGISTERED_MODEL_NAME,
)

print("\nMODEL REGISTRATION")
print("=" * 55)

print(f"Registered model: {REGISTERED_MODEL_NAME}")
print(f"Model version: {registration.version}")


# ==================================================
# 7. CREATE COMPARISON CHART
# ==================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(11, 5),
)

axes[0].bar(
    results_df["model_name"],
    results_df["RMSE"],
)

axes[0].set_title("Model RMSE Comparison")
axes[0].set_ylabel("RMSE")
axes[0].tick_params(
    axis="x",
    rotation=15,
)

axes[1].bar(
    results_df["model_name"],
    results_df["R2"],
)

axes[1].set_title("Model R2 Comparison")
axes[1].set_ylabel("R2")
axes[1].tick_params(
    axis="x",
    rotation=15,
)

fig.tight_layout()

chart_path = (
    ARTIFACTS_DIR / "w9d5_experiment_comparison.png"
)

fig.savefig(
    chart_path,
    dpi=150,
)

plt.close(fig)


# ==================================================
# 8. GENERATE PIPELINE REPORT
# ==================================================

report = f"""# W9D5 Tracked Data Analyst Experiment Pipeline

## Objective

Train, track, compare, and register machine learning
models using MLflow.

## Dataset

- File: data/sample_sales.csv
- Total rows: {len(df)}
- Features: ad_spend, website_visits, discount_percent
- Target: sales
- Training rows: {len(X_train)}
- Testing rows: {len(X_test)}

## Models Evaluated

{results_df.to_string(index=False)}

## Best Model

- Model: {best_model_name}
- MAE: {best_row['MAE']:.4f}
- RMSE: {best_row['RMSE']:.4f}
- R2: {best_row['R2']:.4f}

## MLflow Registration

- Experiment: {EXPERIMENT_NAME}
- Registered model: {REGISTERED_MODEL_NAME}
- Model version: {registration.version}

## Generated Outputs

- w9d5_experiment_comparison.csv
- w9d5_experiment_comparison.png
- w9d5_pipeline_report.md

## Conclusion

Both models were trained using the same dataset
and training/testing split.

The model with the lowest RMSE was selected
and registered in MLflow.
"""

report_path = (
    ARTIFACTS_DIR / "w9d5_pipeline_report.md"
)

report_path.write_text(
    report,
    encoding="utf-8",
)


# ==================================================
# 9. FINAL STATUS
# ==================================================

print("\n" + "=" * 55)
print("W9D5 PIPELINE COMPLETED SUCCESSFULLY!")
print("=" * 55)

print(f"Comparison CSV: {comparison_path}")
print(f"Comparison Chart: {chart_path}")
print(f"Pipeline Report: {report_path}")

print("\nExperiment tracking completed.")
