# W9D5: MLflow Tracked Data Analyst Experiment Pipeline

## Objective

Build an end-to-end machine learning experiment pipeline using MLflow to train, evaluate, compare, and register models.

## Dataset

- Dataset: `data/sample_sales.csv`
- Total records: 300
- Features: `ad_spend`, `website_visits`, `discount_percent`
- Target: `sales`
- Training records: 240
- Testing records: 60

## Models Evaluated

Two regression models were trained using the same dataset and train-test split.

| Metric | Linear Regression | Random Forest |
|---|---:|---:|
| MAE | 3933.26 | 4566.78 |
| RMSE | 5232.37 | 5960.77 |
| R-squared | 0.9357 | 0.9165 |

Linear Regression performed better across all three evaluation metrics.

## MLflow Tracking

- Experiment: `W9D5_Tracked_Experiment_Pipeline`
- Registered model: `W9D5_Best_Sales_Model`
- Registered version: 1
- Tracking backend: SQLite

Both model runs and their evaluation metrics were recorded in MLflow.

## Model Registration

Linear Regression was selected because it achieved the lowest MAE and RMSE and the highest R-squared score.

The selected model was registered in the MLflow Model Registry as version 1.

## Generated Deliverables

- `w9d5_experiment_pipeline.py` — model training and MLflow tracking pipeline.
- `verify_w9d5.py` — experiment and model registry verification.
- `artifacts/w9d5_experiment_comparison.csv` — model comparison results.
- `artifacts/w9d5_experiment_comparison.png` — visual comparison.
- `artifacts/w9d5_pipeline_report.md` — experiment summary.
- `artifacts/evidence/w9d5_model_registry.png` — MLflow registry screenshot.

## Technologies Used

Python, Pandas, Scikit-learn, Matplotlib, MLflow, SQLite and PowerShell.

## Conclusion

This project demonstrates an end-to-end MLflow workflow, including model training, experiment tracking, metric comparison, and model registration.

The results are based on a simulated sales dataset and are intended for learning and demonstration purposes.
