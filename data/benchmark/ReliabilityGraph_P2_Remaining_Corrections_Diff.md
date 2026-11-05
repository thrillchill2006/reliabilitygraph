# P2 benchmark — remaining corrections after Copilot run

**Basis:** comparison of the latest uploaded `questions.json` and `review_annotations.json` with `ReliabilityGraph_P2_Consolidated_Proposed_Corrections.json`, using the uploaded corpus passages/manifest for passage ID validation.

**Status:** proposals only; no human-reviewed gold, approved answers, or frozen test split.

## Summary

- 40/40 question IDs present and correctly paired with annotation records.
- 0/40 current question texts exactly match the proposed revisions.
- 0/40 current proposed answers exactly match the proposed concise answers.
- 4/40 current evidence lists exactly match the proposed sets: Q009, Q018, Q019, Q027.
- 27/40 current question classes match the proposals; 13 still differ.
- 30/40 current question source ID sets match the proposal; 10 still differ.
- All proposed passage IDs resolve in the uploaded 370-passage snapshot. This is **referential validity**, not proof every proposed answer is entailed.
- 22 of the current questions cite multiple document IDs; 24 of the proposed corrections cite multiple distinct documents. Neither count proves genuine minimum-evidence multi-source reasoning.
- All 40 records still have `review_status=pending`, and all remain in the `review` split.

## Per-question delta

| ID | Proposed decision | Fields needing change | Sources in proposed evidence |
|---|---|---|---:|
| Q001 | revise | Question, Answer, Evidence | 3 |
| Q002 | revise | Question, Answer, Class, Evidence, Sources | 1 |
| Q003 | revise | Question, Answer, Class, Evidence | 2 |
| Q004 | revise | Question, Answer, Class, Evidence | 2 |
| Q005 | revise | Question, Answer, Class, Evidence | 2 |
| Q006 | revise | Question, Answer, Class, Evidence | 2 |
| Q007 | revise | Question, Answer, Class, Evidence, Sources | 2 |
| Q008 | replace | Question, Answer, Class, Evidence, Sources | 2 |
| Q009 | revise | Question, Answer | 2 |
| Q010 | revise | Question, Answer, Class, Evidence | 2 |
| Q011 | revise | Question, Answer, Class, Evidence | 2 |
| Q012 | revise | Question, Answer, Evidence | 3 |
| Q013 | revise | Question, Answer, Evidence | 3 |
| Q014 | revise | Question, Answer, Evidence | 3 |
| Q015 | revise | Question, Answer, Evidence, Sources | 2 |
| Q016 | revise | Question, Answer, Evidence | 1 |
| Q017 | revise | Question, Answer, Evidence | 1 |
| Q018 | replace | Question, Answer | 1 |
| Q019 | revise | Question, Answer | 1 |
| Q020 | replace | Question, Answer, Class, Evidence | 1 |
| Q021 | revise | Question, Answer, Evidence | 1 |
| Q022 | revise | Question, Answer, Evidence | 1 |
| Q023 | revise | Question, Answer, Evidence | 1 |
| Q024 | revise | Question, Answer, Evidence | 1 |
| Q025 | revise | Question, Answer, Evidence | 1 |
| Q026 | revise | Question, Answer, Evidence | 1 |
| Q027 | revise | Question, Answer | 1 |
| Q028 | revise | Question, Answer, Evidence | 1 |
| Q029 | revise | Question, Answer, Evidence | 1 |
| Q030 | revise | Question, Answer, Evidence | 2 |
| Q031 | revise | Question, Answer, Evidence | 2 |
| Q032 | revise | Question, Answer, Evidence | 2 |
| Q033 | revise | Question, Answer, Evidence, Sources | 2 |
| Q034 | revise | Question, Answer, Evidence, Sources | 2 |
| Q035 | revise | Question, Answer, Evidence, Sources | 2 |
| Q036 | revise | Question, Answer, Class, Evidence, Sources | 2 |
| Q037 | revise | Question, Answer, Class, Evidence, Sources | 2 |
| Q038 | revise | Question, Answer, Class, Evidence | 2 |
| Q039 | revise | Question, Answer, Evidence | 1 |
| Q040 | replace | Question, Answer, Evidence, Sources | 2 |

## Targeted Copilot instruction

Use the consolidated proposed corrections JSON as the authoritative **suggestion set**, not the review package as gold. For all 40 IDs, apply `proposed_question` to `question`, `proposed_answer` to `proposed_answer`, `question_class`, and `evidence_span_ids` exactly as specified, deriving `source_ids` from the passage-to-source map. Keep `reference_answer` null and all human-review flags pending. Rebuild the matching annotations/citations, regenerate the package, and validate. Stop at human review, not freeze.

If any proposed change is inconsistent with the actual corpus or the schema, report the exact ID and discrepancy instead of silently omitting it.

## Remaining quality checks before approval

- Verify factual entailment and uncertainty on all revised answers; counting evidence sources alone does not validate multi-hop reasoning.
- Inspect historic vs current runbook time scopes and incident-family split.
- Obtain reviewer decisions and freeze only if the complete Gate Q requirements hold.
