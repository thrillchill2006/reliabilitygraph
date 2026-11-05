# Gate B — Provisional baseline retrieval

## Status

**PROVISIONAL — formal Gate Q is not closed.** P3 was executed out of order at
the user's direction. The benchmark remains pending/review-only, so these
metrics are engineering diagnostics and not final benchmark results.

## Implemented

- Deterministic SQLite/FTS5 index over 370 passages.
- Exact hashed-vector retrieval and lexical/vector/hybrid modes.
- Metadata filters for source, status, and incident family.
- Extractive grounded answer generation with strict passage-quote validation.
- Reproducible index metadata and provisional evaluation script.

## Observed metrics

Command:

```text
uv run python scripts/build_index.py
uv run python scripts/evaluate_retrieval.py
```

Index:

```text
passage_count: 370
corpus_hash: 7771d6b652a0d1cc869f58b2b0367e25611f5c5e96f65a531f38f1f5a4060545
```

On 40 pending candidate questions, top-5 results:

| Mode | Recall@5 | MRR@5 | Median latency | P95 latency | Estimated cost |
|---|---:|---:|---:|---:|---:|
| B-1 closed-book | 0.0000 | 0.0000 | 0.0 ms | 0.0 ms | $0.00 |
| R0 lexical | 0.4158 | 0.4483 | 16.2 ms | 17.9 ms | $0.00 |
| Dense diagnostic | 0.1596 | 0.1775 | 17.1 ms | 20.4 ms | $0.00 |
| R1 hybrid | 0.4188 | 0.4588 | 17.1 ms | 19.5 ms | $0.00 |

These are provisional because the benchmark has not passed Gate Q.

## Verification

```text
uv run ruff check .
  All checks passed
uv run pyright
  0 errors, 0 warnings, 0 informations
uv run pytest
  19 passed, 1 warning
```

## Gate decision

**BLOCKED / PROVISIONAL** — technical retrieval controls are implemented, but
formal Gate B requires a frozen reviewed benchmark.
