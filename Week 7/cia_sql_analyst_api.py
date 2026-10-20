from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from w7d4_vanna_sql_analyst import ask_sql_analyst

app = FastAPI(
    title="Cynaris CIA SQL Analyst API",
    version="2.0.0",
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

    try:
        responses = await ask_sql_analyst(question)
        return {
            "question": question,
            "responses": responses,
        }
    except Exception:
        # Avoid returning database credentials or internal error details.
        raise HTTPException(
            status_code=500,
            detail="The SQL analyst could not process the question. Check server logs.",
        )
