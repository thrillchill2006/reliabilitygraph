# Gate Q — Evidence model and benchmark

## Implemented P2 controls

- Typed `EvidenceSpan`, `ClaimRecord`, `RelationRecord`, `GoldQuestion`, and
  `RunArtifact` records are implemented in `src/reliabilitygraph/evidence.py`.
- Validators check source/evidence references, duplicate IDs, split validity,
  incident-family leakage, reviewed-answer requirements, and unacceptable
  inference constraints.
- Deterministic oracle, empty, and seeded-random evaluation stubs are
  implemented in the same module.
- `docs/annotation-guide.md` defines evidence, attribution, time, uncertainty,
  action-state, false-analogy, and abstention rules.
- `docs/decision-criteria.md` records evaluation priorities before retrieval.

## Current benchmark artifact

`data/benchmark/questions.json` contains 40 source-grounded candidate questions:

- 17 multi-source dependency candidates after applying all 40 proposed
  corrections;
- 24 records contain evidence from more than one source, including negative,
  temporal, and abstention controls that are not multi-source dependencies;
- negative/missing-evidence and false-analogy candidates;
- single-document, comparison, and time-qualified controls.

All records are explicitly `review` split and `annotation-pending`. The
generated review worksheet at
`data/benchmark/review_annotations.json` contains proposed extractive answers,
exact passage IDs, canonical URLs, section paths, quoted text, and reviewer
notes. It contains no approved reference answers or human decisions. These are
review work items, not a frozen gold benchmark.

## Verification

Observed locally:

```text
uv run pytest
  14 passed
uv run ruff check .
  All checks passed
uv run pyright
  0 errors, 0 warnings, 0 informations
uv run python -m reliabilitygraph.evaluation validate --questions data\benchmark\questions.json
  validated 40 question records
uv run python -m reliabilitygraph.evaluation freeze --questions data\benchmark\questions.json
  cannot freeze benchmark: benchmark contains pending human review
```

The freeze command intentionally refuses pending or review-only records. Gate Q
cannot pass until the candidate questions are manually annotated, reviewed,
anchored to P1 passages, partitioned by incident family, and the requirement
for at least 12–15 genuinely multi-source questions is confirmed. The current
17 multi-source dependency candidates are still proposals; their minimum
evidence sets and
acceptable versus unsupported inferences still require human review.

## Gate decision

**BLOCKED — human annotation and review pending.** No retrieval or benchmark
performance claim is made.
