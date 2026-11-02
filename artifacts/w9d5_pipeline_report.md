# W9D5 Tracked Data Analyst Experiment Pipeline

## Objective

Train, track, compare, and register machine learning
models using MLflow.

## Dataset

- File: data/sample_sales.csv
- Total rows: 300
- Features: ad_spend, website_visits, discount_percent
- Target: sales
- Training rows: 240
- Testing rows: 60

## Models Evaluated

       model_name         MAE        RMSE       R2                           run_id
Linear_Regression 3933.259257 5232.365774 0.935661 54e25a20bf594bd4b38063201b1c8d61
    Random_Forest 4566.777756 5960.774463 0.916500 a15463f417b349d0bd46ca995d626af0

## Best Model

- Model: Linear_Regression
- MAE: 3933.2593
- RMSE: 5232.3658
- R2: 0.9357

## MLflow Registration

- Experiment: W9D5_Tracked_Experiment_Pipeline
- Registered model: W9D5_Best_Sales_Model
- Model version: 1

## Generated Outputs

- w9d5_experiment_comparison.csv
- w9d5_experiment_comparison.png
- w9d5_pipeline_report.md

## Conclusion

Both models were trained using the same dataset
and training/testing split.

The model with the lowest RMSE was selected
and registered in MLflow.
