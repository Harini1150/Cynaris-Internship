
# W10D1: Sales Time Series Analysis

## Dataset
- Records: 84
- Period: 2019-01-01 to 2025-12-01
- Frequency: Monthly
- Data type: Simulated educational sales data

## Trend and Seasonality
The sales series is analyzed for long-term trend and
recurring monthly seasonal patterns.

## Stationarity
- Original ADF p-value: 0.993275
- First-differenced ADF p-value: 0.000000

A p-value below 0.05 provides evidence against a unit root.

## Forecast Evaluation
- Training observations: 72
- Testing observations: 12
- Best model by test MAE: Seasonal ARIMA

         Model          MAE         RMSE      MAPE
Naive Baseline 31321.525000 35109.828424 30.723329
Seasonal ARIMA  4975.707379  5806.783677  4.635252

## Forecasting Method
Seasonal ARIMA order: (1,1,1)
Seasonal order: (1,1,1,12)

The final model was fitted using all available observations
to forecast the next 12 months.

## Important Note
The dataset is simulated and the forecasts are for learning
and demonstration purposes, not actual business decisions.
