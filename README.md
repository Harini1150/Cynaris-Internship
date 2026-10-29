# Cynaris Internship

## Week 3 – Day 4: Looker Studio Dashboard

### Project: Sales Performance Dashboard

Created an interactive dashboard using Google Looker Studio and Google Sheets.

### Dashboard Features
- Revenue scorecard
- Revenue by city (bar chart)
- Revenue over time (line chart)
- Revenue by category (pie chart)
- Product revenue table
- Date range control
- City and category filters
- Custom dashboard theme

### Dashboard Link
[View Looker Studio Dashboard](https://datastudio.google.com/reporting/1e58a2ed-1e6a-4aa1-a9f7-731d10dbbbef)

### Screenshot
![Looker Studio Dashboard](Week%203/looker_studio_dashboard.png)

# W9D3: A/B Test Tracking with MLflow

## Objective
Track and compare two variants of a simulated A/B test using MLflow. Calculate conversion rates, measure performance lift, and use a chi-square test to evaluate whether the observed difference is statistically significant.

## Tools and Technologies
- Python
- MLflow
- Pandas
- NumPy
- SciPy
- SQLite
- Git and GitHub

## Experiment Design
- **Variant A:** Control group representing the existing experience.
- **Variant B:** Treatment group representing a proposed alternative.
- **Sample size:** 1,000 simulated visitors per variant.
- **Primary metric:** Conversion rate.
- **Statistical method:** Chi-square test of independence.
- **Significance threshold:** 0.05.

## Results

| Metric | Variant A | Variant B |
|---|---:|---:|
| Visitors | 1,000 | 1,000 |
| Conversions | 98 | 128 |
| Conversion rate | 9.8% | 12.8% |

The absolute conversion-rate lift was 3 percentage points. The relative lift was approximately 30.6%.

The chi-square test returned a p-value of 0.0341. Since this is below the predefined 0.05 threshold, the observed difference is statistically significant for this simulated dataset.

## MLflow Tracking
The experiment is named `W9D3_AB_Test_Tracking`. Separate MLflow runs named `Variant_A` and `Variant_B` record the variant, visitor count, conversion count, and conversion rate.

## Generated Artifacts
- `ab_test_tracking.py` — reproducible A/B experiment and MLflow logging script.
- `artifacts/ab_test_results.csv` — variant-level conversion results and lift.
- `artifacts/ab_test_summary.csv` — statistical test result and significance assessment.
- `artifacts/ab_test_mlflow_dashboard.png` — reserved for the MLflow evidence screenshot.

## How to Run
Activate the project's virtual environment, then execute:

```powershell
python .\ab_test_tracking.py
```

The script creates the MLflow experiment and generates the CSV reports in the `artifacts` folder.

## Limitations
The data is simulated and does not represent actual customers or business outcomes. Statistical significance does not establish practical business value or guarantee that the result will generalize. A real experiment should use appropriate random assignment, sufficient sample size, predefined metrics, and checks for bias and other experimental issues.

## Conclusion
This exercise demonstrates how to log A/B test variants in MLflow, compare conversion rates, calculate absolute and relative lift, and use statistical testing to assess an observed difference.
