# W10D2 - Prophet Forecasting on Monthly Sales Data

## Objective
Apply Facebook Prophet to monthly sales data to identify trends and seasonal patterns and forecast the next 12 months.

## Dataset
- File: data/monthly_sales.csv
- Total observations: 84
- Historical period: January 2019 to December 2025
- Average monthly sales: 84,197.17
- Columns: Date and Sales

## Data Preparation
The Date column was converted into datetime format and renamed to ds. The Sales column was renamed to y, following Prophet's required input format.

## Model Development
- Algorithm: Facebook Prophet
- Yearly seasonality: Enabled
- Weekly seasonality: Disabled
- Daily seasonality: Disabled
- Seasonality mode: Additive
- Training observations: 72
- Testing observations: 12

## Evaluation Results
- MAE: 5,533.72
- RMSE: 6,572.27
- MAPE: 5.24%

## Forecast Results
A 12-month forecast was generated for January to December 2026.

- January 2026: 105,635.07
- June 2026: 119,167.13
- December 2026: 151,753.09

The forecast indicates an overall upward sales trend during the predicted period.

## Deliverables
- prophet_forecasting.py
- outputs/prophet_test_predictions.csv
- outputs/prophet_12_month_forecast.csv
- outputs/prophet_forecast.png
- outputs/prophet_components.png
- reports/prophet_forecasting_report.txt
- evidence/W10D2_Prophet_Forecast.png
- evidence/W10D2_Prophet_Components.png

## Learning Outcomes
- Prepared time-series data for Prophet.
- Applied yearly seasonality.
- Evaluated predictions using MAE, RMSE and MAPE.
- Generated future forecasts and visualized trend and seasonal components.

## Note
This exercise uses the monthly sales dataset available in the W10D2 worktree. It is a sales forecasting exercise, not an external Indian stock-market forecast. Forecasts are estimates, not guaranteed future sales.
