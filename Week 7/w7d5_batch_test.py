import json
from pathlib import Path
import requests

BASE_URL = "http://127.0.0.1:8002"
CSV_FILE = Path(__file__).resolve().parent / "merged_orders_cleaned.csv"
REPORT_FILE = Path(__file__).resolve().parent / "w7d5_batch_results.json"

questions = [
    "What is the total sales amount in the dataset?",
    "What is the total profit in the dataset?",
    "What is the total quantity sold?",
    "Which category has the highest total sales?",
    "Which city has the highest total sales?",
    "Which state has the highest total sales?",
    "What is the average order amount?",
    "Which sub-category has the highest total sales?",
    "How many orders are in the dataset?",
    "What is the total sales amount for each category?"
]

def main():
    if not CSV_FILE.exists():
        print(f"CSV not found: {CSV_FILE}")
        return

    try:
        health = requests.get(f"{BASE_URL}/health", timeout=10)
        health.raise_for_status()
        print("CIA server is reachable.")
    except requests.RequestException as exc:
        print(f"Cannot reach CIA server: {exc}")
        return

    with CSV_FILE.open("rb") as csv_file:
        upload = requests.post(
            f"{BASE_URL}/api/upload",
            files={"file": (CSV_FILE.name, csv_file, "text/csv")},
            timeout=60
        )
    upload.raise_for_status()
    session_id = upload.json()["session_id"]
    print(f"Uploaded {CSV_FILE.name} successfully.")

    results = []
    for number, question in enumerate(questions, start=1):
        print(f"\n[{number}/10] {question}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/ask",
                json={"session_id": session_id, "question": question},
                timeout=180
            )
            try:
                body = response.json()
            except ValueError:
                body = {"error": response.text}

            result = {
                "number": number,
                "question": question,
                "http_status": response.status_code,
                "response": body
            }
            if response.ok:
                print("Answer:", body.get("answer", body))
            else:
                print("ERROR:", body)
        except requests.RequestException as exc:
            result = {
                "number": number,
                "question": question,
                "error": str(exc)
            }
            print("ERROR:", exc)

        results.append(result)

    REPORT_FILE.write_text(
        json.dumps(results, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    successful = sum(
        1 for item in results
        if item.get("http_status", 0) == 200
    )
    print(f"\nFinished: {successful}/10 requests returned HTTP 200.")
    print(f"Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    main()
