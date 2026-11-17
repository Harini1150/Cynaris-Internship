from pathlib import Path
import nbformat as nbf

notebook = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell("""# W10D5 — Sales Forecasting Dashboard
## EDA on Indian Business Dataset

**Objective:** Explore Indian business orders, analyse monthly sales patterns, compare forecasting methods, and generate a 12-month sales forecast.

### Data sources
- `data/indian_business_orders.csv` — order-level business dataset.
- `data/monthly_sales.csv` — monthly sales time series containing simulated educational data (January 2019–December 2025).

**Important:** The monthly sales series is simulated, not verified real-world market data. It is used here to demonstrate time-series forecasting. The order-level dataset is analysed separately.

### Workflow
1. Load and validate both datasets.
2. Explore orders, revenue, profit, categories, and locations.
3. Analyse monthly sales trends and seasonality.
4. Compare a seasonal-naive baseline with Prophet using a chronological 12-month holdout.
5. Forecast the next 12 months and document business insights.
"""))

cells.append(nbf.v4.new_code_cell("""from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error
from prophet import Prophet

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda value: f"{value:,.2f}")
sns.set_theme(style="whitegrid")

PROJECT_DIR = Path.cwd()
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"
REPORT_DIR = PROJECT_DIR / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

orders_path = DATA_DIR / "indian_business_orders.csv"
sales_path = DATA_DIR / "monthly_sales.csv"

print("Project directory:", PROJECT_DIR)
print("Orders file exists:", orders_path.exists())
print("Monthly sales file exists:", sales_path.exists())

if not orders_path.exists() or not sales_path.exists():
    raise FileNotFoundError(
        "Run Jupyter from the W10D5 project folder so the data/ directory is available."
    )
"""))

cells.append(nbf.v4.new_code_cell("""orders = pd.read_csv(orders_path)
monthly_sales = pd.read_csv(sales_path)

orders["Order Date"] = pd.to_datetime(orders["Order Date"], errors="coerce")
monthly_sales["Date"] = pd.to_datetime(monthly_sales["Date"], errors="coerce")
monthly_sales["Sales"] = pd.to_numeric(monthly_sales["Sales"], errors="coerce")

monthly_sales = (
    monthly_sales.dropna(subset=["Date", "Sales"])
    .sort_values("Date")
    .reset_index(drop=True)
)

print("Orders shape:", orders.shape)
print("Monthly sales shape:", monthly_sales.shape)
display(orders.head())
display(monthly_sales.head())
"""))

cells.append(nbf.v4.new_markdown_cell("## 1. Data quality and overview"))

cells.append(nbf.v4.new_code_cell("""print("ORDER DATASET")
print("Date range:", orders["Order Date"].min(), "to", orders["Order Date"].max())
print("Duplicate rows:", orders.duplicated().sum())
display(orders.isna().sum().to_frame("Missing values"))
display(orders.describe(include="all").T)

print("\\\\nMONTHLY SALES DATASET")
print("Date range:", monthly_sales["Date"].min(), "to", monthly_sales["Date"].max())
print("Number of monthly observations:", len(monthly_sales))
print("Duplicate dates:", monthly_sales["Date"].duplicated().sum())
display(monthly_sales[["Date", "Sales"]].describe())
display(monthly_sales.isna().sum().to_frame("Missing values"))

if monthly_sales["Date"].duplicated().any():
    raise ValueError("Monthly sales contains duplicate dates.")
if len(monthly_sales) < 36:
    raise ValueError("At least 36 monthly observations are recommended for this exercise.")
"""))

cells.append(nbf.v4.new_markdown_cell("## 2. Exploratory data analysis — Indian business orders"))

