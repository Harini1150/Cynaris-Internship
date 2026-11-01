import io
import os
import uuid
from typing import Any

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM

app = FastAPI(title="CIA Data Analyst Mode", version="1.0.0")
app.mount("/static", StaticFiles(directory="Week 7/static"), name="static")

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_ROWS = 100_000
MAX_COLUMNS = 200
sessions: dict[str, pd.DataFrame] = {}


class QuestionRequest(BaseModel):
    session_id: str
    question: str


@app.get("/")
def home():
    return FileResponse("Week 7/static/index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "CIA Data Analyst Mode"}


@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Please upload a CSV file.")

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "CSV must be 10 MB or smaller.")

    if not content:
        raise HTTPException(400, "The uploaded CSV is empty.")

    try:
        data = pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise HTTPException(400, f"Could not parse CSV: {exc}") from exc

    if data.empty:
        raise HTTPException(400, "The CSV has no data rows.")
    if len(data) > MAX_ROWS:
        raise HTTPException(400, f"Maximum supported rows: {MAX_ROWS}.")
    if len(data.columns) > MAX_COLUMNS:
        raise HTTPException(400, f"Maximum supported columns: {MAX_COLUMNS}.")
    if not data.columns.is_unique:
        raise HTTPException(400, "CSV column names must be unique.")
    if any(not str(col).strip() for col in data.columns):
        raise HTTPException(400, "CSV column names cannot be blank.")

    # Keep uploaded data in server memory; do not save arbitrary user files.
    session_id = str(uuid.uuid4())
    sessions[session_id] = data

    return {
        "session_id": session_id,
        "filename": file.filename,
        "rows": int(len(data)),
        "columns": [str(col) for col in data.columns],
        "preview": data.head(10).where(pd.notna(data.head(10)), None).to_dict("records"),
        "missing_values": {
            str(col): int(count)
            for col, count in data.isna().sum().items()
        },
        "numeric_columns": [
            str(col) for col in data.select_dtypes(include="number").columns
        ],
    }


def chart_for_data(data: pd.DataFrame) -> dict[str, Any] | None:
    """Build safe, JSON-serializable chart data from the uploaded dataset."""
    numeric = list(data.select_dtypes(include="number").columns)
    if not numeric or data.empty:
        return None

    value_col = numeric[0]
    category_cols = [
        col for col in data.columns
        if col != value_col and (
            pd.api.types.is_object_dtype(data[col])
            or pd.api.types.is_string_dtype(data[col])
            or isinstance(data[col].dtype, pd.CategoricalDtype)
        )
    ]

    if category_cols:
        category_col = category_cols[0]
        grouped = (
            data.groupby(category_col, dropna=False)[value_col]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        labels = [
            "(missing)" if pd.isna(label) else str(label)
            for label in grouped.index
        ]
        values = [float(value) for value in grouped.values]
        title = f"{value_col} by {category_col}"
    else:
        labels = [str(value_col)]
        values = [float(data[value_col].sum())]
        title = f"Total {value_col}"

    return {
        "type": "bar",
        "title": title,
        "labels": labels,
        "datasets": [{"label": value_col, "data": values}],
    }



def answer_with_pandas(data: pd.DataFrame, question: str):
    """Answer common questions using direct pandas calculations."""
    q = question.lower().strip()
    columns = {str(col).lower(): col for col in data.columns}

    def find_col(name):
        return columns.get(name.lower())

    amount = find_col("Amount")
    quantity = find_col("Quantity")
    profit = find_col("Profit")
    order_id = find_col("Order ID")
    category = find_col("Category")
    subcategory = find_col("Sub-Category")
    city = find_col("City")
    state = find_col("State")

    def grouped_sales(col):
        if col is None or amount is None:
            return []
        grouped = data.groupby(col, dropna=False)[amount].sum()
        grouped = grouped.sort_values(ascending=False)
        return [
            {
                str(col): "(missing)" if pd.isna(key) else str(key),
                "Total_Sales": float(value),
            }
            for key, value in grouped.items()
        ]

    if quantity is not None and "quantity" in q and any(
        word in q for word in ("total", "sum", "sold")
    ):
        return int(data[quantity].sum())

    if profit is not None and "profit" in q and any(
        word in q for word in ("total", "sum", "overall")
    ):
        return float(data[profit].sum())

    if amount is not None and any(
        phrase in q for phrase in (
            "total sales", "total sale", "total amount",
            "sum of sales", "overall sales", "sales amount"
        )
    ) and not any(word in q for word in (
        "category", "city", "state", "sub-category", "subcategory"
    )):
        return float(data[amount].sum())

    
    # Check sub-category before category because "sub-category"
    # also contains the word "category".
    if subcategory is not None and amount is not None and any(
        word in q for word in ("sub-category", "subcategory", "sub category")
    ) and any(word in q for word in ("highest", "most", "top", "maximum", "best")):
        results = grouped_sales(subcategory)
        return results[0] if results else None

    if category is not None and amount is not None and "category" in q:
        if any(word in q for word in ("each", "every", "breakdown", "by category")):
            return grouped_sales(category)
        if any(word in q for word in ("highest", "most", "top", "maximum", "best")):
            results = grouped_sales(category)
            return results[0] if results else None

   
        return float(data[amount].mean())

    if any(word in q for word in ("how many", "count", "number of")) and "order" in q:
        return int(data[order_id].nunique()) if order_id is not None else int(len(data))

    return None


@app.post("/api/ask")
def ask_question(request: QuestionRequest):
    data = sessions.get(request.session_id)
    if data is None:
        raise HTTPException(404, "Upload a CSV first; session was not found.")

    question = request.question.strip()
    if not question:
        raise HTTPException(400, "Enter a question.")
    if len(question) > 1000:
        raise HTTPException(400, "Question must be 1,000 characters or fewer.")

    try:
        answer = answer_with_pandas(data, question)

        # Use PandasAI only when a direct calculation does not match.
        if answer is None:
            llm = LocalLLM(
                api_base="http://localhost:11434/v1",
                model="qwen2.5:3b",
                api_key="ollama",
            )
            ai_df = SmartDataframe(
                data.copy(),
                config={"llm": llm, "verbose": False},
            )
            answer = ai_df.chat(question)

        if isinstance(answer, pd.DataFrame):
            preview = answer.head(20)
            answer = preview.astype(object).where(
                pd.notna(preview), None
            ).to_dict("records")
        elif hasattr(answer, "tolist"):
            answer = answer.tolist()
        elif not isinstance(answer, (str, int, float, bool, list, dict, type(None))):
            answer = str(answer)

        return {
            "question": question,
            "answer": answer,
            "chart": chart_for_data(data),
            "note": "Chart summarizes the uploaded dataset; it may not represent the specific question.",
        }
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Analysis error for question {question!r}: {exc}")
        raise HTTPException(
            502,
            "Analysis failed. Check that Ollama is running with qwen2.5:3b, "
            "then review the server terminal for details.",
        ) from exc
