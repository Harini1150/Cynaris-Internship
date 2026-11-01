@'
# W9D4: MLflow Dashboard — Compare Model Versions

## Objective
Compare two registered Random Forest model versions using MLflow.
Track model parameters, evaluate performance metrics, and visualize the comparison.

## Tools and Technologies
- Python
- MLflow 3.17.2
- Scikit-learn
- Pandas
- Matplotlib
- SQLite

## Dataset
- Dataset: data/sample_sales.csv
- Train-test split: 80/20
- Random state: 42
- Both versions use the same dataset and test split.

## Model Configurations

| Parameter | Version 1 | Version 2 |
|---|---:|---:|
| Estimators | 100 | 200 |
| Maximum depth | 5 | 8 |
| Minimum samples split | Default | 4 |
| Random state | 42 | 42 |

## Performance Comparison

| Metric | Version 1 | Version 2 |
|---|---:|---:|
| MAE | 4591.0349 | 4566.7778 |
| RMSE | 6139.2575 | 5960.7745 |
| R-squared | 0.9114 | 0.9165 |

## Results
Version 2 performed better than Version 1 on all three evaluation metrics.
It achieved lower MAE and RMSE and a higher R-squared value.

## MLflow Details
- Experiment: W9D4_Model_Version_Comparison
- Registered model: W9D2_Random_Forest
- Baseline: Version 1
- Comparison: Version 2

## Generated Artifacts
- artifacts/w9d4_version_comparison.csv
- artifacts/w9d4_version_comparison.png
- artifacts/w9d4_comparison_report.md

## Conclusion
This task demonstrates MLflow experiment tracking and model version comparison.
The adjusted Random Forest model (Version 2) showed improved prediction performance
on the same test dataset.
'@ | Set-Content -Path .\README_W9D4.md -Encoding UTF8