# W9D1: MLflow Experiment Tracking

## Objective
Track, evaluate, and compare machine-learning experiments using MLflow.

## Dataset
A synthetic sales dataset containing 300 rows, with advertising spend, website visits, and discount percentage as input features. Sales is the target variable.

## Models Compared
- Linear Regression
- Random Forest Regressor

## Evaluation Results

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 3933.26 | 5232.37 | 0.9357 |
| Random Forest | 4591.03 | 6139.26 | 0.9114 |

Linear Regression performed better on this generated test dataset. These results are illustrative and are not findings from real business data.

## MLflow Tracking
Experiment: `W9D1_MLflow_Tracking`

MLflow logs model parameters, evaluation metrics, and comparison artifacts to a local SQLite-backed tracking store.

## Run the Project

Activate the W9D1 virtual environment, then run:

```powershell
python mlflow_tracking.py
```

Start the dashboard:

```powershell
python -m mlflow ui --backend-store-uri "sqlite:///C:/Users/DELL/Desktop/Cynaris-Internship/Cynaris-W9D1/mlflow.db" --host 127.0.0.1 --port 5001 --workers 1
```

Open `http://127.0.0.1:5001` in your browser.

## Deliverables
- `mlflow_tracking.py` — experiment tracking and model evaluation
- `data/sample_sales.csv` — generated dataset
- `artifacts/experiment_results.csv` — comparison metrics
- `artifacts/experiment_comparison.png` — model comparison chart
- `artifacts/mlflow_dashboard.png` — MLflow dashboard evidence
