
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from vanna_sql_analyst import agent, schema_context
from vanna.core.user import RequestContext

app = FastAPI(
    title="Cynaris CIA SQL Analyst API",
    version="1.0.0",
)


class SQLQuestion(BaseModel):
    question: str = Field(min_length=3, max_length=1000)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "CIA SQL Analyst"}


@app.post("/cia/sql-analyst")
async def sql_analyst(payload: SQLQuestion):
    question = payload.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty.",
        )

    prompt = f"""
{schema_context}

Answer the business question using the available SQL tool.
Prefer read-only SELECT queries. Do not modify database data.
Calculate sales as quantity * price.

User question:
{question}
"""

    try:
        request_context = RequestContext()
        responses = []

        async for response in agent.send_message(
            request_context,
            prompt,
        ):
            responses.append(response.model_dump(mode="json"))

        return {
            "question": question,
            "responses": responses,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The SQL analyst could not process the question. Check server logs.",
        )
