"""CLI for validating P2 review artifacts and deterministic evaluation stubs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reliabilitygraph.evidence import (
    evaluate_stub,
    freeze_questions,
    load_questions,
    validate_records,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "score", "freeze"))
    parser.add_argument(
        "--questions", type=Path, default=Path("data/benchmark/questions.json")
    )
    parser.add_argument(
        "--sources", type=Path, default=Path("data/corpus/manifest.json")
    )
    parser.add_argument(
        "--passages", type=Path, default=Path("data/corpus/passages.json")
    )
    parser.add_argument(
        "--mode", choices=("oracle", "empty", "random"), default="oracle"
    )
    args = parser.parse_args()
    questions = load_questions(args.questions)
    manifest = json.loads(args.sources.read_text(encoding="utf-8"))
    passages = json.loads(args.passages.read_text(encoding="utf-8"))
    source_ids = {item["source_id"] for item in manifest["included_sources"]}
    evidence_ids = {item["passage_id"] for item in passages}
    errors = validate_records(questions, source_ids, evidence_ids)
    if args.command == "validate":
        if errors:
            print("\n".join(errors))
            return 1
        print(f"validated {len(questions)} question records")
        return 0
    if args.command == "freeze":
        try:
            benchmark_hash, canonical = freeze_questions(
                questions, source_ids, evidence_ids
            )
        except ValueError as error:
            print(f"cannot freeze benchmark: {error}")
            return 1
        output = args.questions.with_name("frozen.json")
        output.write_text(canonical, encoding="utf-8")
        print(f"frozen benchmark: {benchmark_hash}")
        return 0
    print(json.dumps(evaluate_stub(questions, args.mode), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
