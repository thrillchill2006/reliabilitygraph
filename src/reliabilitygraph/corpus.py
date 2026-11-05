"""Policy-aware current-page acquisition and deterministic corpus indexing."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import html
import json
import re
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "ReliabilityGraph/0.1 (research corpus; contact via repository)"
WIKITECH = "https://wikitech.wikimedia.org"
REST_PAGE = f"{WIKITECH}/api/rest_v1/page"
SUMMARY_PAGE = f"{REST_PAGE}/summary"
HTML_PAGE = f"{REST_PAGE}/html"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
POLICY_URLS = {
    "api_usage": "https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_API_Usage_Guidelines",
    "access": "https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy",
    "robot": "https://wikitech.wikimedia.org/wiki/Robot_policy",
    "reuse": "https://www.mediawiki.org/wiki/Wikimedia_APIs/Content_reuse",
    "user_agent": "https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy",
}

SELECTED_SOURCES = (
    {
        "key": "W1",
        "title": "Incident review ritual",
        "status": "operational-context",
        "family": "incident-review-process",
        "reason": "Verified process context explaining the incident-learning workflow.",
    },
    {
        "key": "W10",
        "title": "Incident status",
        "status": "operational-context",
        "family": "incident-index",
        "reason": "Verified incident-status/index context for source discovery.",
    },
    {
        "key": "W11",
        "title": "Incident response/Runbook",
        "status": "operational-context",
        "family": "incident-response-runbook",
        "reason": (
            "Verified response context linked by the incident documentation "
            "index."
        ),
    },
    {
        "key": "W3",
        "title": "Incidents/2017-07-28 s5 (WikiData and dewiki) read-only",
        "status": "final",
        "family": "database-crash-read-only",
        "reason": (
            "Verified incident report with failure, detection, response, "
            "and action sections."
        ),
    },
    {
        "key": "W4",
        "title": "Incidents/2023-02-22 read only",
        "status": "final",
        "family": "configuration-read-only",
        "reason": (
            "Verified final report for a distinct configuration/switchover "
            "mechanism."
        ),
    },
    {
        "key": "W5",
        "title": "Incidents/2021-04-27 Commons wiki primary db",
        "status": "final",
        "family": "database-contention-read-only",
        "reason": (
            "Verified final report with qualified causal language and "
            "corrective actions."
        ),
    },
    {
        "key": "W6",
        "title": "MariaDB/Troubleshooting",
        "status": "work-in-progress",
        "family": "operational-runbook",
        "reason": (
            "Verified operational context page; retained with its "
            "work-in-progress status."
        ),
    },
    {
        "key": "W7",
        "title": "Switch Datacenter",
        "status": "operational-documentation",
        "family": "planned-read-only",
        "reason": "Verified operational context for scheduled read-only behavior.",
    },
    {
        "key": "W8",
        "title": "Incidents/2023-02-22 wiki outage",
        "status": "draft",
        "family": "cache-maintenance-outage",
        "reason": "Verified draft incident retained with visible draft status.",
    },
    {
        "key": "W9",
        "title": "Incidents/2021-11-10 cirrussearch commonsfile outage",
        "status": "final",
        "family": "search-index-outage",
        "reason": "Verified final incident with explicit unresolved metadata fields.",
    },
    {
        "key": "W13",
        "title": "Incidents/2019-06-11 maps",
        "status": "status-not-stated",
        "family": "service-capacity-outage",
        "reason": (
            "Verified incident page with impact, detection, timeline, and "
            "actions."
        ),
    },
    {
        "key": "W14",
        "title": "Incidents/20110524-PlannedMaintenance",
        "status": "status-not-stated",
        "family": "network-maintenance",
        "reason": (
            "Verified historical maintenance incident with planned and "
            "observed work."
        ),
    },
    {
        "key": "W15",
        "title": "Incidents/20110926-DBandPower",
        "status": "status-not-stated",
        "family": "network-power-outage",
        "reason": (
            "Verified historical incident covering rack, network, and "
            "database effects."
        ),
    },
    {
        "key": "W16",
        "title": "Incidents/20120120-Varnish",
        "status": "status-not-stated",
        "family": "cache-network-outage",
        "reason": "Verified incident with mechanism, mitigation, and recommendation.",
    },
    {
        "key": "W17",
        "title": "Incidents/20130508-memcached",
        "status": "status-not-stated",
        "family": "cache-dependency-outage",
        "reason": "Verified incident with dependency failure and remediation evidence.",
    },
    {
        "key": "W18",
        "title": "Incidents/20131118-CirrusSearch",
        "status": "status-not-stated",
        "family": "search-cluster-outage",
        "reason": "Verified incident with redundancy, upgrade, and recovery evidence.",
    },
    {
        "key": "W19",
        "title": "Incidents/20140211-Parsoid",
        "status": "status-not-stated",
        "family": "service-disk-outage",
        "reason": "Verified incident with detection, response, and action status.",
    },
    {
        "key": "W20",
        "title": "Incidents/20131205-Swift",
        "status": "status-not-stated",
        "family": "dependency-cascade-outage",
        "reason": "Verified incident with dependency cascade and corrective actions.",
    },
    {
        "key": "W21",
        "title": "Incidents/20140203-LVS",
        "status": "status-not-stated",
        "family": "load-balancer-outage",
        "reason": "Verified incident with configuration failure and failover response.",
    },
)

EXCLUDED_SOURCES = (
    {
        "key": "T172489",
        "title": "Phabricator T172489",
        "status": "link-only",
        "reason": (
            "Referenced link was inspected, but task/repository material "
            "is not ingested."
        ),
    },
    {
        "key": "T253832",
        "title": "Phabricator T253832",
        "status": "link-only",
        "reason": (
            "Referenced task was inspected as link context only; no task "
            "text is ingested."
        ),
    },
    {
        "key": "T3",
        "title": "Reported 2020 Commons read-only follow-up report",
        "status": "excluded",
        "reason": (
            "Specific primary URL was not independently identified; "
            "deliberately not guessed."
        ),
    },
)


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    key: str
    title: str
    canonical_url: str
    retrieval_url: str
    retrieved_at: str
    revision_id: str
    revision_timestamp: str
    page_id: int
    content_sha256: str
    license_name: str
    license_url: str
    status: str
    family: str
    rights_status: str
    raw_path: str


@dataclass(frozen=True)
class SectionRecord:
    section_id: str
    source_id: str
    path: str
    level: int
    title: str


@dataclass(frozen=True)
class PassageRecord:
    passage_id: str
    source_id: str
    section_id: str
    ordinal: int
    text: str
    anchor: str
    token_estimate: int


@dataclass(frozen=True)
class LinkRecord:
    link_id: str
    source_id: str
    passage_id: str | None
    href: str
    resolved_url: str
    label: str
    target_class: str
    resolution_status: str


class PageParser(HTMLParser):
    """Extract headings, paragraphs, and links from rendered current HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.sections: list[dict[str, Any]] = []
        self.links: list[dict[str, str]] = []
        self._heading: list[str] | None = None
        self._heading_level = 0
        self._paragraph: list[str] | None = None
        self._paragraph_links: list[dict[str, str]] = []
        self._active_link: dict[str, str] | None = None
        self._section_stack: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag in {"script", "style", "table", "figure"}:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if re.fullmatch(r"h[1-6]", tag):
            self._heading = []
            self._heading_level = int(tag[1])
        elif tag == "p":
            self._paragraph = []
            self._paragraph_links = []
        elif tag == "a" and self._paragraph is not None:
            self._active_link = {"href": attributes.get("href") or "", "label": ""}
            self._paragraph_links.append(self._active_link)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "table", "figure"} and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if re.fullmatch(r"h[1-6]", tag) and self._heading is not None:
            title = clean_text("".join(self._heading))
            if title:
                stack_size = max(self._heading_level - 2, 0)
                self._section_stack = self._section_stack[:stack_size]
                self._section_stack.append(title)
                self.sections.append(
                    {
                        "path": " / ".join(self._section_stack),
                        "level": self._heading_level,
                        "title": title,
                    }
                )
            self._heading = None
        elif tag == "p" and self._paragraph is not None:
            text = clean_text("".join(self._paragraph))
            if text:
                self.sections.append(
                    {
                        "path": " / ".join(self._section_stack) or "Document",
                        "level": 0,
                        "title": "",
                        "text": text,
                        "links": self._paragraph_links,
                    }
                )
            self._paragraph = None
            self._paragraph_links = []
        elif tag == "a":
            self._active_link = None

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._heading is not None:
            self._heading.append(data)
        if self._paragraph is not None:
            self._paragraph.append(data)
        if self._active_link is not None:
            self._active_link["label"] += data


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:20]


