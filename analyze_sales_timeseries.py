
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

warnings.filterwarnings("ignore")

# --------------------------------------------------
# 1. Load and prepare the monthly sales data
# --------------------------------------------------

DATA_PATH = Path("data/monthly_sales.csv")
OUTPUT_DIR = Path("outputs")
REPORT_DIR = Path("reports")

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")
df = df.set_index("Date")
df = df.asfreq("MS")

sales = df["Sales"].astype(float)

print("=" * 55)
print("W10D1: SALES TIME SERIES ANALYSIS")
print("=" * 55)
print(f"Records: {len(sales)}")
print(f"Date range: {sales.index.min().date()} to {sales.index.max().date()}")
print(f"Missing values: {sales.isna().sum()}")
print(f"Average monthly sales: {sales.mean():,.2f}")

# --------------------------------------------------
# 2. Visualize the sales trend
# --------------------------------------------------

plt.figure(figsize=(12, 5))
plt.plot(sales.index, sales, marker="o", linewidth=1.5)
plt.title("Monthly Sales Trend (2019–2025)")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sales_trend.png", dpi=150)
plt.close()

# --------------------------------------------------
# 3. Analyze seasonality and decomposition
# --------------------------------------------------

decomposition = seasonal_decompose(
    sales,
    model="multiplicative",
    period=12
)

fig = decomposition.plot()
fig.set_size_inches(12, 9)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "seasonal_decomposition.png", dpi=150)
plt.close(fig)

monthly_average = sales.groupby(sales.index.month).mean()
monthly_average.index = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

plt.figure(figsize=(10, 5))
monthly_average.plot(kind="bar")
plt.title("Average Sales by Month")
plt.xlabel("Month")
plt.ylabel("Average Sales")
plt.xticks(rotation=0)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_seasonality.png", dpi=150)
plt.close()

# --------------------------------------------------
# 4. Augmented Dickey-Fuller stationarity test
# --------------------------------------------------

adf_original = adfuller(sales.dropna())
adf_differenced = adfuller(sales.diff().dropna())

print("\nSTATIONARITY TEST")
print("-" * 40)
print(f"Original series ADF statistic: {adf_original[0]:.4f}")
print(f"Original series p-value: {adf_original[1]:.4f}")
print(f"First-differenced ADF statistic: {adf_differenced[0]:.4f}")
print(f"First-differenced p-value: {adf_differenced[1]:.4f}")

# --------------------------------------------------
# 5. Split data chronologically
#    Last 12 months are used for testing
# --------------------------------------------------

train = sales.iloc[:-12]
test = sales.iloc[-12:]

print("\nMODEL TRAINING")
print("-" * 40)
print(f"Training records: {len(train)}")
print(f"Testing records: {len(test)}")

# --------------------------------------------------
# 6. Naive baseline forecast
#    Uses the last training value for every test month
# --------------------------------------------------

naive_forecast = pd.Series(
    train.iloc[-1],
    index=test.index
)

# --------------------------------------------------
# 7. Seasonal ARIMA model
# --------------------------------------------------

model = SARIMAX(
    train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False
)

fitted_model = model.fit(disp=False)
arima_forecast = fitted_model.forecast(steps=len(test))
arima_forecast.index = test.index

# --------------------------------------------------
# 8. Evaluate forecast performance
# --------------------------------------------------

def calculate_metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(
        np.abs((actual - predicted) / actual)
    ) * 100

    return mae, rmse, mape


naive_metrics = calculate_metrics(test, naive_forecast)
arima_metrics = calculate_metrics(test, arima_forecast)

comparison = pd.DataFrame(
    [
        ["Naive Baseline", *naive_metrics],
        ["Seasonal ARIMA", *arima_metrics]
    ],
    columns=["Model", "MAE", "RMSE", "MAPE"]
)

comparison.to_csv(OUTPUT_DIR / "model_comparison.csv", index=False)

print("\nMODEL COMPARISON")
print("-" * 40)
print(comparison.to_string(index=False))

# --------------------------------------------------
# 9. Plot actual sales against test forecasts
# --------------------------------------------------

plt.figure(figsize=(12, 5))
plt.plot(train.index, train, label="Training Sales")
plt.plot(test.index, test, label="Actual Test Sales", marker="o")
plt.plot(
    test.index,
    arima_forecast,
    label="Seasonal ARIMA Forecast",
    marker="o"
)
plt.title("Actual vs Seasonal ARIMA Forecast")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "actual_vs_forecast.png", dpi=150)
plt.close()

# --------------------------------------------------
# 10. Train on all data and forecast next 12 months
# --------------------------------------------------

final_model = SARIMAX(
    sales,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False
)

final_fit = final_model.fit(disp=False)

future_forecast = final_fit.get_forecast(steps=12)
future_mean = future_forecast.predicted_mean
future_interval = future_forecast.conf_int()

forecast_df = pd.DataFrame({
    "Forecast_Sales": future_mean,
    "Lower_Confidence": future_interval.iloc[:, 0],
    "Upper_Confidence": future_interval.iloc[:, 1]
})

forecast_df.index.name = "Date"
forecast_df.to_csv(OUTPUT_DIR / "future_sales_forecast.csv")

plt.figure(figsize=(12, 5))
plt.plot(sales.index, sales, label="Historical Sales")
plt.plot(
    future_mean.index,
    future_mean,
    label="Next 12 Months Forecast",
    marker="o"
)
plt.fill_between(
    future_mean.index,
    future_interval.iloc[:, 0],
    future_interval.iloc[:, 1],
    alpha=0.2,
    label="Confidence Interval"
)
plt.title("Sales Forecast for 2026")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "future_sales_forecast.png", dpi=150)
plt.close()

# --------------------------------------------------
# 11. Save a summary report
# --------------------------------------------------

best_model = comparison.loc[comparison["MAE"].idxmin(), "Model"]

report = f"""
# W10D1: Sales Time Series Analysis

## Dataset
- Records: {len(sales)}
- Period: {sales.index.min().date()} to {sales.index.max().date()}
- Frequency: Monthly
- Data type: Simulated educational sales data

## Trend and Seasonality
The sales series is analyzed for long-term trend and
recurring monthly seasonal patterns.

## Stationarity
- Original ADF p-value: {adf_original[1]:.6f}
- First-differenced ADF p-value: {adf_differenced[1]:.6f}

A p-value below 0.05 provides evidence against a unit root.

## Forecast Evaluation
- Training observations: {len(train)}
- Testing observations: {len(test)}
- Best model by test MAE: {best_model}

{comparison.to_string(index=False)}

## Forecasting Method
Seasonal ARIMA order: (1,1,1)
Seasonal order: (1,1,1,12)

The final model was fitted using all available observations
to forecast the next 12 months.

## Important Note
The dataset is simulated and the forecasts are for learning
and demonstration purposes, not actual business decisions.
"""

(REPORT_DIR / "W10D1_Time_Series_Analysis.md").write_text(
    report,
    encoding="utf-8"
)

print("\nFUTURE 12-MONTH SALES FORECAST")
print("-" * 40)
print(forecast_df.round(2).to_string())

print("\nAnalysis completed successfully!")
print("Charts and CSV results saved in the outputs folder.")
print("Written report saved in the reports folder.")
