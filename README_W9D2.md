# W9D2: MLflow Model Registry for Analyst Models

## Objective
Build a reproducible MLflow workflow to train, evaluate, register, and document machine learning models for sales prediction.

## Dataset
The project uses `data/sample_sales.csv`, a synthetic sales dataset. The results demonstrate the workflow and should not be interpreted as real-world business findings.

## Models Registered
- **Linear Regression:** Registered as `W9D2_Linear_Regression`
- **Random Forest Regressor:** Registered as `W9D2_Random_Forest`

The workflow records model parameters, evaluation metrics, model artifacts, descriptions, and metadata tags in MLflow.

## Evaluation Results

| Model | Registered Version | MAE | RMSE | R² |
|---|---:|---:|---:|---:|
| Linear Regression | 2 | 3933.26 | 5232.37 | 0.9357 |
| Random Forest | 1 | 4591.03 | 6139.26 | 0.9114 |

Lower MAE and RMSE indicate smaller prediction errors. Higher R² indicates that the model explains more variation in the target on the evaluation data. In this run, Linear Regression performed better on all three metrics.

## Artifacts
- `mlflow_model_registry.py` — model training and registration workflow.
- `artifacts/model_registry_report.csv` — registered model versions, run IDs, metrics, and model URIs.
- `artifacts/model_registry_dashboard.png` — reserved for the MLflow Registry screenshot, if captured.

## How to Run
Activate the project's virtual environment and run:

```powershell
python .\mlflow_model_registry.py
```

The script trains and evaluates both models, registers them with MLflow, and writes the registry report to `artifacts/model_registry_report.csv`.

## Registry Details
The workflow creates or reuses registered models, records model versions, and adds descriptions and tags for model type, dataset, and intended use. For the Random Forest model, the locally trained scikit-learn tree type is explicitly trusted for model serialization.

## Limitations
The dataset is synthetic. Metrics depend on the current dataset and train/test split and do not establish production performance. MLflow may display non-fatal model-signature warnings for integer-valued columns.

## Conclusion
This exercise demonstrates model versioning, experiment tracking, evaluation reporting, and model registry metadata using MLflow.
