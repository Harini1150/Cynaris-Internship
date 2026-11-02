# W5D3 – DuckDB vs Pandas vs Polars

## Objective

Compare DuckDB, Pandas, and Polars for analytical operations on a 100,000-row CSV dataset.

The benchmark dataset is synthetic and was generated reproducibly using NumPy. It contains 100,000 orders and 8 columns: order ID, order date, category, state, city, quantity, amount, and profit.

## Dataset Validation

- Rows: 100,000
- Columns: 8
- Missing values: 0
- Duplicate rows: 0

## Analytical Queries

Five analytical operations were performed:

1. Total sales amount by category.
2. Average profit by state.
3. Total quantity by city.
4. Total sales amount by month.
5. Order count and total profit by category for orders with amount greater than 500.

The results produced by DuckDB, Pandas, and Polars were consistent for the five analytical queries.

## Benchmark Results

| Tool | Total Time |
|---|---:|
| Pandas | 2.5586 seconds |
| Polars | 1.6179 seconds |
| DuckDB | 1.3494 seconds |

For this dataset, machine, and workload, DuckDB recorded the lowest execution time, followed by Polars and Pandas. These results are workload-specific and should not be interpreted as a universal performance ranking.

## Pandas vs DuckDB vs Polars

| Criteria | Pandas | DuckDB | Polars |
|---|---|---|---|
| Query syntax | Python DataFrame API | SQL | DataFrame expression API |
| Execution approach | Eager in-memory processing | Vectorized analytical SQL engine | Columnar, parallel DataFrame engine |
| File analytics | Loads data into DataFrame | Can query files directly | Reads files into DataFrame/LazyFrame |
| Best use case | General data manipulation and EDA | Local analytical SQL and large-file analytics | High-performance DataFrame workflows |
| Ease of learning | Familiar for Python users | Easy for users familiar with SQL | Requires learning Polars expressions |

## Key Findings

- DuckDB performed fastest in this benchmark at 1.3494 seconds.
- Polars completed the same benchmark in 1.6179 seconds.
- Pandas completed the benchmark in 2.5586 seconds.
- All three tools produced consistent analytical results for the five queries.
- DuckDB is useful when analysts prefer SQL for analytical workloads and need to work directly with local files.
- Polars is useful for high-performance DataFrame processing.
- Pandas remains useful for general-purpose Python data analysis and exploratory data work.

## Business Recommendation

For SQL-based analytical workloads involving large local files, DuckDB is a strong option because it allows analysts to use familiar SQL without requiring a separate database server. Polars is useful when a high-performance Python DataFrame workflow is preferred, while Pandas remains suitable for general data analysis and EDA.

The benchmark should be repeated with larger datasets and representative production workloads before making a tool-selection decision for a production environment.

## Limitations

- The dataset is synthetic and contains 100,000 rows.
- The benchmark was performed on one machine.
- Execution time can vary depending on hardware, software versions, caching, and workload.
- The benchmark does not represent all possible Pandas, DuckDB, or Polars workloads.