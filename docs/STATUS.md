# ReliabilityGraph status

- **Active phase:** P0 — Foundation and guardrails
- **Active gate:** P0
- **Active task:** P0 complete; awaiting external verification
- **Last validation:** 2026-11-05 local verification passed
- **Last green commit/tag:** None
- **Provider mode:** Deterministic mock/record-replay only; no paid provider calls
- **Corpus status:** Not acquired; rights and source eligibility remain unresolved
- **Next task:** Obtain a successful GitHub Actions run and record account entitlement status
- **Blockers:** GitHub Actions and account entitlement checks are external to this local session

## Local P0 verification

The following commands passed locally from the repository directory:

```text
uv sync --frozen
uv run ruff check .
uv run pyright
uv run pytest       # 8 passed
uv run python scripts/check_secrets.py
```

GitHub Actions is configured in `.github/workflows/ci.yml` but has not been
observed running. No Copilot Student or independent provider credentials were
copied into the repository; entitlement status remains to be checked in the
actual account.

## Working rules

The roadmap and corpus specification are authoritative. Each task is completed
with targeted evidence before the next task begins. Do not copy credentials,
raw uncertain-rights source content, or unverified benchmark claims into this
repository.
