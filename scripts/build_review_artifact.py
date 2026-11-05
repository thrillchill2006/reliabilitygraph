# ruff: noqa: E501
"""Build pending P2 review questions from exact frozen P1 passages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus"
BENCHMARK = ROOT / "data" / "benchmark"


SPECS: list[dict[str, Any]] = [
    {
        "id": "Q001",
        "q": "How do the selected incidents distinguish database crash, configuration, and contention mechanisms?",
        "class": "similar-symptom-different-mechanism",
        "keys": ["W3", "W4", "W5"],
        "terms": ["read-only", "contention", "configuration"],
    },
    {
        "id": "Q002",
        "q": "How does the 2017 report connect database recovery to delayed detection?",
        "class": "multi-document-evidence-chain",
        "keys": ["W3", "W6"],
        "terms": ["recovery", "read-only", "detected"],
    },
    {
        "id": "Q003",
        "q": "How does the 2023 report distinguish the switchover test from its user impact?",
        "class": "multi-document-evidence-chain",
        "keys": ["W4", "W7"],
        "terms": ["switchover", "editing", "read-only"],
    },
    {
        "id": "Q004",
        "q": "What uncertainty about immediate cause is preserved across the Commons incident and the review process?",
        "class": "multi-document-evidence-chain",
        "keys": ["W5", "W1"],
        "terms": ["cause", "uncertain", "review"],
    },
    {
        "id": "Q005",
        "q": "What operational distinction applies when a failed database host is a master rather than a replica?",
        "class": "multi-document-evidence-chain",
        "keys": ["W6", "W3"],
        "terms": ["master", "replica", "database"],
    },
    {
        "id": "Q006",
        "q": "How does planned datacenter read-only differ from incident-time read-only?",
        "class": "cross-incident-comparison",
        "keys": ["W7", "W4"],
        "terms": ["read-only", "datacenter"],
    },
    {
        "id": "Q007",
        "q": "Which response actions recur between incident reports and the operational runbook?",
        "class": "multi-document-evidence-chain",
        "keys": ["W3", "W5", "W6"],
        "terms": ["action", "restart", "read-only"],
    },
    {
        "id": "Q008",
        "q": "What source evidence links an incident to a follow-up record, and what remains unknown?",
        "class": "explicit-link-sql-control",
        "keys": ["W3", "W5"],
        "terms": ["task", "action", "Phabricator"],
    },
    {
        "id": "Q009",
        "q": "Why does a completed action not by itself establish prevention of recurrence?",
        "class": "missing-evidence-negative",
        "keys": ["W3", "W5"],
        "terms": ["action", "status", "cause"],
    },
    {
        "id": "Q010",
        "q": "Which documents describe read-only as a protective state after recovery?",
        "class": "multi-document-evidence-chain",
        "keys": ["W3", "W6"],
        "terms": ["read-only", "recovery"],
    },
    {
        "id": "Q011",
        "q": "What later operational documentation qualifies the response described in the 2017 report?",
        "class": "multi-document-evidence-chain",
        "keys": ["W3", "W6"],
        "terms": ["response", "master", "read-only"],
    },
    {
        "id": "Q012",
        "q": "Which records distinguish documented cause from suspected contributor?",
        "class": "cross-incident-comparison",
        "keys": ["W3", "W5", "W9"],
        "terms": ["cause", "probable", "unclear"],
    },
    {
        "id": "Q013",
        "q": "Can the selected sources establish that all read-only events had one underlying cause?",
        "class": "false-analogy-negative",
        "keys": ["W3", "W4", "W5"],
        "terms": ["cause", "read-only"],
    },
    {
        "id": "Q014",
        "q": "Which sources are historical evidence rather than current operational instructions?",
        "class": "time-qualified",
        "keys": ["W3", "W6", "W7"],
        "terms": ["incident", "current", "read-only"],
    },
    {
        "id": "Q015",
        "q": "What evidence would be required before claiming that a corrective action prevented recurrence?",
        "class": "missing-evidence-negative",
        "keys": ["W3", "W5", "W1"],
        "terms": ["action", "review", "incident"],
    },
    {
        "id": "Q016",
        "q": "What does the incident review process say about variable report quality?",
        "class": "single-document-control",
        "keys": ["W1"],
        "terms": ["quality", "incident"],
    },
    {
        "id": "Q017",
        "q": "What does the incident index provide for historical source discovery?",
        "class": "single-document-control",
        "keys": ["W10"],
        "terms": ["incident", "history"],
    },
    {
        "id": "Q018",
        "q": "What is the response sequence for determining whether a failed host is a master or replica?",
        "class": "single-document-control",
        "keys": ["W11"],
        "terms": ["master", "replica"],
    },
    {
        "id": "Q019",
        "q": "What mechanism caused the 2023 wiki outage draft to affect cache-backed traffic?",
        "class": "single-document-control",
        "keys": ["W8"],
        "terms": ["depool", "cache"],
    },
    {
        "id": "Q020",
        "q": "What limitations are visible in the CirrusSearch incident metadata?",
        "class": "missing-evidence-negative",
        "keys": ["W9"],
        "terms": ["YYYY", "unknown", "incident"],
    },
    {
        "id": "Q021",
        "q": "What caused the maps service-capacity incident and how quickly was it detected?",
        "class": "single-document-control",
        "keys": ["W13"],
        "terms": ["reimage", "detected"],
    },
    {
        "id": "Q022",
        "q": "What assumptions and mitigations appear in the planned network maintenance record?",
        "class": "single-document-control",
        "keys": ["W14"],
        "terms": ["maintenance", "router"],
    },
    {
        "id": "Q023",
        "q": "How did a local power event create broader application-service effects?",
        "class": "single-document-control",
        "keys": ["W15"],
        "terms": ["rack", "network"],
    },
    {
        "id": "Q024",
        "q": "What mitigation restored the Varnish-related service and what recommendation followed?",
        "class": "single-document-control",
        "keys": ["W16"],
        "terms": ["redirected", "recommendation"],
    },
    {
        "id": "Q025",
        "q": "What dependency failure caused the memcached incident and what changed afterward?",
        "class": "single-document-control",
        "keys": ["W17"],
        "terms": ["memcached", "twemproxy"],
    },
    {
        "id": "Q026",
        "q": "What redundancy and upgrade conditions contributed to the CirrusSearch outage?",
        "class": "single-document-control",
        "keys": ["W18"],
        "terms": ["redundancy", "Elasticsearch"],
    },
    {
        "id": "Q027",
        "q": "What chain connected logging, disk pressure, and Parsoid unavailability?",
        "class": "single-document-control",
        "keys": ["W19"],
        "terms": ["disk", "logging"],
    },
    {
        "id": "Q028",
        "q": "How did an rsyslog update cascade from Swift into image services?",
        "class": "single-document-control",
        "keys": ["W20"],
        "terms": ["rsyslog", "Swift"],
    },
    {
        "id": "Q029",
        "q": "What configuration change caused the LVS outage and how was it investigated?",
        "class": "single-document-control",
        "keys": ["W21"],
        "terms": ["Puppet", "LVS"],
    },
    {
        "id": "Q030",
        "q": "How do the maps and Parsoid incidents differ in affected layer and detection?",
        "class": "cross-incident-comparison",
        "keys": ["W13"],
        "terms": ["alert", "service"],
    },
    {
        "id": "Q031",
        "q": "How do cache dependency failures differ between Varnish and memcached?",
        "class": "cross-incident-comparison",
        "keys": ["W16"],
        "terms": ["cache", "server"],
    },
    {
        "id": "Q032",
        "q": "How do search-index incidents differ between CirrusSearch and Commons file search?",
        "class": "cross-incident-comparison",
        "keys": ["W9"],
        "terms": ["search", "index"],
    },
    {
        "id": "Q033",
        "q": "Which incidents show a dependency cascade rather than a direct application defect?",
        "class": "cross-incident-comparison",
        "keys": ["W20"],
        "terms": ["cascading", "service"],
    },
    {
        "id": "Q034",
        "q": "Which candidate records contain explicit action status and which do not?",
        "class": "time-qualified",
        "keys": ["W19"],
        "terms": ["Status", "Done"],
    },
    {
        "id": "Q035",
        "q": "Which sources explicitly preserve uncertainty instead of asserting one cause?",
        "class": "false-analogy-negative",
        "keys": ["W5"],
        "terms": ["unclear", "probably", "unknown"],
    },
    {
        "id": "Q036",
        "q": "What evidence supports comparing a planned maintenance event with an unplanned outage?",
        "class": "multi-document-evidence-chain",
        "keys": ["W14"],
        "terms": ["maintenance", "outage"],
    },
    {
        "id": "Q037",
        "q": "What evidence supports comparing operational response guidance with historical remediation?",
        "class": "multi-document-evidence-chain",
        "keys": ["W11"],
        "terms": ["response", "restart"],
    },
    {
        "id": "Q038",
        "q": "Which records show that detection speed and remediation speed are separate properties?",
        "class": "multi-document-evidence-chain",
        "keys": ["W3"],
        "terms": ["detected", "restart"],
    },
    {
        "id": "Q039",
        "q": "What evidence would be needed to claim that a documented action was operationally effective?",
        "class": "missing-evidence-negative",
        "keys": ["W17"],
        "terms": ["action", "Done"],
    },
    {
        "id": "Q040",
        "q": "Which cross-document comparisons remain unsafe until a reviewer confirms the minimum evidence set?",
        "class": "abstention-control",
        "keys": ["W1"],
        "terms": ["review", "cause"],
    },
]


def pick_passage(
    passages: list[dict[str, Any]], source_id: str, terms: list[str]
) -> dict[str, Any]:
    candidates = [
        item
        for item in passages
        if item["source_id"] == source_id
        and any(term.lower() in item["text"].lower() for term in terms)
    ]
    if not candidates:
        candidates = [item for item in passages if item["source_id"] == source_id]
    if not candidates:
        raise ValueError(f"no passage for source {source_id}")
    return max(candidates, key=lambda item: len(item["text"]))


def main() -> int:
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    passages = json.loads((CORPUS / "passages.json").read_text(encoding="utf-8"))
    sections = json.loads((CORPUS / "sections.json").read_text(encoding="utf-8"))
    section_paths = {item["section_id"]: item["path"] for item in sections}
    by_key = {item["key"]: item for item in manifest["included_sources"]}
    questions: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    for spec in SPECS:
        selected = [
            pick_passage(passages, by_key[key]["source_id"], spec["terms"])
            for key in spec["keys"]
        ]
        citations = [
            {
                "source_key": key,
                "source_id": by_key[key]["source_id"],
                "source_url": by_key[key]["canonical_url"],
                "section_path": section_paths.get(passage["section_id"], "unknown"),
                "passage_id": passage["passage_id"],
                "quote": passage["text"],
            }
            for key, passage in zip(spec["keys"], selected, strict=True)
        ]
        proposed_answer = "Pending review. Extractive evidence proposal: " + " ".join(
            f"[{row['source_key']}] {row['quote']}" for row in citations
        )
        questions.append(
            {
                "question_id": spec["id"],
                "question": spec["q"],
                "question_class": spec["class"],
                "split": "review",
                "answerability": "pending-review",
                "source_ids": [row["source_id"] for row in citations],
                "evidence_span_ids": [row["passage_id"] for row in citations],
                "reference_answer": None,
                "proposed_answer": proposed_answer,
                "unacceptable_inferences": [
                    "Do not infer causality, prevention, or operational effectiveness beyond source wording."
                ],
                "review_status": "pending",
                "multi_source_reviewed": False,
            }
        )
        review_rows.append(
            {
                "question_id": spec["id"],
                "question": spec["q"],
                "proposed_answer": proposed_answer,
                "citations": citations,
                "review_status": "pending",
                "reviewer_notes": "",
            }
        )
    BENCHMARK.mkdir(parents=True, exist_ok=True)
    (BENCHMARK / "questions.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "status": "annotation-pending",
                "question_count": len(questions),
                "multi_source_candidate_count": sum(
                    len(item["source_ids"]) > 1 for item in questions
                ),
                "questions": questions,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (BENCHMARK / "review_annotations.json").write_text(
        json.dumps(
            {
                "status": "pending-human-review",
                "instructions": "Confirm or reject each proposed answer and citation set; do not treat this file as approved gold data.",
                "questions": review_rows,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(
        f"wrote {len(questions)} questions and "
        f"{sum(len(item['source_ids']) > 1 for item in questions)} multi-source candidates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
