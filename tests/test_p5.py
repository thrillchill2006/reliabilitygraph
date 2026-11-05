from pathlib import Path

from reliabilitygraph.retrieval import (
    SearchIndex,
    hyperlink_expand,
    iterative_search,
    long_context,
)


def test_p5_competitors_are_bounded(tmp_path: Path) -> None:
    index = SearchIndex.build(tmp_path / "index.sqlite")
    assert len(iterative_search(index, "database and recovery", passes=2)) <= 5
    assert len(hyperlink_expand(index, "incident response", hop_budget=1)) <= 5
    context = long_context(index, "database recovery", token_budget=100)
    assert sum(len(item.text.split()) for item in context) <= 100
    index.close()
