"""Verified relation facts and bounded SQL/traversal helpers."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class RelationFact:
    relation_id: str
    from_source_id: str
    to_source_id: str
    relation_type: str
    provenance: str
    evidence_span_ids: tuple[str, ...]
    review_status: str
    confidence: str


def _normalize_url(value: str) -> str:
    parsed = urlsplit(value)
    return urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            parsed.query,
            "",
        )
    )


def load_relations(path: Path) -> list[RelationFact]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        RelationFact(
            item["relation_id"],
            item["from_source_id"],
            item["to_source_id"],
            item["relation_type"],
            item["provenance"],
            tuple(item["evidence_span_ids"]),
            item["review_status"],
            item["confidence"],
        )
        for item in payload["relations"]
    ]


def validate_relations(
    relations: list[RelationFact],
    source_ids: set[str],
    evidence_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for relation in relations:
        if relation.relation_id in seen:
            errors.append(f"duplicate relation ID: {relation.relation_id}")
        seen.add(relation.relation_id)
        if relation.from_source_id not in source_ids:
            errors.append(f"unknown relation source: {relation.relation_id}")
        if relation.to_source_id not in source_ids:
            errors.append(f"unknown relation target: {relation.relation_id}")
        if any(item not in evidence_ids for item in relation.evidence_span_ids):
            errors.append(f"unknown relation evidence: {relation.relation_id}")
        if relation.relation_type == "CAUSED":
            errors.append(f"unqualified CAUSED relation: {relation.relation_id}")
        if relation.provenance not in {"source-stated", "analyst-derived"}:
            errors.append(f"invalid relation provenance: {relation.relation_id}")
        if (
            relation.provenance == "analyst-derived"
            and relation.review_status != "pending"
        ):
            errors.append(f"unreviewed derived relation: {relation.relation_id}")
    return errors


def resolve_local_link(
    link: sqlite3.Row,
    source_urls: dict[str, str],
) -> str | None:
    """Resolve only an exact URL match to an included local source."""
    if link["target_class"] != "wikitech":
        return None
    target_url = _normalize_url(link["resolved_url"])
    for source_id, canonical_url in source_urls.items():
        if _normalize_url(canonical_url) == target_url:
            return source_id
    return None
