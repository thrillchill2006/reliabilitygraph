"""Validate the P6 verified relation facts against the local corpus."""

from __future__ import annotations

import json
from pathlib import Path

from reliabilitygraph.relations import load_relations, validate_relations


def main() -> int:
    corpus = Path("data/corpus")
    source_ids = {
        item["source_id"]
        for item in json.loads(
            (corpus / "manifest.json").read_text(encoding="utf-8")
        )["included_sources"]
    }
    evidence_ids = {
        item["passage_id"]
        for item in json.loads(
            (corpus / "passages.json").read_text(encoding="utf-8")
        )
    }
    relations = load_relations(Path("data/relations/verified_relations.json"))
    errors = validate_relations(relations, source_ids, evidence_ids)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"validated {len(relations)} verified relation(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
