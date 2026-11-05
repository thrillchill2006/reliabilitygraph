"""Build the reproducible local P3 search index."""

from pathlib import Path

from reliabilitygraph.retrieval import SearchIndex

if __name__ == "__main__":
    index = SearchIndex.build(Path("artifacts/reliabilitygraph.sqlite"))
    print(index.metadata())
    index.close()
