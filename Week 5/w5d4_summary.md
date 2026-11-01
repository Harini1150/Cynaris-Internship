# W5D4 – Polars: High-Performance DataFrame Operations

## Objective

Explore Polars for high-performance DataFrame operations using a 100,000-row synthetic dataset. Perform analytical operations and compare eager and lazy execution.

## Dataset Validation

- Rows: 100,000
- Columns: 8
- Missing values: 0
- Duplicate rows: 0

## Analytical Operations

Five analytical operations were completed:

1. Total sales amount by category.
2. Average profit by state.
3. Total quantity by city.
4. Monthly total sales amount.
5. Order count and total profit by category for orders with amount greater than 500.

The results matched the corresponding W5D3 benchmark results.

## Eager vs Lazy Execution

| Execution mode | Time |
|---|---:|
| Eager | 0.0232 seconds |
| Lazy | 0.0993 seconds |

The results matched after rounding to two decimal places.

Eager execution operated on an already-loaded DataFrame. Lazy execution scanned the CSV and collected the optimized query. Since the data-loading conditions were different, these timings are not a direct performance comparison.

## Key Findings

- Polars supports expressive DataFrame operations for grouping, aggregation, filtering, sorting, and date-based analysis.
- Eager execution is convenient when immediate results are required.
- Lazy execution allows query optimization before execution.
- Both execution modes produced equivalent analytical results in the category-sales test.
- Performance depends on data size, query complexity, memory, and whether data loading is included.

## Business Recommendation

Polars is useful for Python-based analytical workflows that need efficient DataFrame processing. Eager execution is suitable for interactive analysis, while lazy execution can be useful for complex pipelines where query optimization may reduce unnecessary work.

## Limitations

- The dataset is synthetic and contains 100,000 rows.
- The benchmark was run on one machine.
- The eager and lazy timings included different data-loading conditions.
- More representative workloads and repeated tests are needed for a reliable performance comparison.