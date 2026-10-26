# CIA Executive Insights Generator

## Overview

A Python-based business analytics application that analyzes CSV datasets, generates five exploratory data analysis (EDA) insights, creates an AI-powered executive summary, and exports a PowerPoint report.

## Features

- Upload business CSV files.
- View dataset dimensions and missing-cell counts.
- Preview records and descriptive statistics.
- Generate five automated EDA insights.
- Generate an executive summary using the Groq API.
- Display business recommendations.
- Download a seven-slide PowerPoint presentation.

## Technologies

- Python 3.11
- Pandas
- Streamlit
- Groq API
- python-pptx

## Project Files

- `app.py` — Streamlit application and EDA workflow.
- `executive_summary.py` — AI executive-summary generation.
- `powerpoint_export.py` — PowerPoint report creation.
- `sample_business_data.csv` — Sample dataset for testing.
- `requirements.txt` — Python dependencies.

## Setup

Install the dependencies from the repository root:

```powershell
py -3.11 -m pip install -r ".\Week 8\requirements.txt"
```

Configure the Groq API key in the PowerShell session used to run the app. Keep the key private and never commit it to Git.

Run the application:

```powershell
py -3.11 -m streamlit run ".\Week 8\app.py"
```

Open `http://localhost:8501` in your browser and upload `sample_business_data.csv`.

## Important Note

AI-generated summaries and automated insights should be reviewed before being used for business decisions. The sample dataset is small and is not representative of all business activity.

## Future Improvements

- Add correlation analysis and visualizations.
- Improve statistical checks and data-quality reporting.
- Add configurable recommendations based on business context.

## W8D3: PowerPoint Export Testing

- Updated the PowerPoint report branding to Week 8 Day 3.
- Updated the downloaded report filename to `CIA_Executive_Insights_W8D3.pptx`.
- Added consistent footers and slide numbering.
- Validated the PowerPoint generator using sample insights, an executive summary, and business recommendations.
- Confirmed that the generated presentation opens successfully and contains exactly seven slides.
- Verified Python syntax for `app.py`, `executive_summary.py`, and `powerpoint_export.py`.

### Test Result

**Status:** Passed

**Slides generated:** 7

**Test file size:** 35,547 bytes

The test presentation was temporary and was removed after validation.

