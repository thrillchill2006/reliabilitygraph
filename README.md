# ReliabilityGraph

ReliabilityGraph is a retrospective, citation-grounded research application for
examining historical software incidents. It is intended to help engineers
connect documented symptoms, mechanisms, dependencies, responses, and
corrective actions without presenting unsupported operational advice.

The project has completed the local P0/P1/P2 infrastructure and now contains a
provisional P3 retrieval baseline and P4 local demonstration. The benchmark is
still pending formal human-signoff in Gate Q, so P3 metrics and P4 status are
not final gate results.

## Development setup

The project uses Python 3.12 and `uv`. Install `uv`, then run:

```powershell
uv sync --extra app
uv run ruff check .
uv run pyright
uv run pytest
uv run python scripts/check_secrets.py
uv run python scripts/build_index.py
uv run python scripts/evaluate_retrieval.py
```

These commands cover linting, type checks, tests, local indexing, provisional
retrieval metrics, and a lightweight secret scan. No paid model provider or API
key is required.

Run the local demonstration after building the index:

```powershell
uv run uvicorn reliabilitygraph.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/` to use the evidence-first UI. The `/health`,
`/ask`, and `/trace/{id}` endpoints are read-only and use the local snapshot.

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
