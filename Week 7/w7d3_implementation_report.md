\# W7D3 — Plotly and ECharts Dashboard



\## Objective

Create an interactive retail analytics dashboard demonstrating

Plotly and ECharts chart generation for the W7D3 task.



\## Implementation

\- Loaded the Indian retail CSV dataset containing 1,500 rows and 17 columns.

\- Used Python's built-in CSV module to calculate dashboard metrics.

\- Generated a standalone HTML dashboard with four interactive charts.

\- Used Plotly for sales by category and profit by category.

\- Used ECharts for top cities by sales and monthly sales.

\- Added responsive layouts, hover tooltips, and chart resizing.

\- Displayed sales, profit, quantity, and negative-profit row metrics.



\## Validated Metrics

\- Total sales: 431,502.00

\- Total profit: 23,955.00

\- Total quantity sold: 5,615

\- Rows with negative profit: 503



\## Testing

Command:

`python -m unittest "Week 7\\test\_w7d3\_dashboard.py"`



Result: 5 tests passed.



The tests check the dataset shape, business metrics, Plotly chart calls,

ECharts initialization, and all four chart containers.



The dashboard was also opened in a browser, and all four charts were

visually confirmed to appear.



\## Design Decisions

Plotly was used for category comparisons because interactive bars make

relative sales and profit easy to inspect. ECharts was used for city

ranking and monthly sales, providing a horizontal ranking chart and a

zoomable time-series chart.



\## Limitation

This worktree did not contain the CIA frontend application. The

deliverable is therefore a standalone HTML dashboard demonstrating

both chart libraries, rather than a direct integration into the

existing CIA frontend. Integration can be completed when the actual

frontend source and approved patterns are available.



The chart libraries are loaded from online CDNs, so an internet

connection is required to render the interactive charts.



\## Potential Improvements

\- Integrate the charts into the actual CIA frontend.

\- Add date and category filters.

\- Add accessibility checks and a browser-based test.

\- Validate behavior when CDN resources

