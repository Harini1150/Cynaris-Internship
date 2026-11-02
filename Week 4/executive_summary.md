# Executive Summary – Superstore Sales & Profitability Analysis

## Business Question

Which products, regions, customer segments, and discount levels are driving sales and profitability, and what actions can the business take to improve profitability?

## Dataset

- Source: Kaggle Sample Superstore dataset
- Records: 10,194
- Variables: 21
- Analysis tools: Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy, and Power BI

## Key Findings

1. Technology generated the highest sales (₹839,893.28) and strong total profit (₹146,543.38) among the three categories.
2. The West region generated ₹739,813.61 in sales and ₹110,798.82 in profit, while the East region generated ₹691,828.17 in sales and ₹94,883.26 in profit.
3. Tables, Bookcases, and Supplies were loss-making sub-categories, with Tables showing the largest total loss.
4. Consumer customers generated the highest sales (₹1,170,659.79) and profit (₹136,371.45) among the three customer segments.
5. Discounted orders had a lower average profit than non-discounted orders. The Welch two-sample t-test produced a p-value below 0.05, indicating a statistically significant difference in average profit between the two groups.
6. The correlation between discount and profit was negative, indicating that higher discount levels were associated with lower profit in this dataset.

## Recommendations

### 1. Introduce Discount Guardrails

Review high-discount orders and introduce margin-based discount limits. Monitor profitability by discount level, product category, and region before approving larger discounts.

### 2. Review Loss-Making Sub-Categories

Investigate Tables, Bookcases, and Supplies to identify the reasons for negative profitability. Review pricing, product costs, shipping expenses, and discount practices and take corrective action where required.

### 3. Protect and Expand High-Performing Areas

Continue monitoring strong-performing areas such as Technology, the West region, and the Consumer segment. Identify the products and practices contributing to their performance and evaluate opportunities to replicate them in other areas.

## Statistical Interpretation

The statistical test found a significant difference in average profit between discounted and non-discounted orders. However, this result shows an association and does not prove that discounts directly caused lower profit. Other factors such as product type, region, order size, and costs may also influence profitability.

## Limitations

- The analysis is based on the available Sample Superstore dataset.
- Statistical relationships should not automatically be interpreted as causal relationships.
- Further analysis with cost, shipping, customer-level, and product-level information could provide deeper business insights.