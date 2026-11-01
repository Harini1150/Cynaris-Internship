# Data Quality Scorecard

## Dataset
Cleaned Sales Dataset

## Overall Data Quality

| Dimension | Score | Status | Recommendation |
|---|---:|---|---|
| Completeness | 100% | PASS | Continue monitoring missing values |
| Accuracy | 100% | PASS | Validate values against business rules |
| Consistency | 100% | PASS | Maintain consistency across datasets |
| Timeliness | 100% | PASS | Monitor data refresh SLA |
| Uniqueness | 100% | PASS | Enforce unique sale IDs |
| Validity | 100% | PASS | Validate formats and allowed values |

## Great Expectations Validation

A Great Expectations suite containing 8 expectations was created.

Three intentional data-quality errors were injected:
1. Quantity was changed to 0.
2. Discount was changed to 150.
3. A duplicate sale ID was introduced.

Great Expectations successfully detected all three errors.

## PII Classification

- `customer_name` — PII; classified as confidential.
- `city` — potentially sensitive location data.
- Other columns — non-PII for this dataset.

## Recommendations

- Continue automated validation of required fields.
- Enforce unique sale IDs.
- Validate numerical ranges and allowed category values.
- Monitor data freshness against the defined SLA.
- Mask or tokenize customer names when data is shared with unauthorized users.

## Conclusion

The cleaned sales dataset passed all six DAMA-DMBOK data quality dimensions. Great Expectations validation demonstrated that the defined rules can detect common data-quality issues before the data is used for reporting or dashboards.