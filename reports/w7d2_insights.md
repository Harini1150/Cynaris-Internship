# W7D2 — Automated EDA: Business Insights

## Dataset overview
- Rows: 1,500
- Columns: 17
- Total sales amount: 431,502.00
- Total profit: 23,955.00

## Three business insights

### 1. Electronics leads sales
Electronics has the highest category sales at 165,267.00, representing 38.3% of total sales.

### 2. Clothing leads total profit
Clothing generates the highest category profit (11,163.00) with a profit-to-sales ratio of 8.0%. Furniture generates only 2,298.00 profit (1.8% of its sales), so its costs, pricing, and discounting deserve further review.

### 3. Negative-profit records need attention
503 of 1,500 rows (33.5%) have negative profit. Investigate the loss-making transactions by category, sub-category, and city before making pricing or supplier decisions.

## Top five cities by sales

| City | Sales amount |
|---|---:|
| Indore | 79,069.00 |
| Mumbai | 61,867.00 |
| Pune | 33,481.00 |
| Delhi | 25,019.00 |
| Bhopal | 23,583.00 |

## Text data quality checks

Leading/trailing whitespace was detected in these text columns:
- `State`: 45 value(s)

Standardize whitespace before grouping or comparing these fields.

## Method
These figures were calculated using Pandas groupby and aggregation. The HTML profiling tools are used to explore distributions and data-quality patterns; key business totals should still be validated independently.
