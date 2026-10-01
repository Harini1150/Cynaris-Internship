# Week 5 Day 2 - Automated EDA Summary

## Key Insights

1. **Sales, Quantity and Profit Relationships**
   The AutoViz correlation heatmap shows a weak positive relationship between Amount and Quantity (0.35). Amount and Profit also have a weak positive relationship (0.24), while Profit and Quantity have almost no linear relationship. These relationships are descriptive and do not establish causation.

2. **Quantity and Average Order Amount**
   The AutoViz categorical analysis shows that average Amount generally increases at higher Quantity levels, although the pattern is not perfectly consistent. Quantities of 13 and 14 show particularly high average Amount values.

3. **Distribution of Order Amount**
   The AutoViz distribution plot shows a bimodal pattern in Order Amount, with most observations concentrated in the lower range and a smaller secondary concentration around approximately 1,000-1,500.

## AutoViz vs SweetViz

AutoViz quickly generates a broad range of visualizations with minimal code, making it useful for rapid exploratory analysis. SweetViz produces a structured HTML report that organizes variable-level summaries, distributions, associations, and data-quality information. AutoViz is more visualization-oriented, while SweetViz provides a more organized report that is easier to navigate and share. Both tools reduce repetitive EDA coding and help analysts identify patterns quickly. Automated reports still require analyst validation and business context.

## Recommendation for Business Stakeholders

SweetViz can be used as the primary automated EDA reporting tool for business stakeholders because its structured HTML format is easier to review and share. AutoViz is useful for analysts during exploratory analysis because it generates multiple visualizations quickly. A practical workflow is to use AutoViz for initial exploration and SweetViz to present key findings in a more organized format. Automated findings should be validated against the underlying data before business decisions are made.
