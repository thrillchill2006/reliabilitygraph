# ReliabilityGraph P2 — Final Evidence Review and Human Sign-off Sheet

**Review basis:** updated `human_review_package.md` uploaded 5 November 2026, checked against previously uploaded `passages.json` and `manifest.json`. This is an independent *proposal* for human review, not a human approval or frozen benchmark. Current `questions.json` and `review_annotations.json` were not re-uploaded after the last agent correction, so full post-change JSON synchronization is **not independently revalidated** here. Original Wikitech pages and unuploaded raw HTML were not re-fetched.

## Overall result

- **40/40** question rows inspected against their cited passages.
- **111/111** cited passage IDs, source keys, canonical links, and displayed excerpts match the uploaded corpus snapshot. This is a mechanical integrity check; the review also assessed answer support and reasoning.
- **35 ready for human sign-off**, **5 targeted revisions**, **0 outright reject** in this pass. Ready ≠ approved.
- **17 labeled genuine multi-source candidates**, but final necessity, independence and balance require human confirmation. Do not equate multi-document citations with real multi-hop links.
- All review decisions remain **Pending**. Gate Q remains **BLOCKED**.

## Five required fixes (before sign-off)

| ID | Issue | Proposed action |
|---|---|---|
| **Q008** | W5 text is an instruction/template-style placeholder, not proof of an incident-specific follow-up task or completion. | Use revised question/answer from `ReliabilityGraph_P2_Targeted_Fixes.json`. |
| **Q015** | A later runbook and a template-style instruction do not establish completion of an incident-specific corrective action. | Use revised question/answer from `ReliabilityGraph_P2_Targeted_Fixes.json`. |
| **Q018** | Remove extraneous commentary about W6; cited W11 passage answers the question directly. | Use revised question/answer from `ReliabilityGraph_P2_Targeted_Fixes.json`. |
| **Q032** | The proposed answer mentions an Elasticsearch 0.90.7/0.90.4 replica-transfer issue, but the current evidence set omits the W18 passage supporting it. | Add passage(s) `af10e4fd0828a5f6b956`. |
| **Q036** | The proposed answer says the router work addressed packet loss/latency, but the current evidence set omits the W14 passage showing those prior symptoms. | Add passage(s) `921d9cd7184fdcc304ef`. |

## Question-by-question sign-off worksheet

| QID | Assessment | Claimed multi-source? | Reviewer decision |
|---|---|---|---|
| Q001 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q002 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q003 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q004 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q005 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q006 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q007 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q008 | **Revise** — see fix file | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q009 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q010 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q011 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q012 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q013 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q014 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q015 | **Revise** — see fix file | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q016 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q017 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q018 | **Revise** — see fix file | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q019 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q020 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q021 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q022 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q023 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q024 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q025 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q026 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q027 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q028 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q029 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q030 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q031 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q032 | **Revise** — see fix file | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q033 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q034 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q035 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q036 | **Revise** — see fix file | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q037 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q038 | Ready for human sign-off | Yes | ☐ Approve ☐ Revise ☐ Reject |
| Q039 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |
| Q040 | Ready for human sign-off | No / control | ☐ Approve ☐ Revise ☐ Reject |

## Additional review notes (not automatic blockers)

- **Paired / overlapping questions:** Q001 and Q013 use the same three incidents for positive vs false-analogy reasoning; Q003 and Q006 both draw on W4+W7; Q005, Q010 and Q011 overlap on W3+W6. Retain only when their distinct evaluation purpose is justified; keep highly overlapping items in one split to avoid benchmark contamination.
- **Question class semantics:** Q013, Q014, Q015, Q034, Q035, Q040 cite more than one document but are flagged “No — context/control.” This can be defensible if controls are deliberately excluded from the *genuine multi-hop* quota; document that rule explicitly. Their labels should not be described as simply “answerable from one document” when their wording asks for a contrast of named records.
- **Q008/Q015:** The record text says “Add links…” but does not identify a particular completed alert-update task. Do not turn an instruction into implementation evidence.
- **Version and time scope:** W6/W7 and W11 are later/current guides; W8 is a draft incident; do not project either backward as historical execution facts.
- **Citation evaluation:** A correct passage id and matching excerpt are necessary but not sufficient; use the checklist below to confirm each claim is entailed, especially negative-evidence claims.

## Incident-family-separated dev/test warning

The cross-incident questions connect the **14 incident sources into only four connected components**. These components are indivisible if *no incident family can appear in both dev and test questions*. The components and their associated questions are:

| Component (incident keys) | Questions touching the component |
|---|---|
| W3, W4, W5, W9, W18, W21 | 21 |
| W15, W16, W17, W20 | 10 |
| W13, W19 | 3 |
| W14, W8 | 3 |

The remaining three questions, Q016–Q018, cite only shared context documents. A workable **candidate** split is the 6-incident component for development and the other three incident components for held-out test, then assign context-only controls according to the pre-registered criteria. This yields 21 incident-based dev questions and 16 incident-based test questions before assigning the 3 context controls. Confirm the split under `docs/decision-criteria.md` and run the leakage validator. Do not assign individual multi-incident questions randomly. Shared runbooks may be visible to both systems; their *evaluation question placement* must still follow the written leakage policy.

## Final reviewer checklist

1. Apply only the five proposed targeted fixes, synchronize question and annotation JSON, and regenerate the review worksheet; maintain pending statuses.
2. Personally confirm each proposed reference answer and exact minimum evidence set, including supported uncertainty and deliberately unanswerable/control cases. Record Approve/Revise/Reject per ID in the actual annotations.
3. Verify at least the required 12–15 **genuinely** cross-source questions after de-duplication. Revisit the corpus if the target cannot be met without contrivance.
4. Assign incident-family-disjoint dev/test groups; test the leakage policy and prevent gold test access during tuning.
5. After approval, populate final reference answers, run all validation, freeze/hash the benchmark and record Gate Q evidence. Do not begin P3 before that.
