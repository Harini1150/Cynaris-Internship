# W7D2 — AutoViz vs SweetViz

## Comparison (100 words)

AutoViz automatically generates a broad set of charts with little setup and is useful for analysts who want to quickly scan numeric and categorical relationships. Its interactive HTML output is convenient to explore but can produce several separate files and may need interpretation. SweetViz packages distributions, associations, and variable summaries into a polished, single HTML report that is easier to share with non-technical stakeholders. SweetViz is more presentation-friendly, while AutoViz offers flexible chart generation for exploratory work. Neither replaces data validation or business context. For this dataset, I recommend SweetViz for stakeholder review and AutoViz for analyst-led follow-up and investigation.


## Recommendation

Recommend SweetViz for the initial business-stakeholder review because its single HTML report is straightforward to share. Use AutoViz for analyst-led exploration and ydata-profiling for a more detailed check of distributions, correlations, and data quality. Validate all important findings with Pandas before presenting them.
