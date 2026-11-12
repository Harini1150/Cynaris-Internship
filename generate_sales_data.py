
import numpy as np
import pandas as pd
from pathlib import Path

# Reproducible simulated monthly sales data
np.random.seed(42)

dates = pd.date_range(
    start="2019-01-01",
    end="2025-12-01",
    freq="MS"
)

n = len(dates)

# Long-term upward trend
trend = np.linspace(50000, 110000, n)

# Repeating yearly seasonal pattern
seasonal_pattern = {
    1: 0.90, 2: 0.92, 3: 0.95,
    4: 0.97, 5: 1.00, 6: 1.02,
    7: 1.04, 8: 1.03, 9: 1.06,
    10: 1.15, 11: 1.25, 12: 1.35
}

seasonality = np.array([
    seasonal_pattern[date.month] for date in dates
])

# Random variation
noise = np.random.normal(0, 3500, n)

sales = trend * seasonality + noise
sales = np.maximum(sales, 0).round(2)

df = pd.DataFrame({
    "Date": dates,
    "Sales": sales
})

output_path = Path("data/monthly_sales.csv")
df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print(f"Total records: {len(df)}")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print("\nFirst five records:")
print(df.head())
print(f"\nSaved to: {output_path}")
print("\nNote: This is simulated data created for educational analysis.")
