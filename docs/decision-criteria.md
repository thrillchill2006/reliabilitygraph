# P2 evaluation decision criteria

These criteria are recorded before any retriever is built.

- Evidence recall and citation validity take priority over unsupported answer
  completeness.
- A system must not receive credit for a citation whose passage does not support
  the claim.
- Negative and false-analogy questions must reward explicit abstention or
  qualification.
- Compare systems on the same frozen question split, evidence format, and
  output budget.
- Report latency, estimated cost, and curation/indexing effort separately from
  retrieval quality.
- A graph path cannot be declared valuable from a human-oracle relation set
  alone; extracted relations require a separate later gate.
- Gate G decisions are `CONTINUE`, `SIMPLIFY`, `STOP`, or `REWORK`, based on
  preregistered dev evidence and cost/fidelity tradeoffs.
