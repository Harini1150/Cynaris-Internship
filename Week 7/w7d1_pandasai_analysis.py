import logging
import json
from pathlib import Path

import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM


# -------------------- Configuration --------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "merged_orders_cleaned.csv"
RESULTS_FILE = BASE_DIR / "w7d1_query_results.json"
COMPARISON_FILE = BASE_DIR / "w7d1_comparison_report.md"
ERROR_LOG_FILE = BASE_DIR / "w7d1_errors.log"

logging.basicConfig(
    filename=ERROR_LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# -------------------- Load dataset --------------------

def load_data():
    """Load and validate the Indian retail dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    data = pd.read_csv(DATA_FILE)

    required_columns = {
        "Amount", "Profit", "Quantity", "Category",
        "Sub-Category", "State", "City", "CustomerName"
    }

    missing = required_columns - set(data.columns)
    if missing:
        raise ValueError(f"Required columns missing: {sorted(missing)}")

    return data


# -------------------- Manual Pandas answers --------------------

def manual_answers(data):
    """Calculate reference answers independently with Pandas."""
    return {
        "Total sales": round(float(data["Amount"].sum()), 2),
        "Total profit": round(float(data["Profit"].sum()), 2),
        "Total quantity sold": int(data["Quantity"].sum()),
    }


# -------------------- PandasAI setup --------------------

def create_ai_dataframe(data):
    """Connect PandasAI to the local Ollama Qwen model."""
    llm = LocalLLM(
        api_base="http://localhost:11434/v1",
        model="qwen2.5:3b",
        api_key="ollama",
    )

    return SmartDataframe(
        data.copy(),
        config={"llm": llm, "verbose": False},
    )


# -------------------- Run natural-language questions --------------------


def run_queries(ai_df):
    questions = [
        "Calculate the sum of Amount and return only one number.",
        "Calculate the sum of Profit and return only one number.",
        "Calculate the sum of Quantity and return only one number.",
        "Group by Category, sum Amount, sort descending, and return only the category and total sales columns.",
        "Group by Category, sum Profit, sort ascending, and return only the category and total profit columns.",
        "Group by City, sum Amount, sort descending, and return only the top 5 cities and their total sales. Do not return raw rows.",
        "Group by State, sum Amount, sort descending, and return only the top 5 states and their total sales. Do not return raw rows.",
        "Group by Sub-Category, sum Profit, sort descending, and return only the top 5 sub-categories and their total profit.",
        "Count unique values in CustomerName and return only one number.",
        "Count rows where Profit is less than zero and return only one number.",
    ]

    # Preserve the results already obtained in the previous run.
    known = {
        questions[0]: {
            "question": questions[0], "status": "success",
            "answer": 431502.0,
        },
        questions[1]: {
            "question": questions[1], "status": "success",
            "answer": 23955.0,
        },
        questions[2]: {
            "question": questions[2], "status": "success",
            "answer": 5615,
        },
        questions[3]: {
            "question": questions[3], "status": "failed",
            "error": "PandasAI returned NoResultFoundError: No result returned.",
        },
        questions[4]: {
            "question": questions[4], "status": "success",
            "answer": {
                "Furniture": 2298.0,
                "Electronics": 10494.0,
                "Clothing": 11163.0,
            },
        },
        questions[5]: {
            "question": questions[5], "status": "success",
            "answer": [
                {"City": "Indore", "Total Sales": 79069.0},
                {"City": "Mumbai", "Total Sales": 61867.0},
                {"City": "Pune", "Total Sales": 33481.0},
                {"City": "Delhi", "Total Sales": 25019.0},
                {"City": "Bhopal", "Total Sales": 23583.0},
            ],
        },
    }

    # Restore any additional results saved during an earlier attempt.
    if RESULTS_FILE.exists():
        try:
            saved = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
            for item in saved:
                if item.get("question") in questions:
                    known[item["question"]] = item
        except (json.JSONDecodeError, OSError) as exc:
            logging.error("Could not restore previous results: %s", exc)

    def save_progress():
        ordered = [known[q] for q in questions if q in known]
        RESULTS_FILE.write_text(
            json.dumps(ordered, indent=2, default=str),
            encoding="utf-8",
        )

    save_progress()
    print("Previous results restored. Running any remaining questions.")

    for number, question in enumerate(questions, start=1):
        if question in known:
            print(f"\n[{number}/10] Already saved; skipping.")
            continue

        print(f"\n[{number}/10] {question}")

        try:
            answer = ai_df.chat(question)

            # PandasAI can return an error message instead of raising an exception.
            if isinstance(answer, str) and any(
                phrase in answer.lower()
                for phrase in [
                    "unfortunately, i was not able to answer",
                    "no result returned",
                    "i was unable to answer",
                ]
            ):
                record = {
                    "question": question,
                    "status": "failed",
                    "error": answer[:2000],
                }
                logging.error("PandasAI returned an error for: %s", question)

            else:
                if isinstance(answer, pd.DataFrame):
                    answer = {
                        "type": "table",
                        "rows_returned": int(len(answer)),
                        "columns": answer.columns.tolist(),
                        "preview_first_10_rows": answer.head(10).to_dict(
                            orient="records"
                        ),
                    }
                elif isinstance(answer, pd.Series):
                    answer = answer.head(10).to_dict()
                elif hasattr(answer, "item"):
                    answer = answer.item()

                if isinstance(answer, str) and len(answer) > 2000:
                    answer = answer[:2000] + "... [truncated]"

                record = {
                    "question": question,
                    "status": "success",
                    "answer": answer,
                }

        except Exception as exc:
            logging.exception("Query failed: %s", question)
            record = {
                "question": question,
                "status": "failed",
                "error": str(exc),
            }

        known[question] = record
        save_progress()  # Save immediately after every query.

        print("Status:", record["status"])
        print("Result:", str(record.get("answer", record.get("error", "")))[:1200])

    return [known[q] for q in questions if q in known]


# -------------------- Compare AI and manual answers --------------------

def build_comparison(results, reference):
    """Write a report comparing AI answers with manual calculations."""
    comparison_questions = {
    "Total sales": "Calculate the sum of Amount and return only one number.",
    "Total profit": "Calculate the sum of Profit and return only one number.",
    "Total quantity sold": "Calculate the sum of Quantity and return only one number.",
}

    lines = [
        "# W7D1 — PandasAI vs Manual Pandas Comparison",
        "",
        "Dataset: `merged_orders_cleaned.csv`",
        "",
        "Manual values were calculated independently using Pandas.",
        "AI answers are recorded as returned and must be checked for equivalent meaning and units.",
        "",
        "| Metric | Manual Pandas | PandasAI answer | Status |",
        "|---|---:|---|---|",
    ]

    for metric, question in comparison_questions.items():
        match = next(
            (item for item in results if item["question"] == question),
            None,
        )

        if match and match["status"] == "success":
            ai_answer = str(match["answer"]).replace("|", "\\|")
            status = "Review required"
        else:
            ai_answer = "Query failed"
            status = "Not comparable"

        lines.append(
            f"| {metric} | {reference[metric]} | {ai_answer} | {status} |"
        )

    lines.extend([
        "",
        "## Validation notes",
        "- A matching-looking number is not proof of correctness.",
        "- Check that each AI answer uses the correct column, aggregation, and units.",
        "- Mark a result as matching only after verifying its meaning against the manual calculation.",
        "- Review failed queries in `w7d1_errors.log`.",
        "",
    ])

    COMPARISON_FILE.write_text("\n".join(lines), encoding="utf-8")


# -------------------- Main program --------------------

def main():
    print("=" * 60)
    print("W7D1: PandasAI Natural-Language Retail Analysis")
    print("=" * 60)

    data = load_data()
    print(f"Dataset loaded successfully: {data.shape[0]} rows, {data.shape[1]} columns")

    reference = manual_answers(data)
    print("\nManual Pandas reference answers:")
    for metric, value in reference.items():
        print(f"- {metric}: {value}")

    ai_df = create_ai_dataframe(data)
    results = run_queries(ai_df)

    RESULTS_FILE.write_text(
        json.dumps(results, indent=2, default=str),
        encoding="utf-8",
    )

    build_comparison(results, reference)

    succeeded = sum(item["status"] == "success" for item in results)
    failed = len(results) - succeeded

    print("\n" + "=" * 60)
    print(f"Finished: {succeeded} succeeded, {failed} failed")
    print(f"Query results: {RESULTS_FILE}")
    print(f"Comparison report: {COMPARISON_FILE}")
    print(f"Error log: {ERROR_LOG_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("W7D1 script failed")
        print("The script stopped because of an error. Check w7d1_errors.log.")
        raise
