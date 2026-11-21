# W10D1 – Time Series Analysis and Sales Forecasting

## Project Overview
This project analyzes monthly sales data using time-series analysis techniques and Seasonal ARIMA forecasting.

## Dataset
- 84 monthly observations
- Period: January 2019 – December 2025
- Columns: Date and Sales
- Dataset: Simulated educational sales data

## Technologies Used
- Python 3.11
- Pandas and NumPy
- Matplotlib
- Statsmodels
- Scikit-learn

## Analysis Performed
1. Data loading and date-time preprocessing
2. Sales trend visualization
3. Seasonal pattern analysis
4. Seasonal decomposition
5. Augmented Dickey-Fuller stationarity test
6. Chronological train-test split
7. Naive baseline and Seasonal ARIMA comparison
8. 12-month sales forecasting

## Model Evaluation

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Naive Baseline | 31321.53 | 35109.83 | 30.72% |
| Seasonal ARIMA | 4975.71 | 5806.78 | 4.64% |

Seasonal ARIMA performed better than the naive baseline on the 12-month test period.

## Forecast
The final model forecasts monthly sales for January–December 2026. Forecast values and confidence intervals are saved in the outputs folder.

## Key Learning
This project demonstrates how trend, seasonality, stationarity testing, and ARIMA models can be used to analyze historical time-series data and generate forecasts.

## Note
The dataset is simulated for educational purposes. Forecasts should not be interpreted as actual business predictions.