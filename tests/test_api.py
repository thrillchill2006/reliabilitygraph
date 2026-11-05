"""API smoke tests."""

# TestClient's third-party stubs are incomplete under strict Pyright.
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false

from pathlib import Path

from fastapi.testclient import TestClient

from reliabilitygraph.api import create_app
from reliabilitygraph.retrieval import SearchIndex


def test_api_health_ask_and_trace(tmp_path: Path) -> None:
    index = SearchIndex.build(tmp_path / "index.sqlite")
    client = TestClient(create_app(index))

    assert client.get("/health").json()["status"] == "ok"
    response = client.post("/ask", json={"question": "What caused the outage?"})
    assert response.status_code == 200
    body = response.json()
    assert body["citations"]
    assert client.get(f"/trace/{body['trace_id']}").status_code == 200
    index.close()


def test_api_rejects_empty_question(tmp_path: Path) -> None:
    index = SearchIndex.build(tmp_path / "index.sqlite")
    client = TestClient(create_app(index))
    assert client.post("/ask", json={"question": ""}).status_code == 422
    index.close()
