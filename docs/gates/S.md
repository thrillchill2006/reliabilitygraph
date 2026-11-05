# Gate S — Authorized corpus snapshot

## Observed policy evidence

Policy pages were checked on 2026-11-05:

- Wikimedia API usage requires an identifying User-Agent, rate-limit
  compliance, license compliance, and no concurrent traffic that degrades
  service.
- The robot policy requires current canonical pages, gzip, retry-after handling,
  current REST/API access, and no historical revision crawling.
- Wikimedia reuse guidance identifies the site license through metadata as
  Creative Commons Attribution-Share Alike 4.0 and requires attribution and
  indication of modifications.
- Phabricator task pages T172489 and T253832 were inspected only as link
  context. Their full task content is not included in the snapshot or asserted
  as gold evidence.

The exact URLs and acquisition rules are recorded in
`data/corpus/manifest.json` and `data/corpus/selection_notes.md`.

## Snapshot evidence

The local snapshot contains 19 current Wikitech pages:

- 14 incident reports;
- 5 operational/context pages, including explicitly marked draft and
  work-in-progress pages.

Observed generated statistics:

```text
eligible_documents: 19
incident_families: 19
sections: 218
passages: 370
content_tokens: 15891
links: 98
```

Each included source has a canonical URL, retrieval URL, page ID, current
revision metadata, retrieval timestamp, SHA-256 hash, license metadata, status,
family, and local raw path. The validator checks raw-byte hashes, source
ownership, record references, duplicate passage IDs, and prohibited acquisition
flags.

## Verification

```text
uv run pytest tests/test_corpus.py
  2 passed
uv run python -m reliabilitygraph.corpus --output data\corpus
  19 documents, 218 sections, 370 passages, 98 links
uv run python scripts/validate_corpus.py data\corpus
  P1 snapshot valid: 19 sources, 218 sections, 370 passages, 98 links
uv run ruff check .
  All checks passed
uv run pyright
  0 errors, 0 warnings, 0 informations
uv run pytest
  14 passed
```

The local raw snapshot is ignored from public version control. The manifest,
parsed metadata, statistics, selection notes, and validation code are the
reproducible public control artifacts. No restricted historical revisions or
external attachments were acquired. A Wikimedia HTTP 429 was observed during
expansion; acquisition was corrected to honor `Retry-After`, use five-second
page pacing, and the complete current-page-only snapshot then succeeded.

## Gate decision

**PASS for the bounded local P1 pilot.** Rights and attribution are documented
for this Wikimedia snapshot, and unresolved Phabricator/follow-up material is
explicitly link-only or excluded. Public release of raw text still requires
the recorded attribution and page-specific reuse check.
