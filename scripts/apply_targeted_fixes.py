"""Apply the five validated targeted P2 review fixes."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXES_PATH = ROOT / "data/benchmark/ReliabilityGraph_P2_Targeted_Fixes.json"
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
    fixes = load(FIXES_PATH)["changes"]
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
    expected_ids = {"Q008", "Q015", "Q018", "Q032", "Q036"}
    fix_ids = {item["question_id"] for item in fixes}
    if fix_ids != expected_ids or len(fixes) != 5:
        raise ValueError(
            "targeted fixes must contain exactly Q008, Q015, Q018, Q032, Q036"
        )

    for fix in fixes:
        question_id = fix["question_id"]
        question = questions[question_id]
        annotation = annotations[question_id]
        if (
            question["review_status"] != "pending"
            or annotation["review_status"] != "pending"
            or question["reference_answer"] is not None
        ):
            raise ValueError(
                f"{question_id} is not pending with a null reference answer"
            )

        citation_ids = [item["passage_id"] for item in annotation["citations"]]
        for evidence_id in fix["add_evidence_span_ids"]:
            if evidence_id not in passages:
                raise ValueError(
                    f"{question_id}: unsupported evidence ID {evidence_id}"
                )
            if evidence_id in citation_ids:
                continue
            passage = passages[evidence_id]
            source = sources[passage["source_id"]]
            section = sections[passage["section_id"]]
            annotation["citations"].append(
                {
                    "source_key": source["key"],
                    "source_id": passage["source_id"],
                    "source_url": source["canonical_url"],
                    "section_path": section["path"],
                    "passage_id": evidence_id,
                    "quote": passage["text"],
                }
            )
            citation_ids.append(evidence_id)

        proposed_question = fix["question"] or question["question"]
        question["question"] = proposed_question
        question["proposed_answer"] = fix["proposed_answer"] or question[
            "proposed_answer"
        ]
        question["evidence_span_ids"] = citation_ids
        question["source_ids"] = list(
            dict.fromkeys(
                item["source_id"] for item in annotation["citations"]
            )
        )
        annotation["question"] = proposed_question
        annotation["proposed_answer"] = question["proposed_answer"]
        annotation["review_status"] = "pending"

    write(QUESTIONS_PATH, questions_payload)
    write(ANNOTATIONS_PATH, annotations_payload)
    print("applied targeted fixes: Q008, Q015, Q018, Q032, Q036")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
