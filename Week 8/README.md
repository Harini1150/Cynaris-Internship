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

## W8D4: Production Deployment and API Documentation

### Live Deployment
- **Application:** CIA Executive Insights Generator
- **Platform:** Render
- **Live URL:** https://cia-executive-insights-harini.onrender.com
- **Deployment Status:** Successfully deployed and tested

### Features
- CSV dataset upload and preview
- Dataset overview and descriptive statistics
- Automated exploratory data analysis (EDA) insights
- AI-generated executive summary
- AI-generated business recommendations
- PowerPoint executive report download

### Technology Stack
- Python 3
- Streamlit
- Pandas
- Groq API for AI-generated insights
- python-pptx for PowerPoint export
- Render for deployment

### Local Setup
1. Clone the repository.
2. Open the `Week 8` directory.
3. Install the dependencies:
   `pip install -r requirements.txt`
4. Configure the `GROQ_API_KEY` environment variable with a valid Groq API key.
5. Run the application:
   `streamlit run app.py`

### Deployment Configuration
- **Root directory:** `Week 8`
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- **Secret configuration:** `GROQ_API_KEY` is configured through Render environment variables.

### Deployment Verification
- Render build completed successfully.
- The application started and became live.
- A sample CSV containing 10 rows and 5 columns was uploaded successfully.
- Dataset overview, automated EDA insights, AI executive summary, and five business recommendations were displayed.
- The PowerPoint report was downloaded successfully.

### Known Limitations
- The sample dataset is small and its findings should not be generalized to a larger business population.
- AI-generated summaries and recommendations should be reviewed before business decisions are made.
- The Groq-powered features require a valid API key and available API service.
- The Render free instance may spin down after inactivity, delaying the first request while the service wakes up.

### Security
Never commit API keys or other secrets to the repository. Store deployment secrets in Render environment variables.

## W8D5: Full Demo and Final Verification

### Application Verification

The CIA Executive Insights Generator was tested using the sample business dataset.

- **CSV upload and processing:** Successfully processed the sample dataset.
- **Dataset overview:** Displayed 10 rows, 5 columns, and 0 missing cells.
- **Automated EDA:** Generated descriptive insights, including sales statistics and city frequency.
- **AI executive summary:** Generated a summary covering key findings, business implications, data-quality risks, and practical next steps.
- **Business recommendations:** Generated five AI-powered recommendations.
- **PowerPoint export:** Successfully downloaded the executive report.

### Test Dataset

The verification used a small sample dataset. Results are for demonstration purposes and should not be treated as conclusions about a larger business population.

### Deployment

Live application: https://cia-executive-insights-harini.onrender.com/

### Limitations

- Small datasets may not represent wider business trends.
- AI-generated insights and recommendations should be checked against the source data.
- AI features depend on the configured API service and its availability.
