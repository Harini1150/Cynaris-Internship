# W6D5: Natural-Language SQL Analyst API — Test Report

## Objective
Verify the Vanna-powered API can accept natural-language business questions and query the cynaris_sales MySQL database.

## API Details
- Framework: FastAPI
- Endpoint: POST /cia/sql-analyst
- Health endpoint: GET /health
- LLM: Qwen 2.5 3B through Ollama
- Database: MySQL (cynaris_sales)

## Tests
1. GET /health — tested successfully.
2. POST /cia/sql-analyst with question "What is the total sales value?" — tested successfully.
3. Earlier successful total sales result: 126200.00.
4. Earlier top-customer query returned Arun with sales of 55000.00 after SQL correction.

## Notes
- The API returns the Vanna agent responses as JSON.
- Verify query results against MySQL before relying on them for business decisions.
- Read-only SQL must be enforced by database permissions and query validation, not only by prompt instructions.
