# ReliabilityGraph repository rules

- Treat `docs/PLAN.md` as the development roadmap and
  `docs/STATUS.md` as the current execution record.
- Work on one bounded roadmap task at a time; verify it before starting the
  next task.
- Preserve source provenance and rights boundaries. Do not commit credentials,
  raw uncertain-rights corpus content, or unmeasured claims.
- Keep Phase 0 deterministic and offline: use mock or record/replay providers,
  never paid model calls.
- Record exact validation commands and observed results; do not claim CI passed
  without a successful workflow run.
- Do not begin a later phase while the current gate is incomplete.
