"""Protected read-only FastAPI application for the local retrieval baseline."""

# FastAPI registers nested handlers through decorators that Pyright cannot inspect.
# pyright: reportUnusedFunction=false

from __future__ import annotations

import os
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Final

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from reliabilitygraph.retrieval import Answer, SearchIndex, answer_query

MAX_QUERY_CHARS: Final = 1000
MAX_RESULTS: Final = 10
RATE_LIMIT: Final = 30
RATE_WINDOW_SECONDS: Final = 60.0
INDEX_PATH = Path(
    os.environ.get("RELIABILITYGRAPH_INDEX", "artifacts/reliabilitygraph.sqlite")
)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=MAX_QUERY_CHARS)
    mode: str = Field(default="hybrid", pattern="^(lexical|vector|hybrid)$")
    limit: int = Field(default=5, ge=1, le=MAX_RESULTS)


class CitationResponse(BaseModel):
    passage_id: str
    source_key: str
    source_url: str
    section_path: str
    quote: str


class AskResponse(BaseModel):
    answer: str
    citations: list[CitationResponse]
    trace_id: str
    retrieval_mode: str
    latency_ms: float
    estimated_cost_usd: float


def _kill_switch_enabled() -> bool:
    return os.environ.get("RELIABILITYGRAPH_KILL_SWITCH", "").lower() in {
        "1",
        "true",
        "yes",
    }


def create_app(index: SearchIndex | None = None) -> FastAPI:
    app = FastAPI(
        title="ReliabilityGraph",
        version="0.1.0",
        docs_url="/docs",
        redoc_url=None,
    )
    search_index = index
    request_times: dict[str, deque[float]] = defaultdict(deque)
    traces: dict[str, dict[str, object]] = {}

    def get_index() -> SearchIndex:
        nonlocal search_index
        if search_index is None:
            if not INDEX_PATH.exists():
                raise HTTPException(
                    status_code=503,
                    detail="local search index is unavailable",
                )
            search_index = SearchIndex(INDEX_PATH)
        return search_index

    @app.get("/health")
    def health() -> dict[str, str | bool]:
        return {
            "status": "disabled" if _kill_switch_enabled() else "ok",
            "index": str(INDEX_PATH),
            "kill_switch": _kill_switch_enabled(),
        }

    @app.post("/ask", response_model=AskResponse)
    def ask(payload: AskRequest, request: Request) -> AskResponse:
        if _kill_switch_enabled():
            raise HTTPException(status_code=503, detail="service disabled")
        client = request.client.host if request.client else "unknown"
        now = time.monotonic()
        recent = request_times[client]
        while recent and now - recent[0] > RATE_WINDOW_SECONDS:
            recent.popleft()
        if len(recent) >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="rate limit exceeded")
        recent.append(now)
        answer = answer_query(
            get_index(),
            payload.question,
            mode=payload.mode,
            limit=payload.limit,
        )
        traces[answer.trace_id] = {
            "trace_id": answer.trace_id,
            "retrieval_mode": answer.retrieval_mode,
            "citation_ids": [item.passage_id for item in answer.citations],
            "estimated_cost_usd": answer.estimated_cost_usd,
        }
        return _response(answer)

    @app.get("/trace/{trace_id}")
    def trace(trace_id: str) -> dict[str, object]:
        if trace_id not in traces:
            raise HTTPException(status_code=404, detail="trace not found")
        return traces[trace_id]

    @app.get("/", response_class=HTMLResponse)
    def ui() -> str:
        return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>ReliabilityGraph</title></head>
<body><main><h1>ReliabilityGraph</h1>
<p>Evidence-grounded incident search over the local, attributed snapshot.</p>
<form id="ask"><label>Question <input id="question" maxlength="1000" required></label>
<button>Ask</button></form><pre id="result"></pre>
<script>
document.querySelector("#ask").addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = document.querySelector("#question").value;
  const response = await fetch("/ask", {method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({question})});
  document.querySelector("#result").textContent =
    JSON.stringify(await response.json(), null, 2);
});
</script></main></body></html>"""

    return app


def _response(answer: Answer) -> AskResponse:
    return AskResponse(
        answer=answer.answer,
        citations=[
            CitationResponse(
                passage_id=item.passage_id,
                source_key=item.source_key,
                source_url=item.source_url,
                section_path=item.section_path,
                quote=item.quote,
            )
            for item in answer.citations
        ],
        trace_id=answer.trace_id,
        retrieval_mode=answer.retrieval_mode,
        latency_ms=answer.latency_ms,
        estimated_cost_usd=answer.estimated_cost_usd,
    )


app = create_app()
