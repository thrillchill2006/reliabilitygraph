import json
from pathlib import Path

from reliabilitygraph.relations import load_relations, validate_relations
from reliabilitygraph.retrieval import (
    SearchIndex,
    relation_guided_search,
    render_relation_path,
)


def test_verified_relation_is_corpus_grounded(tmp_path: Path) -> None:
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
    assert validate_relations(relations, source_ids, evidence_ids) == []
    index = SearchIndex.build(tmp_path / "index.sqlite")
    rendered = render_relation_path(index, relations[0].relation_id)
    assert "REFERENCES" in rendered
    assert relations[0].evidence_span_ids[0] in rendered
    assert relation_guided_search(index, "incident status")
    index.close()
