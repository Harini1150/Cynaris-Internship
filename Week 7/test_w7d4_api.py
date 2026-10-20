import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi.testclient import TestClient
import cia_sql_analyst_api as api

client = TestClient(api.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_question_too_short():
    response = client.post(
        "/cia/sql-analyst",
        json={"question": "hi"},
    )
    assert response.status_code == 422


def test_missing_question():
    response = client.post(
        "/cia/sql-analyst",
        json={},
    )
    assert response.status_code == 422


def test_blank_question():
    # Whitespace passes the minimum-length check but must be rejected
    # before invoking the AI agent.
    response = client.post(
        "/cia/sql-analyst",
        json={"question": "   "},
    )
    assert response.status_code == 422


if __name__ == "__main__":
    tests = [
        test_health,
        test_question_too_short,
        test_missing_question,
        test_blank_question,
    ]
    for test in tests:
        test()
        print("PASS:", test.__name__)
    print(f"{len(tests)} API tests passed")
