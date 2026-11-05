"""Apply validated consolidated corrections to pending P2 benchmark records."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORRECTIONS_PATH = ROOT / "data/benchmark/P2_Consolidated_Proposed_Corrections.json"
QUESTIONS_PATH = ROOT / "data/benchmark/questions.json"
ANNOTATIONS_PATH = ROOT / "data/benchmark/review_annotations.json"
PASSAGES_PATH = ROOT / "data/corpus/passages.json"
SECTIONS_PATH = ROOT / "data/corpus/sections.json"
MANIFEST_PATH = ROOT / "data/corpus/manifest.json"


def load(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict | list) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    corrections_payload = load(CORRECTIONS_PATH)
    questions_payload = load(QUESTIONS_PATH)
    annotations_payload = load(ANNOTATIONS_PATH)
    passages = {item["passage_id"]: item for item in load(PASSAGES_PATH)}
    sections = {item["section_id"]: item for item in load(SECTIONS_PATH)}
    sources = {
        item["source_id"]: item for item in load(MANIFEST_PATH)["included_sources"]
    }
    questions = {
        item["question_id"]: item for item in questions_payload["questions"]
    }
    annotations = {
        item["question_id"]: item for item in annotations_payload["questions"]
    }
    corrections = corrections_payload["proposed_changes"]
    correction_ids = [item["question_id"] for item in corrections]
    unsupported: dict[str, list[str]] = {}

    if len(correction_ids) != 40 or len(set(correction_ids)) != 40:
        raise ValueError("corrections must contain 40 unique question IDs")

    for correction in corrections:
        question_id = correction["question_id"]
        issues: list[str] = []
        question = questions.get(question_id)
        annotation = annotations.get(question_id)
        if question is None or annotation is None:
            issues.append("missing benchmark or annotation record")
        else:
            if question["review_status"] != "pending":
                issues.append("benchmark review is not pending")
            if annotation["review_status"] != "pending":
                issues.append("annotation review is not pending")
            if question["reference_answer"] is not None:
                issues.append("benchmark reference answer is not null")
            if correction.get("review_status") != "pending":
                issues.append("proposed review status is not pending")
            if correction.get("human_approved") is not False:
                issues.append("proposed correction is marked approved")

        citation_records: list[dict[str, str]] = []
        observed_source_ids: list[str] = []
        for evidence_id in correction["evidence_span_ids"]:
            passage = passages.get(evidence_id)
            if passage is None:
                issues.append(f"unsupported evidence ID: {evidence_id}")
                continue
            source = sources.get(passage["source_id"])
            section = sections.get(passage["section_id"])
            if source is None or section is None:
                issues.append(f"incomplete corpus metadata: {evidence_id}")
                continue
            if passage["source_id"] not in observed_source_ids:
                observed_source_ids.append(passage["source_id"])
            citation_records.append(
                {
                    "source_key": source["key"],
                    "source_id": passage["source_id"],
                    "source_url": source["canonical_url"],
                    "section_path": section["path"],
                    "passage_id": evidence_id,
                    "quote": passage["text"],
                }
            )

        if correction.get("distinct_source_count") != len(observed_source_ids):
            issues.append("distinct source count does not match corpus evidence")
        if correction.get("multi_source_candidate") and len(observed_source_ids) < 2:
            issues.append("multi-source candidate has fewer than two sources")
        if issues:
            unsupported[question_id] = issues
            continue

        proposed_answer = correction["proposed_answer"]
        question["question"] = correction["proposed_question"]
        question["question_class"] = correction["question_class"]
        question["proposed_answer"] = proposed_answer
        question["evidence_span_ids"] = list(correction["evidence_span_ids"])
        question["source_ids"] = observed_source_ids

        annotation["question"] = correction["proposed_question"]
        annotation["proposed_answer"] = proposed_answer
        annotation["citations"] = citation_records
        annotation["review_status"] = "pending"

    if unsupported:
        print("unsupported corrections:")
        for question_id, issues in unsupported.items():
            print(f"{question_id}: {'; '.join(issues)}")
        return 1

    questions_payload["question_count"] = len(questions_payload["questions"])
    questions_payload["multi_source_candidate_count"] = sum(
        item["multi_source_candidate"] for item in corrections
    )
    write(QUESTIONS_PATH, questions_payload)
    write(ANNOTATIONS_PATH, annotations_payload)
    print(f"applied {len(corrections)} pending corrections")
    print(
        "multi-source candidates: "
        f"{questions_payload['multi_source_candidate_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
