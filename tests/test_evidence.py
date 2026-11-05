import pytest

from reliabilitygraph.evidence import (
    GoldQuestion,
    evaluate_stub,
    evidence_scores,
    freeze_questions,
    validate_records,
)


def reviewed_question(split: str = "dev") -> GoldQuestion:
    return GoldQuestion(
        "Q1",
        "What happened?",
        "single-document-control",
        split,
        "supported",
        ("source-1",),
        ("passage-1",),
        "The source reports an event.",
        ("Do not infer prevention.",),
        "reviewed",
        False,
    )


def test_evidence_scores_match_hand_calculated_example() -> None:
    scores = evidence_scores({"a", "b"}, {"b", "c"})

    assert scores == {"precision": 0.5, "recall": 0.5, "f1": 0.5}


def test_oracle_and_empty_stubs_have_expected_scores() -> None:
    question = reviewed_question()

    oracle = evaluate_stub([question], "oracle")
    empty = evaluate_stub([question], "empty")

    assert oracle["mean_f1"] == 1.0
    assert empty["mean_recall"] == 0.0


def test_pending_questions_cannot_be_frozen() -> None:
    pending = reviewed_question()
    pending = GoldQuestion(
        pending.question_id,
        pending.question,
        pending.question_class,
        "review",
        "pending-review",
        pending.source_ids,
        (),
        None,
        (),
        "pending",
        False,
    )

    with pytest.raises(ValueError, match="pending human review"):
        freeze_questions([pending], {"source-1"}, {"passage-1"})


def test_validation_rejects_incident_family_leakage() -> None:
    dev = reviewed_question("dev")
    test = GoldQuestion(
        "Q2",
        "What changed?",
        "single-document-control",
        "test",
        "supported",
        ("source-1",),
        ("passage-1",),
        "The source reports a change.",
        ("Do not infer prevention.",),
        "reviewed",
        False,
    )

    errors = validate_records([dev, test], {"source-1"}, {"passage-1"})

    assert "incident-family leakage between dev and test" in errors
