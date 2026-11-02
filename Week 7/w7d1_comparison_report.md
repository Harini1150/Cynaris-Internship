# W7D1 — PandasAI vs Manual Pandas Comparison

Dataset: `merged_orders_cleaned.csv`

Manual values were calculated independently using Pandas.
AI answers are recorded as returned and must be checked for equivalent meaning and units.

| Metric | Manual Pandas | PandasAI answer | Status |
|---|---:|---|---|
| Total sales | 431502.0 | 431502.0 | Review required |
| Total profit | 23955.0 | 23955.0 | Review required |
| Total quantity sold | 5615 | 5615 | Review required |

## Validation notes
- A matching-looking number is not proof of correctness.
- Check that each AI answer uses the correct column, aggregation, and units.
- Mark a result as matching only after verifying its meaning against the manual calculation.
- Review failed queries in `w7d1_errors.log`.
