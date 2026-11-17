

\# W10D4 – Forecasting Dashboard Using Plotly and Streamlit



\## 1. Project Overview



The objective of this task was to develop an interactive sales forecasting dashboard using Python, Plotly, and Streamlit.



The dashboard analyses the Indian Business Orders dataset and provides historical sales insights, short-term sales predictions, and interactive data exploration.



\## 2. Dataset Details



\- Dataset: Indian Business Orders

\- Total records: 1,500

\- Date range: April 2018 to March 2019

\- Number of months: 12

\- Key columns: Order Date, Amount, Profit, Quantity, Category, State, and City.



\## 3. Technologies Used



\- Python 3.11

\- Pandas – Data cleaning and analysis

\- NumPy – Numerical operations

\- Scikit-learn – Linear Regression forecasting

\- Plotly – Interactive visualisations

\- Streamlit – Dashboard development



\## 4. Dashboard Features



The dashboard includes:



1\. Interactive date, category, and state filters.

2\. KPI cards displaying total sales, profit, unique orders, and average order value.

3\. Monthly sales trend visualisation.

4\. Future sales forecasting for 3, 6, or 12 months.

5\. Forecast evaluation using Mean Absolute Error (MAE).

6\. Category-wise sales performance.

7\. State-wise sales analysis.

8\. Filtered order records in tabular format.

9\. CSV download functionality for forecast results.



\## 5. Forecasting Methodology



A Linear Regression model was used to identify the trend in monthly sales.



The month sequence was used as the input feature, and monthly sales were used as the target variable.



The last three available monthly observations were reserved for chronological holdout evaluation. The model was evaluated using Mean Absolute Error (MAE).



After evaluation, the model was trained again using all available selected monthly observations to generate future sales predictions.



Negative predictions were restricted to zero.



\## 6. Forecast Results



The dashboard generated the following three-month forecast using the default settings:



| Month | Forecast Sales |

|---|---:|

| April 2019 | ₹54,624.68 |

| May 2019 | ₹57,496.40 |

| June 2019 | ₹60,368.12 |



The forecast indicates an increasing sales trend over the selected forecast period.



The results are indicative estimates and should not be treated as guaranteed future sales.



\## 7. Default Dashboard KPIs



\- Total Sales: ₹4,31,502

\- Total Profit: ₹23,955

\- Unique Orders: 500

\- Average Order Value: ₹863



\## 8. Challenges and Solutions



\### Challenge 1: Limited historical data



The dataset contained only 12 months of observations.



Solution: A simple Linear Regression baseline was selected instead of claiming reliable yearly seasonality from limited data.



\### Challenge 2: Interactive dashboard development



Multiple charts and filters needed to work together.



Solution: Streamlit widgets were used for filtering, while Plotly was used to create interactive charts.



\### Challenge 3: Forecast evaluation



It was important to evaluate the model before generating future predictions.



Solution: The last three observations were kept aside for chronological holdout evaluation using MAE.



\## 9. Limitations



\- Only one year of historical data was available.

\- Linear Regression captures a general trend but may not capture seasonal patterns.

\- The forecast does not account for external factors such as promotions, holidays, or market changes.

\- More historical observations are needed for stronger forecasting validation.



\## 10. Future Improvements



\- Use multiple years of sales data.

\- Compare Linear Regression with Prophet, ARIMA, and other forecasting models.

\- Introduce time-series cross-validation.

\- Add prediction intervals.

\- Include external business factors.

\- Improve dashboard layout and reporting features.



\## 11. Conclusion



The W10D4 task successfully demonstrated how Python, Plotly, and Streamlit can be combined to build an interactive sales forecasting dashboard.



The project provides historical sales analysis, short-term forecasts, performance visualisations, and downloadable forecast results.



