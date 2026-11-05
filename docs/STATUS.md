# ReliabilityGraph status

- **Active phase:** P6 — Verified relationship upper-bound and SQL control
- **Active gate:** G (provisional REWORK; Gate Q remains incomplete)
- **Active task:** P6 technical comparison and relation annotation evidence
- **Last validation:** 2026-11-05 P3/P4 local verification passed
- **Last green commit/tag:** None
- **Provider mode:** Deterministic mock/record-replay only; no paid provider calls
- **Corpus status:** 19-document local snapshot acquired with provenance, licensing, and current-page-only metadata
- **Next task:** Complete document-level relation annotation and agreement evidence
- **Blockers:** Gate Q remains blocked; P6 has only one metadata-verified relation and no manual annotation/agreement evidence

## Local P0 verification

The following commands passed locally from the repository directory:

```text
uv sync --frozen
uv run ruff check .
uv run pyright
uv run pytest       # 14 passed
uv run python scripts/check_secrets.py
```

## P1/P2 validation

The P1 snapshot and P2 infrastructure also pass locally:

```text
uv run python scripts/validate_corpus.py data\corpus
  P1 snapshot valid: 19 sources, 218 sections, 370 passages, 98 links
uv run pytest
  14 passed
uv run python -m reliabilitygraph.evaluation validate --questions data\benchmark\questions.json
  validated 40 question records
uv run python -m reliabilitygraph.evaluation freeze --questions data\benchmark\questions.json
  cannot freeze benchmark: benchmark contains pending human review
```

GitHub Actions is configured in `.github/workflows/ci.yml` but has not been
observed running. No Copilot Student or independent provider credentials were
copied into the repository; entitlement status remains to be checked in the
actual account. P1 Gate S passed for the expanded local snapshot. P2 Gate Q is
blocked pending manual annotation and review. The corrected benchmark contains
17 multi-source dependency candidates; 24 records contain evidence from more
than one source, including controls that are not multi-source dependencies.
The pending review worksheet is
`data/benchmark/review_annotations.json`; benchmark freeze is intentionally
not attempted successfully while records remain pending.

The user confirmed that human review was completed in conversation, but no
repository artifact records approved decisions or non-null reference answers.
The sign-off sheet still says `READY FOR HUMAN REVIEW; NOT APPROVED`, so this
confirmation does not close Gate Q. The readiness diagnostic is:

```text
uv run python scripts/check_benchmark_readiness.py
```

Its expected non-zero result lists the missing approval fields. This is the
documented provisional-development exception: engineering may continue, but
provisional metrics are never final and no blocked gate is changed to PASS.

## P3/P4 execution-order deviation

At the user's direction, P3 and P4 were implemented before formal Gate Q
closure. The benchmark remains provisional and unfrozen; no final benchmark
claim or formal Gate B/D0 pass is made.

P3 provides a deterministic SQLite/FTS5 index, hashed-vector retrieval,
hybrid scoring, metadata filters, extractive grounded answers, strict citation
validation, and provisional metrics in `docs/gates/B.md`. P4 provides the
read-only FastAPI app, minimal evidence UI, bounded requests, rate limiting,
kill switch, and Dockerfile in `docs/gates/D0.md`. No paid provider or hosting
resource was used.

## P5 provisional verification

Implemented R2 bounded iterative retrieval, R3 resolved-link expansion, and
R4 bounded long-context assembly. R3 followed zero links because the local
corpus marks its links unresolved; no arbitrary or external link was opened.
R4 uses a 1,200-token bound and reports selected passage context only.

Observed commands and results:

```text
uv run pytest
20 passed, 1 warning
uv run ruff check .
All checks passed
uv run pyright
0 errors, 0 warnings, 0 informations
uv run python scripts/build_index.py
370 passages; corpus hash 7771d6b652a0d1cc869f58b2b0367e25611f5c5e96f65a531f38f1f5a4060545
uv run python scripts/evaluate_retrieval.py
exit 0; provisional R2 recall@5 0.3704, R3 0.4188, R4 0.5858; estimated cost $0.00
uv run python scripts/check_benchmark_readiness.py
exit 1; 120 blocking fields across Q001-Q040 (expected while review remains pending)
```

Gate N remains **BLOCKED / PROVISIONAL** because Gate Q is not closed and the
benchmark is not frozen. P6 is recorded separately below.

## P6 verification

R3 local-link diagnosis found one exact canonical-URL match among 98 corpus
links: the Incident Review Ritual page references the included Incident Status
page. The remaining links are unresolved or link-only and were not promoted.
The verified relation record is in
`data/relations/verified_relations.json`; the annotation log records 19 pilot
sources pending manual document-level annotation.

Observed commands and results:

```text
uv run pytest tests/test_relations.py tests/test_retrieval.py
4 passed
uv run ruff check .
All checks passed
uv run pyright
0 errors, 0 warnings, 0 informations
uv run python scripts/validate_relations.py
validated 1 verified relation(s)
uv run python scripts/build_index.py
370 passages; corpus hash 7771d6b652a0d1cc869f58b2b0367e25611f5c5e96f65a531f38f1f5a4060545
uv run python scripts/evaluate_retrieval.py
exit 0; R5 recall@5 0.0000; R6a recall@5 0.4188; estimated costs $0.00
```

Gate G is **REWORK / PROVISIONAL**. The relation set is too sparse to support
a graph-traversal claim, and no P7 work is authorized.

## Working rules

The roadmap and corpus specification are authoritative. Each task is completed
with targeted evidence before the next task begins. Do not copy credentials,
raw uncertain-rights source content, or unverified benchmark claims into this
repository.
