from pathlib import Path
import warnings

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "monthly_sales.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
REPORT_DIR = BASE_DIR / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# 1. Load and prepare the dataset
data = pd.read_csv(DATA_PATH)
data["Date"] = pd.to_datetime(data["Date"])

df = data.rename(columns={"Date": "ds", "Sales": "y"})
df = df[["ds", "y"]].sort_values("ds").dropna().reset_index(drop=True)

if len(df) < 36:
    raise ValueError("At least 36 monthly observations are recommended.")

if df["ds"].duplicated().any():
    raise ValueError("Duplicate dates found. Please clean the dataset.")

print("\nDATASET OVERVIEW")
print("----------------")
print(f"Total observations: {len(df)}")
print(f"Start date: {df['ds'].min().date()}")
print(f"End date: {df['ds'].max().date()}")
print(f"Average monthly sales: {df['y'].mean():,.2f}")

# 2. Hold out the last 12 months for evaluation
train = df.iloc[:-12].copy()
test = df.iloc[-12:].copy()

evaluation_model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    seasonality_mode="additive"
)

evaluation_model.fit(train)

test_forecast = evaluation_model.predict(test[["ds"]])
comparison = test[["ds", "y"]].copy()
comparison["Predicted_Sales"] = test_forecast["yhat"].values
comparison["Absolute_Error"] = (
    comparison["y"] - comparison["Predicted_Sales"]
).abs()

mae = mean_absolute_error(
    comparison["y"], comparison["Predicted_Sales"]
)
rmse = np.sqrt(
    mean_squared_error(comparison["y"], comparison["Predicted_Sales"])
)
mape = (
    np.mean(
        np.abs(
            (comparison["y"] - comparison["Predicted_Sales"])
            / comparison["y"].replace(0, np.nan)
        )
    ) * 100
)

comparison.to_csv(OUTPUT_DIR / "prophet_test_predictions.csv", index=False)

# 3. Train the final model on all available observations
final_model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    seasonality_mode="additive"
)

final_model.fit(df)

future = final_model.make_future_dataframe(
    periods=12,
    freq="MS"
)

forecast = final_model.predict(future)

forecast_output = forecast[
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
].tail(12).copy()

forecast_output.to_csv(
    OUTPUT_DIR / "prophet_12_month_forecast.csv",
    index=False
)

# 4. Save the forecast graph
fig1 = final_model.plot(forecast)
fig1.suptitle("Monthly Sales Forecast Using Prophet", fontsize=14)
fig1.tight_layout()
fig1.savefig(
    OUTPUT_DIR / "prophet_forecast.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close(fig1)

# 5. Save the trend and seasonality components
fig2 = final_model.plot_components(forecast)
fig2.tight_layout()
fig2.savefig(
    OUTPUT_DIR / "prophet_components.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close(fig2)

# 6. Save evaluation metrics and summary
summary = f"""
PROPHET MONTHLY SALES FORECASTING REPORT
=========================================

Dataset: data/monthly_sales.csv
Observations: {len(df)}
Historical period: {df['ds'].min().date()} to {df['ds'].max().date()}

MODEL
-----
Algorithm: Facebook Prophet
Yearly seasonality: Enabled
Weekly seasonality: Disabled
Daily seasonality: Disabled
Seasonality mode: Additive

EVALUATION
----------
Training observations: {len(train)}
Testing observations: {len(test)}
Testing period: {test['ds'].min().date()} to {test['ds'].max().date()}

MAE: {mae:,.2f}
RMSE: {rmse:,.2f}
MAPE: {mape:.2f}%

NEXT 12 MONTHS FORECAST
-----------------------
Forecast start: {forecast_output['ds'].min().date()}
Forecast end: {forecast_output['ds'].max().date()}
Average predicted sales: {forecast_output['yhat'].mean():,.2f}
Minimum predicted sales: {forecast_output['yhat'].min():,.2f}
Maximum predicted sales: {forecast_output['yhat'].max():,.2f}

NOTE
----
This analysis uses the monthly sales dataset available in the W10D2
worktree. It is a sales time-series exercise, not an external
Indian stock-market forecast. Forecast values are estimates, not guarantees.
"""

(REPORT_DIR / "prophet_forecasting_report.txt").write_text(
    summary, encoding="utf-8"
)

print("\nMODEL EVALUATION")
print("----------------")
print(f"MAE:  {mae:,.2f}")
print(f"RMSE: {rmse:,.2f}")
print(f"MAPE: {mape:.2f}%")

print("\nNEXT 12 MONTHS FORECAST")
print("-----------------------")
print(forecast_output.to_string(index=False))

print("\nFILES CREATED")
print("-------------")
print("outputs/prophet_test_predictions.csv")
print("outputs/prophet_12_month_forecast.csv")
print("outputs/prophet_forecast.png")
print("outputs/prophet_components.png")
print("reports/prophet_forecasting_report.txt")
print("\nProphet forecasting completed successfully!")
