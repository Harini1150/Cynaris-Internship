# W10D5 - Sales Forecasting Dashboard

## 1. Project Overview

This project combines Exploratory Data Analysis (EDA) with time-series forecasting to study business performance, identify sales patterns, compare forecasting models, and generate a 12-month sales forecast.

## 2. Datasets

### Indian Business Orders
- 1,500 records and 17 columns.
- 500 unique orders.
- Date range: April 2018 to March 2019.
- Includes sales, profit, quantity, customer, category, state, and city information.

### Monthly Sales
- 84 monthly observations.
- Date range: January 2019 to December 2025.
- Contains Date and Sales columns.
- This is simulated educational data, not verified real-world market data.

The two datasets are analysed separately for business EDA and time-series forecasting.

## 3. Business EDA Findings

| Metric | Result |
|---|---:|
| Total records | 1,500 |
| Unique orders | 500 |
| Total sales | 431,502.00 |
| Total profit | 23,955.00 |
| Average order value | 863.00 |

The notebook also explores category-wise sales and profit, state-wise sales, and monthly order trends.

## 4. Forecasting Methodology

- Training period: January 2019 to December 2024.
- Testing period: January 2025 to December 2025.
- Baseline model: Seasonal Naive.
- Forecasting model: Prophet.
- Evaluation metrics: MAE, RMSE, and MAPE.

The final Prophet model was fitted using all 84 observations to forecast the next 12 months.

## 5. Model Comparison

| Metric | Seasonal Naive | Prophet |
|---|---:|---:|
| MAE | 8,509.66 | 5,533.72 |
| RMSE | 9,777.81 | 6,572.27 |
| MAPE | 7.65% | 5.24% |

Prophet achieved lower errors across all three evaluation metrics. Its MAE was approximately 34.97% lower than the seasonal-naive baseline.

## 6. 2026 Forecast Highlights

| Month | Predicted Sales |
|---|---:|
| January | 105,635.07 |
| February | 107,200.20 |
| March | 108,844.48 |
| April | 114,363.75 |
| May | 115,666.05 |
| June | 119,167.13 |
| July | 122,918.30 |
| August | 122,653.54 |
| September | 123,310.60 |
| October | 132,544.59 |
| November | 142,962.23 |
| December | 151,753.09 |

The forecast indicates an overall upward projected trend, with stronger estimates toward the end of 2026.

These are estimates based on simulated educational data, not guaranteed business outcomes.

## 7. Project Files

- `W10D5_Sales_Forecasting_Dashboard.ipynb` - Main analysis and forecasting notebook.
- `requirements_w10d5.txt` - Python dependencies.
- `data/` - Input datasets.
- `outputs/` - Forecast CSV files and visualisations.
- `reports/` - Forecasting summary report.
- `evidence/` - Supporting screenshots.

## 8. How to Run

1. Clone the repository.
2. Open PowerShell in the project directory.
3. Create and activate a Python virtual environment.
4. Install dependencies:

   `pip install -r requirements_w10d5.txt`

5. Start JupyterLab:

   `jupyter lab`

6. Open `W10D5_Sales_Forecasting_Dashboard.ipynb` and run the cells.

## 9. Limitations

- Monthly sales data is simulated educational data.
- Model evaluation uses one 12-month holdout period.
- Forecast accuracy may vary with different datasets and periods.
- Forecasts are estimates, not guarantees.
- Real business decisions require validated and regularly updated sales data.

## 10. Conclusion

This project demonstrates business EDA, data preparation, time-series analysis, forecasting, model evaluation, visualisation, and documentation. Prophet performed better than the seasonal-naive baseline on the selected test period.
