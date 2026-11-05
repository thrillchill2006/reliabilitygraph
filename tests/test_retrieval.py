from pathlib import Path

from reliabilitygraph.retrieval import SearchIndex, answer_query


def test_index_rebuild_and_hybrid_citation(tmp_path: Path) -> None:
    index = SearchIndex.build(tmp_path / "index.sqlite")
    assert index.metadata()["passage_count"] == "370"
    results = index.search("out of memory read only", limit=3)
    assert results
    answer = answer_query(index, "out of memory read only")
    assert answer.citations
    assert answer.estimated_cost_usd == 0.0
    index.close()


def test_metadata_filter(tmp_path: Path) -> None:
    index = SearchIndex.build(tmp_path / "index.sqlite")
    results = index.search("incident", status="draft")
    assert results
    assert all(result.status == "draft" for result in results)
    index.close()


def test_fts_query_quotes_operator_words(tmp_path: Path) -> None:
    index = SearchIndex.build(tmp_path / "index.sqlite")
    assert index.search("only", mode="lexical")
    index.close()
