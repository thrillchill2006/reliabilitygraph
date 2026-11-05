# Gate N — Provisional non-graph comparison

## Status

**PROVISIONAL — blocked by Gate Q.** The benchmark remains pending/review-only,
so these measurements are engineering diagnostics rather than final results.

## Implemented

- R2 bounded iterative retrieval with a maximum of three passes.
- R3 hyperlink expansion restricted to resolved corpus links and a maximum of
  two hops; unresolved or external links are not followed.
- R4 bounded long-context assembly with explicit token accounting.
- Shared deterministic passage output, zero estimated provider cost, and the
  existing benchmark evidence IDs across comparison modes.

## Verification

```text
uv run python scripts/build_index.py
uv run python scripts/evaluate_retrieval.py
uv run pytest
uv run ruff check .
uv run pyright
```

Observed results are recorded in `docs/STATUS.md`. R4 had the highest
provisional recall@5 (0.5858), while R3 matched the hybrid baseline (0.4188);
all estimated costs were $0.00. Results remain provisional until the benchmark
is reviewed and frozen.

## Gate decision

**BLOCKED / PROVISIONAL** — the strongest non-graph comparator cannot be
declared against a frozen development split while Gate Q remains open.
