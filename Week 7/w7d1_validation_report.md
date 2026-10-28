

\# W7D1: PandasAI Validation Report



\## 1. Dataset

\- File: merged\_orders\_cleaned.csv

\- Rows: 1,500

\- Columns: 17

\- Tool: PandasAI 2.3.2

\- Local language model: Ollama qwen2.5:3b

\- Validation: Manual Pandas calculations



\## 2. Natural-Language Query Results



| No. | Analysis | Result | Validation |

|---|---|---|---|

| 1 | Total sales | 431502.0 | Matched manual Pandas |

| 2 | Total profit | 23955.0 | Matched manual Pandas |

| 3 | Total quantity | 5615 | Matched manual Pandas |

| 4 | Category-wise sales | No result returned | Failed; requires handling |

| 5 | Category-wise profit | Furniture: 2298; Electronics: 10494; Clothing: 11163 | Matched manual Pandas |

| 6 | Top five cities by sales | Indore: 79069; Mumbai: 61867; Pune: 33481; Delhi: 25019; Bhopal: 23583 | Matched manual Pandas |

| 7 | Top five states by sales | Madhya Pradesh: 105140; Maharashtra: 95348; Delhi: 22531; Uttar Pradesh: 22359; Rajasthan: 21149 | Sales values matched; extra numeric columns were also returned |

| 8 | Top five sub-categories by profit | Printers: 5964; Bookcases: 4888; Accessories: 3559; Trousers: 2847; Stole: 2559 | Matched manual Pandas |

| 9 | Unique customers | 332 | Matched manual Pandas |

| 10 | Rows with negative profit | 503 | Matched manual Pandas |



\## 3. Manual Pandas vs PandasAI



The three direct numerical comparisons were:



| Metric | Manual Pandas | PandasAI | Outcome |

|---|---:|---:|---|

| Total sales | 431502.0 | 431502.0 | Match |

| Total profit | 23955.0 | 23955.0 | Match |

| Total quantity | 5615 | 5615 | Match |



\## 4. Error Handling and Limitations



\- Query 4 failed with `NoResultFoundError: No result returned`.

\- Query 7 returned the correct top-state sales amounts but also included sums for other numeric columns. This shows why AI-generated results require validation.

\- The script records query failures in `w7d1\_errors.log` and saves query results to `w7d1\_query\_results.json`.

\- A successful response does not automatically mean the answer is correct.



\## 5. Conclusion



PandasAI successfully answered most of the business questions using the local Qwen model. The three direct numerical comparisons matched manual Pandas exactly. The failed category-sales query and extra columns in the state analysis demonstrate the importance of error handling, result validation, and deterministic calculations for critical business metrics.



