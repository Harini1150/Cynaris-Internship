# W9D4 - MLflow Model Version Comparison

## Objective

Compare two registered Random Forest model versions
using the same dataset and test split.

## Model configurations

| Parameter | Version 1 | Version 2 |
|---|---:|---:|
| Estimators | 100 | 200 |
| Maximum depth | 5 | 8 |
| Minimum samples split | Default | 4 |
| Random state | 42 | 42 |

## Performance comparison

| Metric | Version 1 | Version 2 |
|---|---:|---:|
| MAE | 4591.0349 | 4566.7778 |
| RMSE | 6139.2575 | 5960.7745 |
| R2 | 0.9114 | 0.9165 |

## Interpretation

Lower MAE and RMSE indicate lower prediction errors.
Higher R-squared indicates a better fit to the test data.

Both versions were evaluated using the same dataset
and train-test split for a fair comparison.

## MLflow details

- Registered model: W9D2_Random_Forest
- Baseline version: 1
- Comparison version: 2
- Experiment: W9D4_Model_Version_Comparison
- Version 1 run: bf8c91acb2aa45ecbac0d42eafaf450e
- Comparison run: d0fdbc3d71e842599fb7779daea2fa1b

## Conclusion

Version 2 uses adjusted Random Forest
hyperparameters.

Its performance is compared against Version 1 using
MAE, RMSE and R-squared.

The comparison shows whether the adjusted model
improves prediction performance.
