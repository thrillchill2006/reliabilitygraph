"""Run provisional retrieval metrics against pending P2 evidence sets."""

from __future__ import annotations

import json
import statistics
import time
from pathlib import Path

from reliabilitygraph.retrieval import (
    SearchIndex,
    hyperlink_expand,
    iterative_search,
    long_context,
    relation_guided_search,
)


def main() -> int:
    index = SearchIndex(Path("artifacts/reliabilitygraph.sqlite"))
    questions = json.loads(
        Path("data/benchmark/questions.json").read_text(encoding="utf-8")
    )["questions"]
    metrics: dict[str, dict[str, float]] = {}
    metrics["B-1-closed-book"] = {
        "questions": float(len(questions)),
        "recall_at_5": 0.0,
        "mrr_at_5": 0.0,
        "median_latency_ms": 0.0,
        "p95_latency_ms": 0.0,
        "estimated_cost_usd": 0.0,
    }
    for mode in ("lexical", "vector", "hybrid"):
        recalls: list[float] = []
        reciprocal_ranks: list[float] = []
        latencies: list[float] = []
        for question in questions:
            started = time.perf_counter()
            results = index.search(question["question"], mode=mode, limit=5)
            latencies.append((time.perf_counter() - started) * 1000)
            expected = set(question["evidence_span_ids"])
            actual = [result.passage_id for result in results]
            recalls.append(
                len(expected & set(actual)) / len(expected)
                if expected
                else 1.0
            )
            ranks = [actual.index(item) + 1 for item in expected if item in actual]
            reciprocal_ranks.append(1.0 / min(ranks) if ranks else 0.0)
        metrics[mode] = {
            "questions": float(len(questions)),
            "recall_at_5": statistics.fmean(recalls),
            "mrr_at_5": statistics.fmean(reciprocal_ranks),
            "median_latency_ms": statistics.median(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95) - 1],
            "estimated_cost_usd": 0.0,
        }
    for name, runner in (
        ("R2-iterative", iterative_search),
        ("R3-hyperlink", hyperlink_expand),
        ("R4-long-context", long_context),
        ("R5-sql-evidence", lambda idx, query: idx.relation_evidence(query)),
        ("R6a-relation-guided", relation_guided_search),
    ):
        recalls: list[float] = []
        latencies: list[float] = []
        for question in questions:
            started = time.perf_counter()
            result = runner(index, question["question"])
            latencies.append((time.perf_counter() - started) * 1000)
            expected = set(question["evidence_span_ids"])
            recalls.append(
                len(expected & {item.passage_id for item in result})
                / len(expected)
                if expected
                else 1.0
            )
        metrics[name] = {
            "questions": float(len(questions)),
            "recall_at_5": statistics.fmean(recalls),
            "mrr_at_5": 0.0,
            "median_latency_ms": statistics.median(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95) - 1],
            "estimated_cost_usd": 0.0,
        }
    print(json.dumps({"provisional": True, "metrics": metrics}, indent=2))
    index.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
