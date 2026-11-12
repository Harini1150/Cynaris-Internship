# W10D3 - Anomaly Detection
## Indian Business Orders Dataset

### 1. Project Objective
The objective of this task is to identify unusual business transactions using statistical and machine-learning anomaly detection techniques.

### 2. Dataset Overview
- Dataset: Indian Business Orders
- Source file: data/indian_business_orders.csv
- Total records: 1,500
- Total columns: 17
- Missing values: 0
- Duplicate rows: 0

### 3. Features Used
- Amount: Order transaction amount
- Profit: Profit or loss from the order
- Quantity: Number of items ordered

### 4. Techniques Implemented

#### IQR (Interquartile Range)
IQR is a statistical technique used to identify potential outliers.

IQR = Q3 - Q1

Lower Bound = Q1 - (1.5 * IQR)

Upper Bound = Q3 + (1.5 * IQR)

Values outside these bounds are flagged as potential anomalies.

#### Isolation Forest
Isolation Forest is an unsupervised machine-learning algorithm that identifies unusual observations by isolating data points.

- Prediction -1: Anomaly
- Prediction 1: Normal observation
- Number of estimators: 100
- Contamination: 0.05
- Random state: 42

The contamination value is a modeling assumption of 5%, not a confirmed anomaly rate.

### 5. IQR Results

| Feature | Q1 | Q3 | IQR | Lower Bound | Upper Bound | Anomalies |
|---|---:|---:|---:|---:|---:|---:|
| Amount | 45.00 | 322.00 | 277.00 | -370.50 | 737.50 | 155 |
| Profit | -9.25 | 38.00 | 47.25 | -80.12 | 108.88 | 291 |
| Quantity | 2.00 | 5.00 | 3.00 | -2.50 | 9.50 | 23 |

The combined IQR method flagged 343 unique records.

### 6. Isolation Forest Results
- Total records analyzed: 1,500
- Anomalies detected: 75
- Normal records: 1,425
- Anomaly percentage: 5%

### 7. Comparison of Methods

| Method | Anomaly Count | Percentage |
|---|---:|---:|
| IQR | 343 | 22.87% |
| Isolation Forest | 75 | 5.00% |
| Both Methods | 75 | 5.00% |

Additional comparison:
- IQR only: 268 records
- Isolation Forest only: 0 records
- Detected by both: 75 records
- Neither method: 1,157 records

All Isolation Forest anomalies were also flagged by the combined IQR method in this experiment.

### 8. Visualizations
The project generates:
1. Amount vs Profit anomaly scatter plot.
2. Boxplots for Amount, Profit and Quantity.
3. Anomaly count comparison across detection methods.

### 9. Output Files
- outputs/anomaly_detection_results.csv
- outputs/iqr_summary.csv
- outputs/anomaly_summary.csv
- outputs/top_anomalies.csv
- outputs/anomaly_detection_amount_profit.png
- outputs/anomaly_feature_boxplots.png
- outputs/anomaly_method_comparison.png

Evidence copies of the three visualizations are stored in the evidence folder.

### 10. Key Findings
- Profit had the highest individual IQR outlier count, with 291 flagged values.
- Amount had 155 potential outliers.
- Quantity had 23 potential outliers.
- IQR identified more potential outliers than Isolation Forest.
- All 75 Isolation Forest anomalies were also identified by the combined IQR method.

### 11. Limitations
- Statistical outliers are not necessarily incorrect transactions.
- The Isolation Forest contamination setting affects the number of anomalies flagged.
- The analysis uses only Amount, Profit and Quantity as model features.
- Further business investigation is needed before treating any flagged transaction as an error or suspicious activity.

### 12. Conclusion
Both IQR and Isolation Forest were successfully implemented on the Indian Business Orders dataset. The comparison demonstrates how statistical and machine-learning methods can identify unusual business transactions from different perspectives.

The analysis provides a starting point for further investigation of unusual order amounts, profit values and quantities.
