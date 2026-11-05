"""Deterministic local indexing, retrieval, answer generation, and citations."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path

from reliabilitygraph.relations import resolve_local_link

TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
VECTOR_SIZE = 256


@dataclass(frozen=True)
class SearchResult:
    passage_id: str
    source_id: str
    source_key: str
    source_url: str
    title: str
    status: str
    family: str
    section_path: str
    text: str
    lexical_score: float
    vector_score: float
    score: float


@dataclass(frozen=True)
class Citation:
    passage_id: str
    source_id: str
    source_key: str
    source_url: str
    section_path: str
    quote: str


@dataclass(frozen=True)
class Answer:
    answer: str
    citations: tuple[Citation, ...]
    trace_id: str
    retrieval_mode: str
    latency_ms: float
    estimated_cost_usd: float


def _tokens(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def _vector(text: str) -> list[float]:
    values = [0.0] * VECTOR_SIZE
    for token in _tokens(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:2], "big") % VECTOR_SIZE
        values[index] += 1.0
    norm = math.sqrt(sum(value * value for value in values))
    return [value / norm for value in values] if norm else values


def _cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


class SearchIndex:
    """Read-only SQLite FTS5 index with deterministic hashed vectors."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row

    @classmethod
    def build(
        cls,
        output: Path,
        corpus_dir: Path = Path("data/corpus"),
    ) -> SearchIndex:
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.exists():
            output.unlink()
        connection = sqlite3.connect(output)
        connection.executescript(
            """
            PRAGMA journal_mode=DELETE;
            CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE sources (
                source_id TEXT PRIMARY KEY,
                source_key TEXT NOT NULL,
                title TEXT NOT NULL,
                canonical_url TEXT NOT NULL,
                status TEXT NOT NULL,
                family TEXT NOT NULL
            );
            CREATE TABLE passages (
                passage_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                section_path TEXT NOT NULL,
                text TEXT NOT NULL,
                vector TEXT NOT NULL,
                FOREIGN KEY(source_id) REFERENCES sources(source_id)
            );
            CREATE TABLE links (
                link_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                passage_id TEXT NOT NULL,
                resolved_url TEXT NOT NULL,
                target_class TEXT NOT NULL,
                resolution_status TEXT NOT NULL
            );
            CREATE TABLE relation_facts (
                relation_id TEXT PRIMARY KEY,
                from_source_id TEXT NOT NULL,
                to_source_id TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                provenance TEXT NOT NULL,
                evidence_span_ids TEXT NOT NULL,
                review_status TEXT NOT NULL,
                confidence TEXT NOT NULL
            );
            CREATE VIRTUAL TABLE passages_fts USING fts5(
                passage_id UNINDEXED, text, tokenize='unicode61'
            );
            """
        )
        manifest = json.loads(
            (corpus_dir / "manifest.json").read_text(encoding="utf-8")
        )
        sections = {
            item["section_id"]: item["path"]
            for item in json.loads(
                (corpus_dir / "sections.json").read_text(encoding="utf-8")
            )
        }
        sources = {
            item["source_id"]: item for item in manifest["included_sources"]
        }
        for source in sources.values():
            connection.execute(
                "INSERT INTO sources VALUES (?, ?, ?, ?, ?, ?)",
                (
                    source["source_id"],
                    source["key"],
                    source["title"],
                    source["canonical_url"],
                    source["status"],
                    source["family"],
                ),
            )
        passages = json.loads(
            (corpus_dir / "passages.json").read_text(encoding="utf-8")
        )
        links = json.loads(
            (corpus_dir / "links.json").read_text(encoding="utf-8")
        )
        for passage in passages:
            connection.execute(
                "INSERT INTO passages VALUES (?, ?, ?, ?, ?)",
                (
                    passage["passage_id"],
                    passage["source_id"],
                    sections[passage["section_id"]],
                    passage["text"],
                    json.dumps(_vector(passage["text"])),
                ),
            )
            connection.execute(
                "INSERT INTO passages_fts VALUES (?, ?)",
                (passage["passage_id"], passage["text"]),
            )
        for link in links:
            connection.execute(
                "INSERT INTO links VALUES (?, ?, ?, ?, ?, ?)",
                (
                    link["link_id"],
                    link["source_id"],
                    link["passage_id"],
                    link["resolved_url"],
                    link["target_class"],
                    link["resolution_status"],
                ),
            )
        relation_path = corpus_dir.parent / "relations" / "verified_relations.json"
        if relation_path.exists():
            relations = json.loads(
                relation_path.read_text(encoding="utf-8")
            )["relations"]
            for relation in relations:
                connection.execute(
                    "INSERT INTO relation_facts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        relation["relation_id"],
                        relation["from_source_id"],
                        relation["to_source_id"],
                        relation["relation_type"],
                        relation["provenance"],
                        json.dumps(relation["evidence_span_ids"]),
                        relation["review_status"],
                        relation["confidence"],
                    ),
                )
        corpus_hash = hashlib.sha256(
            json.dumps(passages, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        connection.execute(
            "INSERT INTO metadata VALUES (?, ?)",
            ("schema_version", "1"),
        )
        connection.execute(
            "INSERT INTO metadata VALUES (?, ?)", ("corpus_hash", corpus_hash)
        )
        connection.execute(
            "INSERT INTO metadata VALUES (?, ?)",
            ("passage_count", str(len(passages))),
        )
        connection.commit()
        connection.close()
        return cls(output)

    def metadata(self) -> dict[str, str]:
        return dict(self.connection.execute("SELECT key, value FROM metadata"))

    def search(
        self,
        query: str,
        *,
        mode: str = "hybrid",
        limit: int = 5,
        source_id: str | None = None,
        status: str | None = None,
        family: str | None = None,
    ) -> list[SearchResult]:
        if not query.strip():
            return []
        if mode not in {"lexical", "vector", "hybrid"}:
            raise ValueError(f"unsupported retrieval mode: {mode}")
        limit = max(1, min(limit, 20))
        query_vector = _vector(query)
        lexical: dict[str, float] = {}
        if mode in {"lexical", "hybrid"}:
            fts_query = " OR ".join(
                f'"{token}"' for token in _tokens(query)
            )
            if fts_query:
                rows = self.connection.execute(
                    """
                    SELECT passage_id
                    FROM passages_fts WHERE passages_fts MATCH ?
                    ORDER BY bm25(passages_fts) LIMIT 100
                    """,
                    (fts_query,),
                )
                for position, row in enumerate(rows, start=1):
                    lexical[row["passage_id"]] = 1.0 / position
        rows = self.connection.execute(
            """
            SELECT p.*, s.source_key, s.title, s.canonical_url, s.status, s.family
            FROM passages p JOIN sources s ON s.source_id = p.source_id
            """
        )
        results: list[SearchResult] = []
        for row in rows:
            if source_id and row["source_id"] != source_id:
                continue
            if status and row["status"] != status:
                continue
            if family and row["family"] != family:
                continue
            vector_score = _cosine(query_vector, json.loads(row["vector"]))
            lexical_score = lexical.get(row["passage_id"], 0.0)
            if mode == "lexical":
                score = lexical_score
            elif mode == "vector":
                score = vector_score
            else:
                score = 0.6 * lexical_score + 0.4 * vector_score
            if score > 0:
                results.append(
                    SearchResult(
                        row["passage_id"],
                        row["source_id"],
                        row["source_key"],
                        row["canonical_url"],
                        row["title"],
                        row["status"],
                        row["family"],
                        row["section_path"],
                        row["text"],
                        lexical_score,
                        vector_score,
                        score,
                    )
                )
        results.sort(key=lambda result: (-result.score, result.passage_id))
        return results[:limit]

    def links_for_sources(self, source_ids: set[str]) -> list[sqlite3.Row]:
        if not source_ids:
            return []
        return list(
            self.connection.execute(
                "SELECT * FROM links WHERE source_id IN ({})".format(
                    ",".join("?" for _ in source_ids)
                ),
                tuple(source_ids),
            )
        )

    def relation_evidence(
        self, query: str, *, relation_type: str | None = None, limit: int = 5
    ) -> list[SearchResult]:
        """Retrieve relation-supported passages using bounded SQL parameters."""
        terms = [token for token in _tokens(query) if len(token) > 2][:8]
        if not terms:
            return []
        clauses = ["p.text LIKE ?"] * len(terms)
        parameters: list[str] = [f"%{term}%" for term in terms]
        if relation_type:
            clauses.append("r.relation_type = ?")
            parameters.append(relation_type)
        parameters.append(str(max(1, min(limit, 20))))
        rows = self.connection.execute(
            f"""
                SELECT p.*, s.source_key, s.title, s.canonical_url, s.status, s.family
                FROM relation_facts r
                JOIN passages p ON p.passage_id IN (
                    SELECT value FROM json_each(r.evidence_span_ids)
                )
                JOIN sources s ON s.source_id = p.source_id
                WHERE {" AND ".join(clauses)}
                ORDER BY r.relation_id, p.passage_id
                LIMIT ?
                """,
            parameters,
        )
        return [
            SearchResult(
                row["passage_id"], row["source_id"], row["source_key"],
                row["canonical_url"], row["title"], row["status"], row["family"],
                row["section_path"], row["text"], 1.0, 0.0, 1.0,
            )
            for row in rows
        ]

    def close(self) -> None:
        self.connection.close()


def validate_citations(
    citations: tuple[Citation, ...],
    valid_passages: dict[str, str],
) -> None:
    for citation in citations:
        if citation.passage_id not in valid_passages:
            raise ValueError(f"unknown citation: {citation.passage_id}")
        if citation.quote not in valid_passages[citation.passage_id]:
            raise ValueError(f"citation quote mismatch: {citation.passage_id}")


def answer_query(
    index: SearchIndex,
    query: str,
    *,
    mode: str = "hybrid",
    limit: int = 5,
) -> Answer:
    started = time.perf_counter()
    results = index.search(query, mode=mode, limit=limit)
    citations = tuple(
        Citation(
            result.passage_id,
            result.source_id,
            result.source_key,
            result.source_url,
            result.section_path,
            result.text,
        )
        for result in results[:3]
    )
    valid = {
        row["passage_id"]: row["text"]
        for row in index.connection.execute("SELECT passage_id, text FROM passages")
    }
    validate_citations(citations, valid)
    if citations:
        answer_text = " ".join(
            f"[{citation.source_key}] {citation.quote}" for citation in citations
        )
    else:
        answer_text = (
            "I could not find a sufficiently grounded passage in the local corpus."
        )
    trace_id = hashlib.sha256(
        f"{query}|{mode}|{','.join(item.passage_id for item in citations)}".encode()
    ).hexdigest()[:16]
    return Answer(
        answer_text,
        citations,
        trace_id,
        mode,
        (time.perf_counter() - started) * 1000,
        0.0,
    )


def iterative_search(
    index: SearchIndex,
    query: str,
    *,
    passes: int = 2,
    limit: int = 5,
) -> list[SearchResult]:
    """Run bounded clause retrieval without provider calls."""
    if passes < 1 or passes > 3:
        raise ValueError("passes must be between 1 and 3")
    clauses = [part.strip() for part in re.split(r"\band\b|[,;:]", query)]
    queries = [query] + [clause for clause in clauses if clause]
    results: dict[str, SearchResult] = {}
    for subquery in queries[:passes]:
        for result in index.search(subquery, mode="hybrid", limit=limit):
            results.setdefault(result.passage_id, result)
    return sorted(results.values(), key=lambda item: (-item.score, item.passage_id))[
        :limit
    ]


def hyperlink_expand(
    index: SearchIndex,
    query: str,
    *,
    hop_budget: int = 1,
    limit: int = 5,
) -> list[SearchResult]:
    """Expand only links resolving to included Wikitech source URLs."""
    if hop_budget < 0 or hop_budget > 2:
        raise ValueError("hop_budget must be between 0 and 2")
    initial = index.search(query, mode="hybrid", limit=limit)
    if hop_budget == 0:
        return initial
    source_ids = {item.source_id for item in initial}
    source_urls = {
        row["source_id"]: row["canonical_url"]
        for row in index.connection.execute(
            "SELECT source_id, canonical_url FROM sources"
        )
    }
    permitted: set[str] = set()
    for row in index.links_for_sources(source_ids):
        target = resolve_local_link(row, source_urls)
        if target and target not in source_ids:
            permitted.add(target)
    expanded: dict[str, SearchResult] = {item.passage_id: item for item in initial}
    for source_id in permitted:
        for result in index.search(
            query, mode="hybrid", limit=limit, source_id=source_id
        ):
            expanded.setdefault(result.passage_id, result)
    return sorted(expanded.values(), key=lambda item: (-item.score, item.passage_id))[
        :limit
    ]


def relation_guided_search(
    index: SearchIndex,
    query: str,
    *,
    hop_budget: int = 1,
    limit: int = 5,
) -> list[SearchResult]:
    """Expand search through verified, evidence-backed relation facts."""
    if hop_budget < 0 or hop_budget > 2:
        raise ValueError("hop_budget must be between 0 and 2")
    initial = index.search(query, mode="hybrid", limit=limit)
    if hop_budget == 0:
        return initial
    source_ids = {item.source_id for item in initial}
    placeholders = ",".join("?" for _ in source_ids)
    rows = index.connection.execute(
        f"""
        SELECT to_source_id FROM relation_facts
        WHERE from_source_id IN ({placeholders})
          AND review_status = 'verified'
          AND provenance = 'source-stated'
        """,
        tuple(source_ids),
    )
    targets = {row["to_source_id"] for row in rows}
    expanded = {item.passage_id: item for item in initial}
    for source_id in targets:
        for result in index.search(
            query, mode="hybrid", limit=limit, source_id=source_id
        ):
            expanded.setdefault(result.passage_id, result)
    return sorted(expanded.values(), key=lambda item: (-item.score, item.passage_id))[
        :limit
    ]


def render_relation_path(index: SearchIndex, relation_id: str) -> str:
    """Render one bounded relation path with its original evidence."""
    row = index.connection.execute(
        "SELECT * FROM relation_facts WHERE relation_id = ?",
        (relation_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"unknown relation: {relation_id}")
    evidence_ids: list[str] = json.loads(row["evidence_span_ids"])
    if row["provenance"] != "source-stated" or row["review_status"] != "verified":
        raise ValueError("relation is not verified source-stated evidence")
    evidence: list[str] = []
    for passage_id in evidence_ids:
        passage = index.connection.execute(
            "SELECT text FROM passages WHERE passage_id = ?",
            (passage_id,),
        ).fetchone()
        if passage is None:
            raise ValueError(f"missing relation evidence: {passage_id}")
        evidence.append(f"[{passage_id}] {passage['text']}")
    return (
        f"{row['from_source_id']} -[{row['relation_type']}]-> "
        f"{row['to_source_id']}\nEvidence: "
        + " ".join(evidence)
    )


def long_context(
    index: SearchIndex,
    query: str,
    *,
    token_budget: int = 1200,
) -> list[SearchResult]:
    """Assemble a bounded context with explicit token accounting."""
    if token_budget < 1 or token_budget > 10000:
        raise ValueError("token_budget must be between 1 and 10000")
    results = index.search(query, mode="hybrid", limit=20)
    selected: list[SearchResult] = []
    used = 0
    for result in results:
        estimate = len(_tokens(result.text))
        if used + estimate > token_budget:
            continue
        selected.append(result)
        used += estimate
    return selected
