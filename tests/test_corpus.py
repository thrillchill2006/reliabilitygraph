import hashlib
from pathlib import Path

from reliabilitygraph.corpus import (
    PageParser,
    SourceRecord,
    parse_document,
)

FIXTURE = Path(__file__).parent / "fixtures" / "corpus_page.html"


def source_for_fixture() -> SourceRecord:
    content_hash = hashlib.sha256(FIXTURE.read_bytes()).hexdigest()
    return SourceRecord(
        "source-1",
        "TEST",
        "Test page",
        "https://wikitech.wikimedia.org/wiki/Test_page",
        "https://wikitech.wikimedia.org/api/rest_v1/page/html/Test_page",
        "2026-11-05T00:00:00+00:00",
        "1",
        "2026-11-05T00:00:00Z",
        1,
        content_hash,
        "Creative Commons Attribution-Share Alike 4.0",
        "https://creativecommons.org/licenses/by-sa/4.0/",
        "final",
        "test",
        "local-snapshot-authorized-under-site-license",
        "raw/test.html",
    )


def test_parser_extracts_stable_sections_passages_and_typed_links() -> None:
    source = source_for_fixture()
    first = parse_document(source, FIXTURE.read_bytes())
    second = parse_document(source, FIXTURE.read_bytes())

    assert first == second
    sections, passages, links = first
    assert [item.path for item in sections] == ["Summary", "Summary / Response"]
    assert len(passages) == 2
    assert passages[0].anchor
    assert links[0].target_class == "phabricator"
    assert links[0].resolution_status == "link-only"


def test_page_parser_ignores_non_evidence_markup() -> None:
    parser = PageParser()
    parser.feed("<script>secret</script><p>Visible text</p>")

    assert "secret" not in str(parser.sections)
    assert any(item.get("text") == "Visible text" for item in parser.sections)
