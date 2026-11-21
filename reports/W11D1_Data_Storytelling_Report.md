\# W11D1 — Data Storytelling: Structure and Narrative



\*\*Project:\*\* EDA on Indian Business Dataset  

\*\*Topic:\*\* Data Storytelling Principles  

\*\*Date:\*\* 21 November 2026



\## 1. Objective



To communicate business insights clearly using the storytelling framework:



\*\*Context → Finding → Visual Evidence → Interpretation → Action\*\*



The analysis focuses on understanding how sales and profitability differ across product categories.



\## 2. Dataset Overview



\- Dataset: `indian\_business\_orders.csv`

\- Records: 1,500

\- Columns: 17

\- Period: 1 April 2018 – 31 March 2019

\- Unique orders: 500



\## 3. Key Business Metrics



| Metric | Value |

|---|---:|

| Total Sales | ₹4,31,502 |

| Total Profit | ₹23,955 |

| Overall Profit Margin | 5.55% |

| Unique Orders | 500 |



\### Category Performance



| Category | Sales | Profit | Profit Margin |

|---|---:|---:|---:|

| Clothing | ₹1,39,054 | ₹11,163 | 8.03% |

| Electronics | ₹1,65,267 | ₹10,494 | 6.35% |

| Furniture | ₹1,27,181 | ₹2,298 | 1.81% |



\## 4. Main Business Finding



\*\*High sales do not necessarily mean high profits.\*\*



Electronics generated the highest sales, while Clothing generated the highest total profit.



Furniture generated ₹1,27,181 in sales but contributed only ₹2,298 in profit, giving it the lowest profit margin at approximately 1.81%.



This makes Furniture a priority for further profitability analysis.



\## 5. Visual Evidence



Two charts were generated:



1\. `outputs/w11d1\_sales\_profit.png` — Sales and profit comparison across categories.

2\. `outputs/w11d1\_profit\_margin.png` — Profit margin comparison across categories.



Both charts use descriptive titles, labels and consistent formatting to support the narrative.



\## 6. Interpretation



Furniture's lower profit margin indicates that it converts a smaller proportion of sales into reported profit than the other categories.



Possible explanations include discounting, product mix or operational costs. However, the available dataset does not establish these causes.



Further analysis is required before recommending specific pricing or operational changes.



\## 7. Business Recommendations



1\. Analyse Furniture profitability by sub-category.

2\. Investigate discounting and delivery costs if those data become available.

3\. Compare profitability across product categories regularly.

4\. Create a recurring dashboard showing sales, profit and profit margin.

5\. Test potential improvements on a small scale before applying them broadly.



\## 8. CIA Interaction 1



\*\*Question:\*\* How can I structure a data storytelling presentation for business stakeholders using context, findings, visual evidence, interpretation and actionable recommendations?



\*\*CIA guidance:\*\* Organise the presentation around business context, key findings, simple charts, interpretation and practical recommendations. Use clear labels, relevant KPIs and Indian currency formatting.



\*\*What I learned:\*\* Data storytelling should lead stakeholders from the business question to evidence and then to a decision. Charts should support the message rather than simply decorate a presentation.



\*\*Application:\*\* Structured the notebook around Context → Finding → Evidence → Meaning → Action.



\## 9. CIA Interaction 2



\*\*Question:\*\* In my Indian Business Dataset EDA project, Furniture generated ₹1,27,181 in sales but only ₹2,298 in profit, with a 1.81% profit margin. How can I explain this finding to business stakeholders and recommend useful actions without making unsupported claims about the causes?



\*\*CIA guidance:\*\* Clearly state the measured result, separate possible explanations from confirmed findings, and recommend additional analyses such as cost-to-serve and product-level profitability.



\*\*What I learned:\*\* A responsible data story distinguishes evidence from hypotheses. A low margin is observable, but its causes require further investigation.



\*\*Application:\*\* Recommended examining Furniture profitability without claiming that discounts, logistics or returns are proven causes.



\## 10. Technical Verification



\- Notebook: `W11D1\_Data\_Storytelling.ipynb`

\- Python code cells: 6

\- Successfully executed cells: 6

\- Execution errors: 0

\- Generated charts: 2



\## 11. Limitations



\- The analysis covers only the available historical dataset.

\- Category-level results may hide differences between products.

\- The dataset does not contain all information needed to test cost-related hypotheses.

\- Findings should not be generalized to all Indian businesses.



\## 12. Conclusion



This task demonstrates how to transform exploratory data analysis into a business-focused narrative.



The central insight is that \*\*sales performance and profitability must be evaluated together\*\*.



Furniture's low profit margin provides a clear investigation priority, while the charts, interpretations and recommendations make the findings understandable and actionable for business stakeholders.



