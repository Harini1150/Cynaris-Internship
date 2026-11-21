\# Week 11 Day 2 — Executive Business Report



\## 1. Project Overview



\*\*Internship:\*\* Cynaris Data Analyst Internship  

\*\*Project:\*\* Exploratory Data Analysis on Indian Business Dataset  

\*\*Task:\*\* Week 11 Day 2 — Executive Business Reporting



The objective of this task was to analyze Indian business sales data, develop interactive visualizations, identify important business trends, and present actionable insights in an executive-level PowerPoint presentation.



\## 2. Tools and Technologies



\- Python 3.12

\- Pandas for data analysis and aggregation

\- Plotly for interactive data visualization

\- Kaleido for exporting Plotly charts as PNG images

\- python-pptx for generating PowerPoint presentations

\- Git and GitHub for version control



\## 3. Dataset Overview



\*\*Dataset:\*\* `data/indian\_business\_orders.csv`



\- Total records: 1,500

\- Total columns: 17

\- Unique orders: 500

\- Main fields analyzed: Order Date, Amount, Profit, Category, and Order ID



The analysis focused on business revenue, profitability, category performance, and monthly sales trends.



\## 4. Key Performance Indicators



| KPI | Value |

|---|---:|

| Total Sales | ₹431,502 |

| Total Profit | ₹23,955 |

| Overall Profit Margin | 5.55% |

| Unique Orders | 500 |



Overall Profit Margin was calculated as:



\*\*Profit Margin (%) = (Total Profit / Total Sales) × 100\*\*



\## 5. Category Performance



| Category | Sales (₹) | Profit (₹) | Profit Margin |

|---|---:|---:|---:|

| Clothing | 139,054 | 11,163 | 8.03% |

| Electronics | 165,267 | 10,494 | 6.35% |

| Furniture | 127,181 | 2,298 | 1.81% |



\### Key Findings



1\. Electronics generated the highest sales at ₹165,267.

2\. Clothing generated the highest profit at ₹11,163.

3\. Clothing achieved the strongest profit margin at 8.03%.

4\. Furniture had the lowest profit margin at 1.81%.

5\. The overall business profit margin was 5.55%.



\## 6. Data Visualizations



Three interactive charts were created using Plotly:



\### Monthly Sales Trend



\*\*File:\*\* `outputs/w11d2\_monthly\_sales.html`



Displays monthly sales performance to help identify changes in revenue over time.



\### Category Sales vs Profit



\*\*File:\*\* `outputs/w11d2\_category\_sales\_profit.html`



Compares total sales and profit across Clothing, Electronics, and Furniture.



\### Category Profit Margin



\*\*File:\*\* `outputs/w11d2\_category\_profit\_margin.html`



Compares category profitability and highlights Furniture's relatively low margin.



PNG versions of all three charts were also generated for

