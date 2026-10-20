import json
import urllib.request
from pathlib import Path

questions = [
    "What is the total sales value?",
    "How many customers are there in each city?",
    "What are the total sales for each category?",
    "What are the top products by sales?",
    "What are the total sales for each city?",
    "What is the total quantity sold for each product?",
    "How many sales records are there?",
    "What is the average product price?",
    "What are the total sales for each month?",
    "Which city has the highest total sales?",
]

results = []

for number, question in enumerate(questions, start=1):
    print(f"\n{'=' * 60}")
    print(f"QUERY {number}/10: {question}")

    payload = json.dumps({"question": question}).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:8001/cia/sql-analyst",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            body = json.loads(response.read().decode("utf-8"))
            item = {
                "number": number,
                "question": question,
                "status": response.status,
                "response": body,
            }
            results.append(item)
            print(f"HTTP {response.status}")
            for event in body.get("responses", []):
                component = event.get("rich_component") or {}
                if component.get("type") == "status_card":
                    if component.get("status") == "success":
                        print("SQL:", component.get("metadata", {}).get("sql", ""))
                if component.get("type") == "dataframe":
                    print("RESULTS:", json.dumps(
                        component.get("rows", []), ensure_ascii=False
                    ))
                if component.get("type") == "text":
                    content = component.get("content")
                    if content:
                        print("ANSWER:", content)
    except Exception as exc:
        results.append({
            "number": number,
            "question": question,
            "error": str(exc),
        })
        print("FAILED:", exc)

output = Path("Week 7") / "w7d4_batch_results.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

passed = sum(1 for item in results if item.get("status") == 200)
print(f"\nFinished: {passed}/10 returned HTTP 200.")
print(f"Saved full responses to: {output}")
