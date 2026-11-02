
from pathlib import Path

import mlflow
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)

TRACKING_URI = (ROOT / "mlflow.db").as_uri().replace(
    "file:///", "sqlite:///"
)
EXPERIMENT_NAME = "W9D3_AB_Test_Tracking"

# Reproducible simulated experiment: 1,000 visitors per variant.
rng = np.random.default_rng(42)
visitors_per_variant = 1000

visitors_a = pd.DataFrame({
    "variant": "A",
    "converted": rng.binomial(1, 0.10, visitors_per_variant),
})
visitors_b = pd.DataFrame({
    "variant": "B",
    "converted": rng.binomial(1, 0.12, visitors_per_variant),
})

data = pd.concat([visitors_a, visitors_b], ignore_index=True)

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_registry_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

results = []

for variant in ["A", "B"]:
    group = data[data["variant"] == variant]
    conversions = int(group["converted"].sum())
    visitors = len(group)
    conversion_rate = conversions / visitors

    with mlflow.start_run(run_name=f"Variant_{variant}"):
        mlflow.log_param("variant", variant)
        mlflow.log_param("visitors", visitors)
        mlflow.log_metric("conversions", conversions)
        mlflow.log_metric("conversion_rate", conversion_rate)

    results.append({
        "variant": variant,
        "visitors": visitors,
        "conversions": conversions,
        "conversion_rate": conversion_rate,
    })

a = data[data["variant"] == "A"]["converted"]
b = data[data["variant"] == "B"]["converted"]

contingency_table = [
    [int(a.sum()), int(len(a) - a.sum())],
    [int(b.sum()), int(len(b) - b.sum())],
]

chi2, p_value, _, _ = chi2_contingency(
    contingency_table, correction=False
)

rate_a = results[0]["conversion_rate"]
rate_b = results[1]["conversion_rate"]
absolute_lift = rate_b - rate_a
relative_lift = (absolute_lift / rate_a) if rate_a else np.nan

report = pd.DataFrame(results)
report["absolute_lift_vs_A"] = [0.0, absolute_lift]
report["relative_lift_vs_A"] = [0.0, relative_lift]
report.to_csv(ARTIFACTS / "ab_test_results.csv", index=False)

summary = pd.DataFrame([{
    "experiment": EXPERIMENT_NAME,
    "chi_square": chi2,
    "p_value": p_value,
    "significance_level": 0.05,
    "statistically_significant": bool(p_value < 0.05),
    "absolute_lift": absolute_lift,
    "relative_lift": relative_lift,
}])
summary.to_csv(ARTIFACTS / "ab_test_summary.csv", index=False)

print("\nA/B TEST RESULTS")
print(report.to_string(index=False))
print("\nSTATISTICAL TEST")
print(summary.to_string(index=False))
print(f"\nReports saved in: {ARTIFACTS}")
print("SUCCESS: A/B test variants tracked in MLflow.")
