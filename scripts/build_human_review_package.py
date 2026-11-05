"""Build a compact, pending-human-review package from P2 annotations."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANNOTATIONS = ROOT / "data/benchmark/review_annotations.json"
QUESTIONS = ROOT / "data/benchmark/questions.json"
CORRECTIONS = ROOT / "data/benchmark/P2_Consolidated_Proposed_Corrections.json"
MANIFEST = ROOT / "data/corpus/manifest.json"
OUTPUT = ROOT / "data/benchmark/human_review_package.md"


def compact(text: str, limit: int = 220) -> str:
    value = " ".join(text.split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def main() -> int:
    annotations = json.loads(ANNOTATIONS.read_text(encoding="utf-8"))
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))["questions"]
    corrections = json.loads(CORRECTIONS.read_text(encoding="utf-8"))[
        "proposed_changes"
    ]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources = {
        item["source_id"]: item
        for item in manifest["included_sources"]
    }
    annotation_by_id = {
        item["question_id"]: item for item in annotations["questions"]
    }
    candidate_by_id = {
        item["question_id"]: item["multi_source_candidate"]
        for item in corrections
    }
    multi_source_count = sum(candidate_by_id[item["question_id"]] for item in questions)

    lines = [
        "# P2 Human Review Package",
        "",
        "Status: **pending human review**. This is a derived worksheet; it does "
        "not approve annotations, create gold data, or freeze the benchmark.",
        "",
        "Review each row with the existing annotation in "
        "`data/benchmark/review_annotations.json`. Choose only **Approve**, "
        "**Revise**, or **Reject** after checking the linked source passages.",
        "",
        "## Review summary",
        "",
        f"- Questions: {len(questions)}",
        f"- Batches: {(len(questions) + 9) // 10} batches of at most 10",
        f"- Multi-source candidates: {multi_source_count}",
        "- Current decision for every question: `Pending`",
        "- Current split for every question: `review`; dev/test leakage review "
        "remains required before freeze.",
        "",
    ]

    for batch_start in range(0, len(questions), 10):
        batch = questions[batch_start : batch_start + 10]
        batch_number = batch_start // 10 + 1
        lines.extend(
            [
                f"## Batch {batch_number} (Q{batch[0]['question_id'][1:]}–"
                f"Q{batch[-1]['question_id'][1:]})",
                "",
                "| ID | Question | Proposed reference answer | Supporting "
                "passages, excerpts, and source links | Multi-source dependency | "
                "Unsupported inferences / ambiguities | Flags | Decision |",
                "|---|---|---|---|---|---|---|---|",
            ]
        )
        for question in batch:
            question_id = question["question_id"]
            annotation = annotation_by_id[question_id]
            citation_lines: list[str] = []
            citation_sources: list[str] = []
            families: list[str] = []
            for citation in annotation["citations"]:
                source = sources.get(citation["source_id"])
                if source is None:
                    source_label = citation["source_key"]
                    families.append("UNKNOWN")
                else:
                    source_label = source["key"]
                    families.append(source["family"])
                citation_sources.append(source_label)
                citation_lines.append(
                    f"`{citation['passage_id']}` — "
                    f"{compact(citation['quote'])} "
                    f"[{source_label}]({citation['source_url']})"
                )

            unique_sources = list(dict.fromkeys(citation_sources))
            unique_families = set(families)
            multi_source = len(unique_sources) > 1
            flags = [
                "evidence/citation review required",
                "review-only split; leakage check required",
            ]
            if multi_source and len(unique_families) < len(unique_sources):
                flags.append("same-family multi-source risk")
            if question["question_class"] == "false-analogy-negative":
                flags.append("false-analogy boundary")
            if question["answerability"] != "answerable":
                flags.append("answerability pending")

            dependency = (
                "Yes — requires all cited source passages"
                if candidate_by_id[question_id]
                else (
                    "No — evidence context only; not a multi-source dependency"
                    if multi_source
                    else "No — single source"
                )
            )
            if not multi_source and question["question_class"] in {
                "multi-document-evidence-chain",
                "comparison",
            }:
                flags.append("question class/source-count mismatch")

            lines.append(
                "| "
                + " | ".join(
                    [
                        question_id,
                        cell(question["question"]),
                        cell(annotation["proposed_answer"]),
                        "<br>".join(citation_lines),
                        dependency,
                        cell(
                            "; ".join(annotation.get("unacceptable_inferences", []))
                            or (
                                "None recorded; reviewer must check for "
                                "unsupported inference."
                            )
                        ),
                        cell("; ".join(flags)),
                        "Pending",
                    ]
                )
                + " |"
            )
        lines.extend(["", ""])

    lines.extend(
        [
            "## Reviewer checklist",
            "",
            "- Verify every passage ID, excerpt, section, and source URL against the "
            "current corpus snapshot.",
            "- Replace proposed answers only with source-grounded reference answers; "
            "record unsupported inferences and ambiguity explicitly.",
            "- Confirm that multi-source questions require genuinely independent "
            "sources and identify the minimum evidence set.",
            "- Check incident-family-aware dev/test separation before approval; "
            "do not approve the current `review` split as a frozen split.",
            "- Record decisions in the existing annotation workflow. Do not edit "
            "this generated package to imply approval.",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {len(questions)} questions in {(len(questions) + 9) // 10} batches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
