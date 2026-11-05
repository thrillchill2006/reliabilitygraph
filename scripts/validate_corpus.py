"""Validate local P1 snapshot integrity and deterministic indexing outputs."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "data/corpus")
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    passages = json.loads((root / "passages.json").read_text(encoding="utf-8"))
    sections = json.loads((root / "sections.json").read_text(encoding="utf-8"))
    links = json.loads((root / "links.json").read_text(encoding="utf-8"))
    source_ids = set()
    for source in manifest["included_sources"]:
        source_ids.add(source["source_id"])
        raw_path = root / source["raw_path"]
        content = raw_path.read_bytes()
        observed = hashlib.sha256(content).hexdigest()
        if observed != source["content_sha256"]:
            raise SystemExit(f"hash mismatch: {source['key']}")
        if not source["canonical_url"].startswith("https://wikitech.wikimedia.org/wiki/"):
            raise SystemExit(f"non-canonical source URL: {source['key']}")
    if any(item["source_id"] not in source_ids for item in passages + sections + links):
        raise SystemExit("orphaned parsed record")
    for passage in passages:
        if not passage["text"].strip():
            raise SystemExit("empty passage")
        if len(passage["text"]) > 5000:
            raise SystemExit(f"oversized passage: {passage['passage_id']}")
        if not passage["anchor"]:
            raise SystemExit(f"missing passage anchor: {passage['passage_id']}")
    if len({item["passage_id"] for item in passages}) != len(passages):
        raise SystemExit("duplicate passage ID")
    if manifest["acquisition"]["historical_revisions_crawled"]:
        raise SystemExit("historical revision acquisition is prohibited")
    if manifest["acquisition"]["external_attachments_downloaded"]:
        raise SystemExit("external attachment acquisition is prohibited")
    print(
        "P1 snapshot valid: "
        f"{len(source_ids)} sources, {len(sections)} sections, "
        f"{len(passages)} passages, {len(links)} links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
