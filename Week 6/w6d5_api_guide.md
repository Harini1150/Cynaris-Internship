# W6D5: CIA SQL Analyst API Guide

## Prerequisites
- Python virtual environment activated.
- Ollama running with the `qwen2.5:3b` model available.
- MySQL running with the `cynaris_sales` database configured.
- Environment variables configured in `Week 6/.env`.

## Start the API
From the repository root, run:

    python -m uvicorn --app-dir "Week 6" cia_sql_analyst_api:app --host 127.0.0.1 --port 8001

## Open API Documentation
Visit http://127.0.0.1:8001/docs

## Available Endpoints
- `GET /health` — checks API health.
- `POST /cia/sql-analyst` — accepts a natural-language SQL question.

## Example Request
    {
      "question": "What is the total sales value?"
    }

## Expected Behavior
The API passes the question and database schema context to the Vanna agent and returns the agent responses as JSON. Confirm the SQL and result against MySQL.

## Safety
Keep the API bound to localhost during development. Use a read-only database account and enforce SQL validation before exposing it beyond the local machine.
