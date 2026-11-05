# Gate G — P6 verified-relationship decision

## Status

**REWORK — provisional.** The benchmark remains unfrozen, and the pilot has
only one verified cross-document relation from existing corpus metadata.

## P6 evidence

- R3 local-link diagnosis found 1 exact included-source URL match out of 98
  links; no corpus files were relabeled or rewritten.
- P6 relation validation found 1 verified `source-stated` `REFERENCES` edge,
  backed by passage `6d1248e18dac279640fb`.
- R5 uses bounded parameterized SQL over the same relation facts.
- R6a uses verified source-stated relations only, with a hop budget of 2 and
  original passage evidence required for path rendering.
- No `CAUSED` edge was created.
- Document-level annotation remains pending for all 19 pilot sources; recorded
  annotation effort is 0 person-minutes because no manual annotation was
  performed in this execution.

## Provisional comparison

The 40-question pending benchmark was used only for engineering diagnostics:

| System | Recall@5 | Median latency | Estimated cost |
|---|---:|---:|---:|
| R4 long-context | 0.5858 | 17.91 ms | $0.00 |
| R1 hybrid | 0.4188 | 17.72 ms | $0.00 |
| R3 hyperlink | 0.4188 | 19.17 ms | $0.00 |
| R6a relation-guided | 0.4188 | 18.40 ms | $0.00 |
| R5 SQL evidence | 0.0000 | 0.08 ms | $0.00 |

These are not final benchmark results.

## Decision

**REWORK.** Do not proceed to P7. First complete document-level relation
annotation, independently re-annotate a subset, measure agreement, and rerun
paired dev comparisons on a reviewed/frozen split. The current evidence does
not support attributing any gain to graph traversal.