def request_json(url: str, *, retries: int = 3) -> dict[str, Any]:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
        },
    )
    for attempt in range(retries):
        try:
            with urlopen(request, timeout=30) as response:
                payload = response.read()
                if response.headers.get("Content-Encoding") == "gzip":
                    payload = gzip.decompress(payload)
                return json.loads(payload.decode("utf-8"))
        except HTTPError as error:
            if error.code == 429:
                delay = int(error.headers.get("Retry-After", "60"))
                time.sleep(delay)
            elif attempt < retries - 1:
                time.sleep(2**attempt)
            else:
                raise
        except (URLError, TimeoutError):
            if attempt == retries - 1:
                raise
            time.sleep(2**attempt)
    raise RuntimeError("unreachable")


def fetch_bytes(url: str, *, retries: int = 3) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html",
            "Accept-Encoding": "gzip",
        },
    )
    for attempt in range(retries):
        try:
            with urlopen(request, timeout=30) as response:
                payload = response.read()
                if response.headers.get("Content-Encoding") == "gzip":
                    payload = gzip.decompress(payload)
                return payload
        except HTTPError as error:
            if error.code == 429:
                delay = int(error.headers.get("Retry-After", "60"))
                time.sleep(delay)
            elif attempt < retries - 1:
                time.sleep(2**attempt)
            else:
                raise
        except (URLError, TimeoutError):
            if attempt == retries - 1:
                raise
            time.sleep(2**attempt)
    raise RuntimeError("unreachable")