cells.append(nbf.v4.new_code_cell("""# Key business indicators
total_sales = orders["Amount"].sum()
total_profit = orders["Profit"].sum()
total_quantity = orders["Quantity"].sum()
order_count = orders["Order ID"].nunique()
average_order_value = total_sales / order_count if order_count else np.nan

kpis = pd.Series({
    "Total sales": total_sales,
    "Total profit": total_profit,
    "Total quantity": total_quantity,
    "Unique orders": order_count,
    "Average order value": average_order_value
}, name="Value")

display(kpis.to_frame())

# Sales and profit by category
category_summary = (
    orders.groupby("Category", dropna=False)
    .agg(Sales=("Amount", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
    .sort_values("Sales", ascending=False)
)
display(category_summary)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
category_summary["Sales"].sort_values().plot(kind="barh", ax=axes[0], title="Sales by category")
category_summary["Profit"].sort_values().plot(kind="barh", ax=axes[1], title="Profit by category")
axes[0].set_xlabel("Sales")
axes[1].set_xlabel("Profit")
plt.tight_layout()
plt.show()

# Sales by state
state_summary = orders.groupby("State")["Amount"].sum().sort_values(ascending=False)
display(state_summary.head(10).to_frame("Sales"))

plt.figure(figsize=(11, 5))
state_summary.head(10).sort_values().plot(kind="barh")
plt.title("Top 10 states by sales")
plt.xlabel("Sales")
plt.tight_layout()
plt.show()

# Monthly order-level sales
orders["Order Month"] = orders["Order Date"].dt.to_period("M").dt.to_timestamp()
order_monthly = orders.groupby("Order Month").agg(
    Sales=("Amount", "sum"), Profit=("Profit", "sum")
).reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(order_monthly["Order Month"], order_monthly["Sales"], marker="o")
ax.set_title("Monthly sales — order-level dataset")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("## 3. Time-series analysis — monthly sales"))

cells.append(nbf.v4.new_code_cell("""sales = monthly_sales.copy()
sales = sales.rename(columns={"Date": "ds", "Sales": "y"})

fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(sales["ds"], sales["y"], marker="o", linewidth=1.5)
ax.set_title("Monthly sales over time (simulated dataset)")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
plt.tight_layout()
plt.show()

sales["Year"] = sales["ds"].dt.year
sales["Month"] = sales["ds"].dt.month
sales["Month_Name"] = sales["ds"].dt.month_name()

monthly_pattern = sales.groupby("Month")["y"].mean()
plt.figure(figsize=(11, 4))
sns.lineplot(x=monthly_pattern.index, y=monthly_pattern.values, marker="o")
plt.title("Average sales by calendar month")
plt.xlabel("Month number")
plt.ylabel("Average sales")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.show()

yearly_summary = sales.groupby("Year")["y"].agg(["mean", "min", "max"])
display(yearly_summary)
display(sales[["ds", "y"]].tail())
"""))

cells.append(nbf.v4.new_markdown_cell("""## 4. Forecast model evaluation

We reserve the **last 12 months** as a test set. Earlier observations are used for training. This preserves time order and avoids randomly mixing future observations into training.

The baseline predicts each test month using sales from the same month in the previous year. Prophet is then evaluated on exactly the same holdout period.

Metrics:
- **MAE:** average absolute prediction error.
- **RMSE:** gives larger errors more weight.
- **MAPE:** average percentage error; meaningful here because the sales values are positive.
"""))

cells.append(nbf.v4.new_code_cell("""HOLDOUT_MONTHS = 12

train = sales[["ds", "y"]].iloc[:-HOLDOUT_MONTHS].copy()
test = sales[["ds", "y"]].iloc[-HOLDOUT_MONTHS:].copy()

# Seasonal-naive baseline: repeat the values from the previous year.
baseline_predictions = sales["y"].iloc[-2 * HOLDOUT_MONTHS:-HOLDOUT_MONTHS].to_numpy()

if len(baseline_predictions) != len(test):
    raise ValueError("Could not construct the 12-month seasonal baseline.")

# Fit Prophet only on the training period.
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    seasonality_mode="additive"
)
model.fit(train)

prophet_predictions = model.predict(test[["ds"]])["yhat"].to_numpy()

def calculate_metrics(actual, predicted):
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    return {
        "MAE": mean_absolute_error(actual, predicted),
        "RMSE": np.sqrt(mean_squared_error(actual, predicted)),
        "MAPE (%)": np.mean(np.abs((actual - predicted) / actual)) * 100
    }

comparison = pd.DataFrame({
    "Seasonal Naive": calculate_metrics(test["y"], baseline_predictions),
    "Prophet": calculate_metrics(test["y"], prophet_predictions)
}).T

display(comparison)

evaluation = test.copy()
evaluation["Seasonal Naive"] = baseline_predictions
evaluation["Prophet"] = prophet_predictions
display(evaluation)

evaluation.to_csv(OUTPUT_DIR / "w10d5_model_evaluation.csv", index=False)

fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(test["ds"], test["y"], marker="o", label="Actual")
ax.plot(test["ds"], baseline_predictions, marker="o", label="Seasonal naive")
ax.plot(test["ds"], prophet_predictions, marker="o", label="Prophet")
ax.set_title("12-month holdout: actual vs predicted sales")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "w10d5_model_comparison.png", dpi=150, bbox_inches="tight")
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("## 5. Final model and 12-month forecast"))

