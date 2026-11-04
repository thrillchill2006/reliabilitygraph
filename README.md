# ReliabilityGraph

ReliabilityGraph is a retrospective, citation-grounded research application for
examining historical software incidents. It is intended to help engineers
connect documented symptoms, mechanisms, dependencies, responses, and
corrective actions without presenting unsupported operational advice.

The project is currently in **Phase 0: Foundation and Guardrails**. The initial
Wikimedia corpus, graph hypothesis, retrieval quality, provider entitlements,
and deployment costs are not yet validated.

## Development setup

The project uses Python 3.12 and `uv`. Install `uv`, then run:

```powershell
uv sync --extra dev
uv run ruff check .
uv run pyright
uv run pytest
uv run python scripts/check_secrets.py
```

These commands cover linting, type checks, tests, and a lightweight secret
scan. No paid model provider or API key is required for Phase 0.

## Current status

See [docs/STATUS.md](docs/STATUS.md) for the active phase, gate, validation
results, decisions, and next task. The authoritative roadmap is
[docs/PLAN.md](docs/PLAN.md); corpus selection and source boundaries are
defined in [docs/CORPUS/CORPUS_SPECIFICATION.md](docs/CORPUS/CORPUS_SPECIFICATION.md).

## Boundaries

This project does not access live systems, execute repairs, certify
infrastructure, ingest private incident archives, or claim that a graph
database is required. Raw source content is not committed until acquisition,
rights, and reproducibility checks are completed.
