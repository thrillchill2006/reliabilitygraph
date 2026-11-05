"""Typed evidence records and deterministic gold-evaluation utilities."""

from __future__ import annotations

import hashlib
import json
import random
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, cast


@dataclass(frozen=True)
class EvidenceSpan:
    passage_id: str
    source_id: str
    section_path: str
    start: int
    end: int
    quote_fingerprint: str
    snapshot_sha256: str


@dataclass(frozen=True)
class ClaimRecord:
    claim_id: str
    text: str
    claim_type: str
    source_id: str
    evidence_span_ids: tuple[str, ...]
    certainty: str
    time_scope: str
    attribution: str


@dataclass(frozen=True)
class RelationRecord:
    relation_id: str
    from_id: str
    to_id: str
    relation_type: str
    provenance: str
    evidence_span_ids: tuple[str, ...]
    review_status: str
    extraction_version: str


@dataclass(frozen=True)
class GoldQuestion:
    question_id: str
    question: str
    question_class: str
    split: str
    answerability: str
    source_ids: tuple[str, ...]
    evidence_span_ids: tuple[str, ...]
    reference_answer: str | None
    unacceptable_inferences: tuple[str, ...]
    review_status: str
    multi_source_reviewed: bool


@dataclass(frozen=True)
class RunArtifact:
    run_id: str
    system_name: str
    benchmark_sha256: str
    question_ids: tuple[str, ...]
    evidence_ids_by_question: dict[str, tuple[str, ...]]
    answers_by_question: dict[str, str]
    config: dict[str, Any]


def _as_tuple(value: Iterable[str]) -> tuple[str, ...]:
    return tuple(value)


def load_questions(path: Path) -> list[GoldQuestion]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        GoldQuestion(
            item["question_id"],
            item["question"],
            item["question_class"],
            item["split"],
            item["answerability"],
            _as_tuple(item["source_ids"]),
            _as_tuple(item["evidence_span_ids"]),
            item["reference_answer"],
            _as_tuple(item["unacceptable_inferences"]),
            item["review_status"],
            item["multi_source_reviewed"],
        )
        for item in payload["questions"]
    ]


def validate_records(
    questions: list[GoldQuestion],
    valid_source_ids: set[str],
    valid_evidence_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    split_families: dict[str, set[str]] = {}
    for question in questions:
        if question.question_id in seen:
            errors.append(f"duplicate question ID: {question.question_id}")
        seen.add(question.question_id)
        if question.split not in {"dev", "test", "review"}:
            errors.append(f"invalid split: {question.question_id}")
        if any(source not in valid_source_ids for source in question.source_ids):
            errors.append(f"unknown source: {question.question_id}")
        if any(
            evidence not in valid_evidence_ids
            for evidence in question.evidence_span_ids
        ):
            errors.append(f"unknown evidence: {question.question_id}")
        if question.review_status == "reviewed":
            if not question.reference_answer:
                errors.append(
                    f"reviewed question has no answer: {question.question_id}"
                )
            if not question.evidence_span_ids and question.answerability == "supported":
                errors.append(
                    f"supported question has no evidence: {question.question_id}"
                )
            if not question.unacceptable_inferences:
                errors.append(f"missing inference constraints: {question.question_id}")
        if question.split in {"dev", "test"}:
            split_families.setdefault(question.split, set()).update(question.source_ids)
    if split_families.get("dev", set()) & split_families.get("test", set()):
        errors.append("incident-family leakage between dev and test")
    return errors


def benchmark_readiness_errors(
    payload: dict[str, Any],
    *,
    require_reviewed: bool = True,
) -> list[str]:
    """Report missing approval fields without changing benchmark state."""
    errors: list[str] = []
    questions = payload.get("questions")
    if not isinstance(questions, list):
        return ["benchmark questions must be a list"]
    questions = cast(list[Any], questions)
    seen: set[str] = set()
    for raw_item in questions:
        if not isinstance(raw_item, dict):
            errors.append("benchmark question must be an object")
            continue
        item = cast(dict[str, Any], raw_item)
        question_id = item.get("question_id", "<missing>")
        if question_id in seen:
            errors.append(f"duplicate question ID: {question_id}")
        seen.add(question_id)
        for field in (
            "question",
            "question_class",
            "evidence_span_ids",
            "source_ids",
            "reference_answer",
            "review_status",
            "split",
        ):
            if field not in item:
                errors.append(f"{question_id}: missing field {field}")
        if require_reviewed and item.get("review_status") != "reviewed":
            errors.append(f"{question_id}: review_status is not reviewed")
        if require_reviewed and not item.get("reference_answer"):
            errors.append(f"{question_id}: reference_answer is missing")
        if require_reviewed and item.get("split") == "review":
            errors.append(f"{question_id}: split is still review")
    return errors


def freeze_questions(
    questions: list[GoldQuestion],
    valid_source_ids: set[str],
    valid_evidence_ids: set[str],
) -> tuple[str, str]:
    errors = validate_records(questions, valid_source_ids, valid_evidence_ids)
    if errors:
        raise ValueError("; ".join(errors))
    if any(item.review_status != "reviewed" for item in questions):
        raise ValueError("benchmark contains pending human review")
    if any(item.split == "review" for item in questions):
        raise ValueError("benchmark contains review-only records")
    payload = json.dumps(
        {"questions": [asdict(item) for item in questions]},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest(), payload.decode("utf-8")


def evidence_scores(
    expected: set[str], actual: set[str]
) -> dict[str, float]:
    true_positive = len(expected & actual)
    precision = true_positive / len(actual) if actual else 0.0
    recall = true_positive / len(expected) if expected else (1.0 if not actual else 0.0)
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    return {"precision": precision, "recall": recall, "f1": f1}


def evaluate_stub(
    questions: list[GoldQuestion], mode: str, seed: int = 0
) -> dict[str, Any]:
    rng = random.Random(seed)
    per_question: dict[str, dict[str, float]] = {}
    reviewed_questions = [
        question for question in questions if question.review_status == "reviewed"
    ]
    for question in reviewed_questions:
        expected = set(question.evidence_span_ids)
        if mode == "oracle":
            actual: set[str] = expected
        elif mode == "empty":
            actual = set()
        elif mode == "random":
            actual = {rng.choice(sorted(expected))} if expected else set()
        else:
            raise ValueError(f"unknown stub mode: {mode}")
        per_question[question.question_id] = evidence_scores(expected, actual)
    values = list(per_question.values())
    return {
        "mode": mode,
        "questions": len(reviewed_questions),
        "pending_questions": len(questions) - len(reviewed_questions),
        "mean_precision": sum(item["precision"] for item in values) / len(values)
        if values
        else 0.0,
        "mean_recall": sum(item["recall"] for item in values) / len(values)
        if values
        else 0.0,
        "mean_f1": sum(item["f1"] for item in values) / len(values) if values else 0.0,
        "per_question": per_question,
    }