cells.append(nbf.v4.new_code_cell("""# Refit Prophet on all available observations for the future forecast.
final_model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    seasonality_mode="additive"
)
final_model.fit(sales[["ds", "y"]])

future = final_model.make_future_dataframe(periods=12, freq="MS")
forecast = final_model.predict(future)

future_forecast = forecast.loc[
    forecast["ds"] > sales["ds"].max(),
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
].copy()

future_forecast = future_forecast.rename(columns={
    "ds": "Forecast Month",
    "yhat": "Predicted Sales",
    "yhat_lower": "Lower Estimate",
    "yhat_upper": "Upper Estimate"
})

future_forecast.to_csv(OUTPUT_DIR / "w10d5_12_month_forecast.csv", index=False)
display(future_forecast.round(2))

fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(sales["ds"], sales["y"], label="Historical sales")
ax.plot(forecast["ds"], forecast["yhat"], label="Prophet fitted/forecast")
ax.fill_between(
    forecast["ds"],
    forecast["yhat_lower"],
    forecast["yhat_upper"],
    alpha=0.2,
    label="Uncertainty interval"
)
ax.axvline(sales["ds"].max(), linestyle="--", label="Forecast starts")
ax.set_title("Prophet: historical sales and 12-month forecast")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "w10d5_12_month_forecast.png", dpi=150, bbox_inches="tight")
plt.show()

fig = final_model.plot_components(forecast)
fig.savefig(OUTPUT_DIR / "w10d5_forecast_components.png", dpi=150, bbox_inches="tight")
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("## 6. Findings, limitations, and conclusion"))

cells.append(nbf.v4.new_code_cell("""best_model = comparison["MAE"].idxmin()
best_mae = comparison.loc[best_model, "MAE"]

findings = [
    f"The order-level dataset contains {len(orders):,} rows and {orders['Order ID'].nunique():,} unique orders.",
    f"Total order-level sales are {total_sales:,.2f} and total profit is {total_profit:,.2f}.",
    f"The monthly time-series dataset contains {len(sales)} observations from {sales['ds'].min().date()} to {sales['ds'].max().date()}.",
    f"On the 12-month holdout, {best_model} achieved the lower MAE ({best_mae:,.2f}).",
    "The monthly sales series is simulated educational data; its patterns and forecasts must not be presented as verified real-world market predictions."
]

for item in findings:
    print("-", item)

print("\\\\nLimitations:")
print("- The monthly time series is simulated and may not represent actual business demand.")
print("- Forecast quality depends on the historical patterns continuing into the future.")
print("- A 12-month holdout is one evaluation window; performance can vary across other periods.")
print("- Forecast intervals represent model uncertainty, not guaranteed sales ranges.")

report_text = "# W10D5 Sales Forecasting — Summary\\\\n\\\\n"
report_text += "\\\\n".join(f"- {item}" for item in findings)
report_text += "\\\\n\\\\n## Model comparison\\\\n"
report_text += comparison.round(3).to_string()
report_text += "\\\\n\\\\n## Limitations\\\\n"
report_text += "\\\\n".join([
    "- Monthly sales data is simulated educational data.",
    "- Forecasts are estimates, not guarantees.",
    "- Results should be re-evaluated with real, regularly updated sales data."
])

(REPORT_DIR / "w10d5_forecasting_summary.txt").write_text(report_text, encoding="utf-8")
print("\\\\nSaved evaluation, forecast, charts, and summary under outputs/ and reports/.")
"""))

notebook["cells"] = cells
notebook["metadata"] = {
    "kernelspec": {
        "display_name": "Python (Cynaris W10D5)",
        "language": "python",
        "name": "cynaris-w10d5"
    },
    "language_info": {"name": "python", "version": "3.11"}
}

output_path = Path("W10D5_Sales_Forecasting_Dashboard.ipynb")
nbf.write(notebook, output_path)
print(f"Created: {output_path.resolve()}")
print(f"Notebook cells: {len(cells)}")