def classify_link(url: str) -> str:
    host = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()
    if "phabricator.wikimedia.org" in host:
        return "phabricator"
    if "wikitech.wikimedia.org" in host:
        return "wikitech"
    if path.endswith((".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp")):
        return "media-attachment"
    if host.endswith("wikimedia.org"):
        return "wikimedia"
    return "external"


def parse_document(
    source: SourceRecord, html_bytes: bytes
) -> tuple[list[SectionRecord], list[PassageRecord], list[LinkRecord]]:
    parser = PageParser()
    parser.feed(html_bytes.decode("utf-8", errors="replace"))
    sections: list[SectionRecord] = []
    section_ids: dict[str, str] = {}
    passages: list[PassageRecord] = []
    links: list[LinkRecord] = []
    passage_ordinal = 0
    for item in parser.sections:
        if item["level"] > 0:
            section_id = stable_id(source.source_id, item["path"])
            section_ids[item["path"]] = section_id
            sections.append(
                SectionRecord(
                    section_id,
                    source.source_id,
                    item["path"],
                    item["level"],
                    item["title"],
                )
            )
            continue
        section_path = item["path"]
        section_id = section_ids.get(
            section_path, stable_id(source.source_id, section_path)
        )
        if section_id not in {record.section_id for record in sections}:
            sections.append(
                SectionRecord(
                    section_id,
                    source.source_id,
                    section_path,
                    0,
                    section_path.rsplit(" / ", 1)[-1],
                )
            )
        text = item["text"]
        passage_id = stable_id(
            source.source_id, section_path, str(passage_ordinal), text
        )
        passage = PassageRecord(
            passage_id,
            source.source_id,
            section_id,
            passage_ordinal,
            text,
            stable_id(source.content_sha256, section_path, text),
            max(1, (len(text) + 3) // 4),
        )
        passages.append(passage)
        for raw_link in item["links"]:
            href = raw_link["href"]
            if not href or href.startswith("#"):
                continue
            resolved = urljoin(source.canonical_url, href)
            links.append(
                LinkRecord(
                    stable_id(source.source_id, passage_id, resolved),
                    source.source_id,
                    passage_id,
                    href,
                    resolved,
                    raw_link["label"],
                    classify_link(resolved),
                    "link-only"
                    if classify_link(resolved) == "phabricator"
                    else "unresolved",
                )
            )
        passage_ordinal += 1
    return sections, passages, links


def acquire(output: Path, *, sleep_seconds: float = 5.0) -> dict[str, Any]:
    raw_dir = output / "raw"
    parsed_dir = output / "parsed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    parsed_dir.mkdir(parents=True, exist_ok=True)
    rights = request_json(
        f"{WIKITECH}/w/api.php?action=query&meta=siteinfo&siprop=rightsinfo&format=json"
    )["query"]["rightsinfo"]
    sources: list[SourceRecord] = []
    sections: list[SectionRecord] = []
    passages: list[PassageRecord] = []
    links: list[LinkRecord] = []
    retrieved_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    for index, candidate in enumerate(SELECTED_SOURCES):
        title_path = quote(candidate["title"].replace(" ", "_"), safe="")
        summary_url = f"{SUMMARY_PAGE}/{title_path}"
        html_url = f"{HTML_PAGE}/{title_path}"
        summary = request_json(summary_url)
        html_bytes = fetch_bytes(html_url)
        content_hash = sha256_bytes(html_bytes)
        source_id = stable_id("wikitech", candidate["key"], content_hash)
        canonical_url = summary["content_urls"]["desktop"]["page"]
        raw_name = f"{candidate['key']}-{content_hash[:12]}.html"
        (raw_dir / raw_name).write_bytes(html_bytes)
        source = SourceRecord(
            source_id,
            candidate["key"],
            candidate["title"],
            canonical_url,
            html_url,
            retrieved_at,
            str(summary["revision"]),
            str(summary["timestamp"]),
            int(summary["pageid"]),
            content_hash,
            str(rights["text"]),
            str(rights["url"]),
            candidate["status"],
            candidate["family"],
            "local-snapshot-authorized-under-site-license",
            f"raw/{raw_name}",
        )
        parsed_sections, parsed_passages, parsed_links = parse_document(
            source, html_bytes
        )
        sources.append(source)
        sections.extend(parsed_sections)
        passages.extend(parsed_passages)
        links.extend(parsed_links)
        (parsed_dir / f"{candidate['key']}.json").write_text(
            json.dumps(
                {
                    "source": asdict(source),
                    "sections": [asdict(item) for item in parsed_sections],
                    "passages": [asdict(item) for item in parsed_passages],
                    "links": [asdict(item) for item in parsed_links],
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        if index < len(SELECTED_SOURCES) - 1:
            time.sleep(sleep_seconds)
    manifest = {
        "schema_version": 1,
        "created_at": retrieved_at,
        "source_authority": "docs/CORPUS/CORPUS_SPECIFICATION.md",
        "acquisition": {
            "interface": "Wikimedia REST page HTML plus REST summary",
            "current_pages_only": True,
            "historical_revisions_crawled": False,
            "external_attachments_downloaded": False,
            "user_agent": USER_AGENT,
            "delay_seconds": sleep_seconds,
            "retries": 3,
            "failure_behavior": "exponential backoff, then fail visibly",
        },
        "rights": {
            "license_name": rights["text"],
            "license_url": rights["url"],
            "policy_urls": POLICY_URLS,
            "attribution_required": True,
            "modifications_must_be_indicated": True,
            "public_release_note": (
                "Raw snapshots are local-only; public artifacts must preserve "
                "attribution and license terms."
            ),
        },
        "included_sources": [asdict(item) for item in sources],
        "excluded_or_link_only": list(EXCLUDED_SOURCES),
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (output / "links.json").write_text(
        json.dumps([asdict(item) for item in links], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    stats = {
        "eligible_documents": len(sources),
        "incident_families": sorted({item.family for item in sources}),
        "sections": len(sections),
        "passages": len(passages),
        "links": len(links),
        "content_tokens": sum(item.token_estimate for item in passages),
        "link_classes": {
            kind: sum(item.target_class == kind for item in links)
            for kind in sorted({item.target_class for item in links})
        },
    }
    (output / "stats.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    selection = [
        "# P1 selection notes",
        "",
        (
            "The pilot includes five current Wikitech pages selected from the "
            "corpus dossier."
        ),
        "Final incident reports are mixed with two operational context pages to avoid",
        "overfitting the corpus to one incident family.",
        "",
        "Phabricator records were inspected only as link context. Their full task",
        "content is not included in the snapshot or asserted as gold evidence.",
        "",
        "## Policy basis",
        "",
        *[f"- {name}: {url}" for name, url in POLICY_URLS.items()],
        f"- Site rights metadata: {rights['text']} ({rights['url']})",
        "",
        "Raw HTML is retained under the local snapshot directory for reproducibility.",
        "It is not a public release artifact until attribution and any applicable",
        "page-specific reuse requirements are checked.",
    ]
    (output / "selection_notes.md").write_text(
        "\n".join(selection) + "\n", encoding="utf-8"
    )
    (output / "sections.json").write_text(
        json.dumps([asdict(item) for item in sections], indent=2), encoding="utf-8"
    )
    (output / "passages.json").write_text(
        json.dumps([asdict(item) for item in passages], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/corpus"))
    args = parser.parse_args()
    stats = acquire(args.output)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
