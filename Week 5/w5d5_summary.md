# Week 5 Day 5: AI-Powered EDA

## Objective

Explore an Indian business sales dataset using PandasAI and Google's Gemini model to generate insights through natural-language queries.

## Tools and Technologies

* Python
* Pandas
* PandasAI
* Google Gemini
* Matplotlib
* Jupyter Notebook

## Dataset

* File: `merged_orders_cleaned.csv`
* Rows: 1,500
* Columns: 17
* Missing values: 0

## Implementation

1. Loaded and inspected the cleaned sales dataset using Pandas.
2. Configured PandasAI with Gemini through LiteLLM.
3. Queried the dataset using natural language.
4. Compared AI-generated outputs with previously calculated Pandas aggregations.
5. Created a bar chart comparing total sales by product category.

## Key Findings

| Analysis                    | Result                 |
| --------------------------- | ---------------------- |
| Lowest-profit state         | Tamil Nadu: −₹2,216    |
| Highest-sales category      | Electronics: ₹1,65,267 |
| Highest-profit sub-category | Printers: ₹5,964       |

## Visualization

Created a bar chart titled **Total Sales by Product Category** to compare sales across Electronics, Clothing, and Furniture.

## Validation

The three AI-generated findings were checked against Pandas aggregation results and matched.

## Challenges

The initial Gemini model was unavailable. Updating the model configuration to `gemini/gemini-3.8-flash` resolved the direct Gemini connection issue. LiteLLM messages continued to appear during some PandasAI queries, although the requested results were returned.

## Conclusion

PandasAI and Gemini enabled natural-language exploration of the sales dataset. Comparing the generated results with Pandas calculations helped validate the insights and demonstrate the usefulness of AI-assisted exploratory data analysis.
