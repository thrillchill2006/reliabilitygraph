# P2 annotation guide

This guide defines the review artifact; it does not represent completed human
annotation. Annotators must work from the frozen local P1 snapshot and must not
inspect retrieval outputs while creating gold records.

## Required fields

- Answerability: `supported`, `partly-supported`, or `unanswerable`.
- Minimum sufficient evidence spans, using stable P1 passage IDs.
- Reference answer written only from those spans.
- Source attribution, time scope, certainty, and action state.
- Explicit unacceptable inferences, especially closure or completion implying
  prevention or causal certainty.
- Question class and whether a single source already contains the full answer.

## Review rules

Preserve source hedges such as suspected, likely, unclear, and reported. Never
create an unqualified `CAUSED` relation. Distinguish source-stated relations
from analyst-derived comparisons. Treat draft or link-only records as
unverified. Mark false analogies and abstention cases explicitly.

The candidate questions in `data/benchmark/questions.json` are review work
items only. They are not gold data until the fields are completed and a human
review is recorded.
