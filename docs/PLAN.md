# ReliabilityGraph — Final Master Development Plan

**Project:** Project 1 — Knowledge Graph–Augmented Retrieval for Enterprise-Like Evidence  
**Working product:** ReliabilityGraph: Evidence-Grounded Incident Intelligence for Distributed Systems  
**Document version:** 2.0 (revised from Claude's 4 November 2026 v1.0 draft)  
**Review date:** 4 November 2026  
**Recommended repository path:** `docs/PLAN.md`  
**Corpus authority:** `docs/corpus/CORPUS_SPECIFICATION.md`  
**Status:** **Ready to begin Phase 0, subject to the P0 account/environment checks.** The corpus and graph hypothesis are **not** yet validated.  
**Primary principle:** **One bounded task, one verification, one evidence-backed gate at a time.**

> **Accuracy convention.** **[V]** = verified in the supplied corpus dossier or checked directly against an official source; **[P]** = proposed engineering decision or threshold; **[U]** = unresolved, to be investigated before claiming success. Research publications document *their* methods and results, not a promised improvement for ReliabilityGraph. Estimated effort, cost and performance are never measured outcomes.

## 0. Executive decision — what is approved and what is not

**Approved problem:** Build a retrospective, citation-grounded research application that helps engineers examine *historical* software incidents: what failed, which layers or dependencies were implicated, what response was documented, what corrective work followed, and what later records do or do not establish. The system must distinguish source-reported claims from our own comparisons and assumptions. It does **not** diagnose live systems, execute repairs, certify infrastructure, or make operational decisions.

**Approved initial corpus ecosystem:** A small, deliberately selected snapshot of **Wikimedia Wikitech** incident reports, relevant operational context pages, and only those linked Wikimedia Phabricator records whose access and reuse conditions have been reviewed. Do not ingest all pages in an incident category as if they were all final reports. [V: dossier §§1–6; R1–R5 below]

**Conditional expansion:** First-party GitHub, Cloudflare and Google Cloud incident/postmortem reports, after the pilot and rights review. The expansion is **not** a precondition for v1.0.

**Unproven thesis:** For some cross-document questions, **relationship-aware evidence retrieval** will recover more complete and more faithfully qualified supporting evidence than well-engineered lexical/vector search, iterative retrieval, explicit-link expansion, SQL evidence queries or long-context reading.

**Approved engineering posture:** Default to the smallest maintainable system; use a frozen local corpus, SQLite/FTS5, exact dense similarity at pilot scale, one common retrieval interface, a small Python service and reproducible evaluations. **Do not install a graph database on principle.** The relationship-aware experiment is mandatory; a graph database is conditional.

**Success is not defined as “Neo4j wins.”** Success is a trustworthy deployed artifact, a defensible experiment, an auditable technical decision, and accurate resume claims. If graph guidance proves valuable, ship it; if it does not, ship the best evidence system and report the negative result, or revisit the corpus through a documented decision.

### One-page readiness matrix

| Dimension | Status on 4 Nov 2026 | Completion evidence |
|---|---|---|
| Problem rationale | **[V] supported** by documented incident-learning workflow | Dossier and first-party Wikitech process page |
| Pilot corpus candidates | **[V] selected URLs exist**; final eligible snapshot **[U]** | P1 source manifest, hashes, rights notes |
| Full Phabricator evidence chain | **[U]** partly reported by previous research; not gold-ready | P1 primary record inspection and attribution review |
| Genuine multi-document benchmark | **[P]** | P2 reviewed evidence-set annotations |
| Graph improvement over simpler retrieval | **[U]** | P6/P8 comparative experiments |
| Neo4j requirement | **Not established** | Gate G + optional P10a comparison |
| Provider API/model credits | **[U] account-dependent** | P0 provider and billing checks |
| Hosting choice and public cost | **[U]** | P4 deploy spike, measured costs and safeguards |
| Released app and resume metrics | **Not achieved** | P8–P9 release artifacts |

## 1. Project contract, user experience and boundaries

### 1.1 Problem to solve

A question may begin with a symptom rather than a ticket ID: “Why might a database look healthy while writes fail?” The relevant evidence may live in a dated incident report, a linked corrective-action discussion, a separate later incident, and a current runbook. The system should return a **source-backed explanation** that separates:

- symptom versus implicated system layer;
- trigger, contributing factors, and an investigator/operator's *stated* cause;
- incident-time evidence versus later/current documentation;
- proposed work, merged/recorded work, and later *observed* behavior;
- similarities between incidents versus the facts that distinguish them;
- supported conclusions versus information the public record does not establish.

This problem is narrower than generic “chat with postmortems” and more defensible than promising arbitrary root-cause diagnosis.

### 1.2 Intended users and public demo scope

**Users:** software/backend engineers, SREs, platform engineers, AI-infrastructure engineers, and learners of distributed systems. 

**User-facing minimum:** ask an evidence question; see a grounded answer; inspect claim-level citations to original pages/sections; see source date/revision and document-status indicators; understand uncertainty; access at least several curated demonstration questions; optionally view *why a retriever selected evidence* if the trace is safe to expose.

**Explicit exclusions:** no live-system access, no autonomous repair, no private incident archives, no advice presented as authoritative production operations, no person-focused incident/responder graph, no unsupported claims of causality, no invented incident status updates.

### 1.3 Deliverables for a credible GitHub/resume project

- Clean public repository with clear licensing and attribution; reproducible environment and tests.
- Curated, versioned *source manifest* and a documented authorized reconstruction method for eligible corpus items.
- Strong retrieval baseline; a set of fair non-graph alternatives; a conditional relationship-guided method.
- Benchmark set with source-grounded answers and explicit limitations, plus frozen test evaluation.
- Working deployment (cost-protected, rate-limited) or an explicitly labeled hosted static demonstration when paid model usage is unavailable.
- README centered on the problem, live demonstration, evaluation table, architecture choice, and honest limitations.
- Demo video/screenshots, release tag, issue/PR history, and interview decision rationale.

**No metric, dataset size, cost saving or graph advantage should appear as an achievement before it is measured.**

## 2. Corpus authority and source boundaries

The accompanying [`CORPUS_SPECIFICATION.md`](./corpus/CORPUS_SPECIFICATION.md) is the source authority for content selection and factual evidence. This plan describes **how to acquire, test, build and ship** that corpus, not an alternative corpus. The dossier's **V/R/P/U labels** continue to apply: **R** items (research-reported only) cannot become gold benchmark evidence without primary-source verification.

### 2.1 Core starting links (source candidates, not already ingested)

| Key | First-party source | Why it matters | Caution |
|---|---|---|---|
| W1 | [Wikitech incident review ritual](https://wikitech.wikimedia.org/wiki/Incident_review_ritual) | Documents incident-learning, quality and knowledge-discovery problem | A process proposal; not evidence of market demand |
| W2 | [Incident documentation category](https://wikitech.wikimedia.org/wiki/Category:Incident_documentation) | Discovery index | Contains pages other than polished final incident reports |
| W3 | [2017 s5 Wikidata/dewiki read-only incident](https://wikitech.wikimedia.org/wiki/Incidents/2017-07-28_s5_%28WikiData_and_dewiki%29_read-only) | Database restart/read-only symptom and monitoring action lead | A dated, operator-authored report, not universal system behavior |
| W4 | [2023 read-only incident](https://wikitech.wikimedia.org/wiki/Incidents/2023-02-22_read_only) | Similar symptom, application/configuration mechanism | Preserve report status and date |
| W5 | [2021 Commons primary database incident](https://wikitech.wikimedia.org/wiki/Incidents/2021-04-27_Commons_wiki_primary_db) | Contrasting database incident and reported uncertainty | Verify precise passage claims from snapshot |
| W6 | [MariaDB troubleshooting](https://wikitech.wikimedia.org/wiki/MariaDB/Troubleshooting) | Current role-dependent operational context | Work-in-progress page; not proof of 2017 practice |
| W7 | [Datacenter switchover](https://wikitech.wikimedia.org/wiki/Switch_Datacenter) | App/database read-only distinctions | Current and historical material must be distinguished |
| W8 | [2023 wiki outage](https://wikitech.wikimedia.org/wiki/Incidents/2023-02-22_wiki_outage) | Different failure family; false analogy controls | Draft status in dossier |
| W9 | [2021 CirrusSearch commonsfile outage](https://wikitech.wikimedia.org/wiki/Incidents/2021-11-10_cirrussearch_commonsfile_outage) | Cross-service dependency retrieval | Verify completeness and report status |
| T1 | [Phabricator T172489](https://phabricator.wikimedia.org/T172489) | Reported monitoring follow-up for W3 | **[U]** discussion/details/rights not fully reverified |
| T2 | [Phabricator T253832](https://phabricator.wikimedia.org/T253832) | Reported runbook follow-up | **[U]** primary content and rights need inspection |

**2017 → task → later observation caution.** W3 independently links T172489. Previous research identified a later Commons incident and the T253832 documentation task, but the dossier did not reproduce the complete independent chain. **Do not pre-label it as verified causal effectiveness.** P1 must resolve the exact references and access; P2 must decide whether the question is source-supported. If it cannot, drop that benchmark family without fabricating evidence.

### 2.2 Snapshot policy — corrected after checking Wikimedia rules

**Important correction to original Claude draft:** Do **not** design a crawler that repeatedly requests old revisions or uses `oldid` URL enumeration to “pin” history. Wikimedia's current [Robot policy](https://wikitech.wikimedia.org/wiki/Robot_policy) discourages crawling old revisions and gives separate limits for website, REST, Action API, and other resources. See also [Wikimedia API access policy](https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy).

Instead:

1. Use the approved current-page content interface (canonical pages or an API method permitted by the current policy). Prefer a small hand-approved list; no broad crawler.
2. Identify the client as required, obey request spacing/concurrency and `Retry-After`/server errors; log request provenance. **Recheck the live policy before execution.**
3. On first authorized retrieval, capture page title, canonical URL, returned/displayed revision ID when available, retrieval timestamp, content SHA-256, and raw/parsed content locally.
4. Freeze **the locally obtained copy** and manifest. All development and tests read the local snapshot, not fresh live pages.
5. Retain revision metadata for provenance; do not infer that a previously obtained revision can be recollected by historical crawling. If exact historic revision retrieval is later essential, obtain a permitted/export-approved mechanism before doing it.
6. For tasks, use Phabricator's documented access/export route only if permitted; otherwise retain a link-only reference with status **unverified**.
7. Avoid re-fetching unchanged pages needlessly. Record effective access limits actually used, not guessed permissive thresholds.

**Rights gate:** Public readability is not blanket redistribution permission. Verify text licensing and attribution on **each site/content type**, particularly task discussions, comments, embedded images, external charts and fragments of other organizations' documents. Store raw snapshots privately/local-only if rights are uncertain; a public repository should be rebuildable using authorized fetches without shipping questionable text. Show only defensibly short attributed evidence extracts and source links in the demo, subject to the verified terms. Record these decisions in `docs/corpus/rights.md`.

### 2.3 Corpus sizing and acceptance

**[P] Pilot target:** approximately 12–20 incident reports plus 5–10 operational/context pages, with a small number of directly relevant verified tasks. These are planning targets, not known eligible counts. Include varied failure mechanisms, not only database read-only cases. Exclude low-quality pages if they cannot support faithful claims, but keep legitimate draft/in-review records if their status is visible and analytically appropriate.

A selection sheet records for every candidate: inclusion/exclusion reason, original URL, event date, document status, size, critical links, rights decision, retrieval hash, and whether it can support independent gold evidence.

**Stage-2 [P] only:** first-party GitHub Availability Reports, Cloudflare postmortems and Google Cloud incident reports. Review each publisher's rights and provenance separately. This expansion tests generalization; it is never used to rescue a weak baseline by adding more data only to the graph arm.

## 3. What established Graph RAG projects actually did (research-verified design lessons)

These are **methodological references, not dependencies, blueprints or proof of superiority for this corpus**. Source links and review date appear in §17.

| Public project / research | Documented pattern | Relevance here | What **not** to copy blindly |
|---|---|---|---|
| **Microsoft GraphRAG** | Processes text units, extracts entities/relationships/claims, builds communities and summaries; supports local, global, DRIFT and basic search. The repo warns indexing can be expensive and currently describes the research project as largely in maintenance mode. | Use source-linked text units; distinguish entity-local questions from corpus-wide synthesis; profile indexing cost. | Expensive community detection/summarization and an entire framework for a few dozen incidents. |
| **HippoRAG / HippoRAG 2** | Combines LLM-extracted knowledge connections with graph-based propagation such as Personalized PageRank for associative/multi-hop retrieval; evaluates against iterative/other retrieval. | Treat graph traversal as an **evidence selection method**, measure retrieval recall and latency versus iteration. | Reported research gains as predictions for incident data; install its entire stack without a measurable need. |
| **LightRAG** | Uses paired vector and graph representations, higher/lower level information retrieval, incremental update ideas and distinct storage abstractions; exposes source-oriented citation features in its maintained implementation. | Prototype lightweight relation-to-passage expansion and test whether it improves evidence selection. | Multiple specialized databases, complicated ingestion infrastructure and broad UI feature set before a successful pilot. |
| **Google SRE postmortem practice** (domain reference, not Graph RAG) | Incident reviews capture sequence, contributing conditions and corrective follow-up; aggregation can reveal patterns beyond individual incidents. | Anchor question types in a genuine engineering workflow and preserve blameless attribution. | Treating postmortems as full causal truth or inferring a corrective action prevented future failures. |

**Common useful pattern:** source acquisition → canonical evidence units → optional structured knowledge → candidate retrieval → evidence selection → answer generation → citation verification → evaluation and error analysis. **There is no universal requirement that the graph live in Neo4j** or that it beat a strong, corpus-specific non-graph baseline.

**Architecture-level consequence:** Begin with a small tested retrieval experiment, and only add entity/relation extraction when a hand-verified *oracle relationship layer* shows a repeatable benefit. Microsoft GraphRAG's global/community summarization is a possible future ablation, not a v1.0 requirement. Incremental graph mutation is unnecessary while the corpus is frozen.

## 4. Architecture and deliberate non-decisions

```text
OFFLINE AUTHORING / EVALUATION
  Authorized source selection → local frozen snapshot + SHA-256 manifest
     → status-aware section parser → provenance-anchored passages + outbound links
     → SQLite tables + FTS5 + exact dense search index
     → common Retriever(question, budget, filters) → EvidenceSet
         B-1 closed-book; R0 lexical; R1 hybrid/rerank
         R2 iterative; R3 explicit-link expansion; R4 long-context
         R5 evidence-table SQL; R6a checked-relationship guidance
         R6b extracted-relationship guidance [only if approved]
     → same Answerer → claim/evidence/citation format → validators
     → frozen evaluation harness, ablations and immutable run artifacts

PUBLIC READ-ONLY DEMONSTRATION
  FastAPI → /ask, /health, /trace/{safe_trace_id} → minimal UI
     → source-link evidence panel + dates/status/limitations
     → strict request/input limits + spend controls + kill switch
```

**Evidence layers:**

1. **Source artifact:** canonical URL, title, source site, author/source type, event/publication/retrieval dates, revision/hash and reuse assessment.
2. **Evidence unit:** section path, text span, quote-anchor/fingerprint, source document ID and document status. Chunking is an implementation view of evidence, not the identity of the gold answer.
3. **Attributed claim:** the source *states* a symptom, trigger, contributor, response, effect, uncertainty, etc., with time scope and verbatim supporting passage.
4. **Relation/derived comparison:** typed relation linking claims, incidents, artifacts or components; provenance on each edge; explicit `SOURCE_STATED` vs `ANALYST_DERIVED`; derivations cite evidence on both sides.

**Do not create an unqualified universal `CAUSED` edge.** Attribute causal language to the original report and preserve hedges (reported, likely, suspected, confirmed-by-source). Distinguish `PROPOSED`, `COMPLETED_AS_REPORTED`, `OBSERVED_AFTERWARD`, `UNKNOWN`; none implies a counterfactual safety/reliability improvement.

### 4.1 Defaults, and the trigger to reconsider each

| Concern | Default **[P]** | Reason / reconsideration trigger |
|---|---|---|
| Language | Python 3.12 | Accessible, testable, Copilot-friendly; pin in config |
| Environment | `uv`, `ruff`, `pytest`, optional `pyright`, Docker | Limit tool count; choose consistent commands; pin dependencies |
| Primary store | SQLite + FTS5 + relational evidence/link tables | One read-only, immutable pilot artifact; good baseline for graph-vs-SQL |
| Vectors | Exact cosine/dot similarity over cached normalized embeddings, with one simple reranker | Pilot scale may not justify vector-server/ANN indexing; measure actual size and latency |
| LLM | Replaceable provider adapter, record/replay, deterministic fixtures | **No mandatory paid Anthropic key in P0.** Select provider/cost only after entitlement and model checks |
| Graph | Typed relational edge table + recursive/limited traversal initially | Test knowledge value before Neo4j operations |
| API | FastAPI; only required endpoints | Separation between offline evaluation and online demo |
| UI | Minimal Streamlit **or** static page, choose once in P4 | Avoid maintaining two UI stacks |
| Deployment | Read-only container hosting with snapshot or legally reconstructible index | Host/pricing to be checked in P4; do not claim a free tier |
| Evaluation | Custom harness, documented criteria, frozen artifacts | Ensure clear evidence-level metrics; may incorporate libraries only if they save effort |

**Storage reconsideration is measurement-driven:** Reevaluate SQLite/exact search if actual corpus scale, build time, memory, query latency, contention or operational requirements exceed measured budgets. The original draft's “50k passages” is an **illustrative tripwire**, not a universal SQLite limitation.

### 4.2 Data contracts to stabilize early

- `SourceRecord`: stable local ID, canonical URL/title, event/publication/retrieval dates, revision/hash, source kind, status, rights reference.
- `EvidenceSpan`: source ID, section path, start/end or quote fingerprint, raw text snapshot reference, `passage_id` computed from snapshot+span.
- `ClaimRecord`: claim ID, source attribution, claim type, text, certainty/hedging, time scope, evidence span IDs.
- `RelationRecord`: from/to IDs, relation type, source-stated versus derived, evidence span IDs, review status, extraction version.
- `EvidenceSet`: ordered evidence span IDs, retrieval path, scores, token count, retriever/version, optional cost/latency.
- `AnswerClaim`: claim text, supported-by evidence span IDs, status/time label, support quality/abstention state.
- `RunArtifact`: code commit, corpus hash, gold-set hash, model/embedding/reranker versions, config, retrieval outputs, evaluated answers, judge method, latency/cost and environment metadata.

The specific JSON schema and DDL are created in P2, not prematurely frozen by this roadmap.

## 5. Measurement contract and benchmark integrity

A graph-shaped diagram is not evidence of a graph advantage. **Predefine what will count as an improvement before viewing the final test outcomes.** Gold questions and evidence sets are built from primary snapshots, not from model answers or extracted graph edges.

### 5.1 Benchmark question classes **[P]**

Aim initially for **about 40 carefully reviewed questions** (a screening/evaluation set, not a statistically decisive universal benchmark). The actual class counts are adjusted to verified corpus coverage, not to make a graph win.

| Class | Purpose | Example pattern (illustrative, not prescored gold) |
|---|---|---|
| Single-document control | Test ordinary retrieval and answer fidelity | What did this particular incident report say about detection? |
| Similar symptom / different mechanism | Separate layers, roles and causes | Which read-only incidents differ at application versus database layer? |
| Multi-document evidence chain | Recover incident → follow-up → later evidence | What record supports the proposed correction, and is there later observation? |
| Cross-incident comparison | Synthesize mechanisms without false equivalence | What pattern is shared, and which conditions differ? |
| Time-qualified | Prevent present-day runbook from rewriting historical behavior | What was documented at a specific event date? |
| Missing-evidence / negative | Appropriate abstention | Does closure prove a fix prevented recurrence? |
| Explicit-link/SQL control | Test whether cheap graph or table join already works | Which specific task is linked to this incident? |

**[P] Quality gate:** Seek **12–15 or more genuinely useful multi-source questions**, where the minimum complete evidence set cannot be supplied from a single comprehensive document. If not achievable, reconsider scope/corpus. Never remove documents or artificially fracture them to manufacture multi-hop cases.

### 5.2 Gold-answer specification

For each question, record:

- stable question ID, natural phrasing, real user purpose and class;
- answerability (supported / partly supported / unanswerable), as-of date if relevant;
- **minimum sufficient source/evidence set(s)**; support may have more than one valid combination;
- exact source URL, frozen source hash/revision, section path and quote anchors;
- required relationships and any required negative/qualification statements;
- facts that **must not** be inferred (e.g., task closed ⇒ permanent prevention);
- whether one original source already has the full answer;
- relevance of an official hyperlink, SQL join or long-context reading;
- annotator, review status and adjudication notes; never assume external expert sign-off.

**Anchor to source evidence, not to implementation chunks.** A change to chunking may change passage IDs but must not silently change the gold truth. A deterministic resolver maps quote/section anchors to the chosen snapshot, and gold validation fails on ambiguous or missing anchors.

### 5.3 Leakage-control policy

- **Freeze document snapshot before labeling** and freeze the gold *test* questions and evidence references before retriever tuning.
- Split by **incident/evidence family** wherever possible. Linked reports, task discussions and direct re-tellings belong to the same family; otherwise near-duplicate source leakage invalidates held-out claims. Ensure every test question remains answerable from the test-time indexed corpus.
- **Dev set:** inspect errors and tune retrieval, models and prompts. **Test set:** run once after system freeze, with predeclared repeats for stochastic outputs and no post-hoc tuning. If you change the system after a test failure, create `test-v2` and openly disclose the repeated look.
- All systems index the same eligible source snapshot and operate under comparable evidence/context budgets. For R4 long-context, state the full token budget explicitly; when it is larger than normal retrieval context, treat it as a distinct, stronger-cost comparator rather than pretending budgets match.
- **Curate relationship facts document-by-document using a fixed annotation guide, not question-by-question.** Do not add an edge solely because a benchmark question asks for it. Reviewed relations for held-out questions may be present as uniformly created document annotations, but test question text and expected answers must not guide their construction.
- Automatic extraction tuning occurs on dev documents; unseen held-out documents are processed by the *same frozen extraction policy* before final test answers.
- Choose the best non-graph comparator using only dev evidence; no cherry-picking a weak baseline or changing thresholds after looking at test results.
- If public corpus memorization is plausible, run closed-book B-1. Closed-book success is a **diagnostic**, not proof that a retriever is unnecessary on novel future corpora.

### 5.4 Systems to compare

| ID | System | What it tests | Typical pitfall |
|---|---|---|---|
| B-1 | Closed-book LLM | Recall without retrieved evidence | May memorize public pages; answer still lacks fresh provenance |
| R0 | FTS5/BM25 lexical retrieval | Cheap keyword control | Paraphrases may not match |
| R1 | Hybrid lexical + dense, metadata, reranker | Strong baseline RAG | Poor ranking/chunk boundaries |
| R2 | Iterative/query-decomposed retrieval | Adaptive multi-step search | More calls and latency |
| R3 | Explicit hyperlink / task-link expansion | Available “free graph” from source links | Raw links may already solve chain questions |
| R4 | Long-context documents | Does the small corpus need a retriever? | Price/token budget and context effects |
| R5 | Structured evidence table + SQL | Does normal relational modeling suffice? | Hand-curated structure may add value independent of DB type |
| R6a | **Human-checked** relationship-guided retrieval | Upper-bound value of representation | Not representative of extraction cost or errors |
| R6b | **Automatically extracted** relationship-guided retrieval | Realistic benefit after extraction noise | Unsupported edges, error amplification |

Use one common answer-generation interface, fixed answer schema, controlled settings, versioned prompts and measured context budgets. Embedding and reranker variants are tuned on dev questions only. **R5 and R6a must use comparable underlying curated fact sets** to isolate the value of traversal versus the value of having structured facts. Optional SQLite-versus-Neo4j comparison must hold the *same edges and query semantics* constant.

### 5.5 Outcome metrics and their interpretation

| Metric | Definition / method | Why it matters |
|---|---|---|
| **Complete evidence-set success** (primary) | For a question, did retrieved material contain **at least one** minimum sufficient evidence combination? Calculate proportion across questions; report class breakdown. | Directly measures the hypothesized evidence-chain advantage |
| Evidence-item recall | Required source-supported items retrieved / required items, allowing documented alternative sufficient sets | Diagnoses partial chain recovery |
| Claim-level support / entailment | Human reviewer checks each generated claim against cited spans and qualifiers; sampled LLM judges are secondary | A citation existing is not proof its claim is supported |
| Mechanism distinction accuracy | Reviewed case labels and prohibited conflations; report errors by system layer | Prevents false analogies |
| Temporal/status fidelity | Correct “as of” handling, source revision, proposed/completed/observed distinctions | Avoids false currentness or efficacy claims |
| Unsupported causal/generalization rate | Count claims exceeding evidence (e.g., a merged change *proved* prevention) | Measures dangerous overstatement |
| Abstention quality | Correct non-answers vs missed answerable cases | Enables safe evidence boundaries |
| Retrieval/answer latency | End-to-end median and p95 with sample size and environment | Operational feasibility |
| Token/API/compute cost | Indexing/extraction separate from per-query cost; show local hardware and provider pricing assumptions | Avoids “free inference” illusion |
| Human annotation cost | Minutes per document/edge/question, including adjudication | Graph curation can dominate project cost |
| Reproducibility | Runs reconstructable from source snapshot, code, cache/model settings | Essential for portfolio credibility |

**Evaluation rules:** For each claim-support judgment, check *meaning*, not only a substring match or citation URL. Report numerator/denominator, number of test questions, reviewer identity/qualification, uncertainty and conflicting judgments. With a small test set, show raw paired wins/losses and uncertainty intervals where feasible; do **not** assert statistically significant generalization without sufficient data. A 40-question pilot is informative, not a universal accuracy estimate. If no domain expert reviews the labels, say **researcher-annotated documentary benchmark**, not **expert-validated**.

### 5.6 Data and experiment reproducibility

Every run captures: commit/tag, source manifest hash, eligibility/rights manifest version, parser/chunker version, index/embedding/reranker version, gold split hashes, retrieval settings, model identifier and observed provider version where available, prompts, random settings, context token count, outputs, evidence IDs, cost and latency. Include a **redacted**, reproducible config; never commit secrets, private tokens or potentially restricted raw content. Cache replay tests logic, but it is not proof that a live external provider returns identical output months later.

## 6. Execution discipline: VS Code, Copilot Student and GitHub

**The developer is the final reviewer.** Copilot is an implementation assistant, not the source of truth about licenses, graph improvement, benchmark answers or production safety.

### 6.1 Required working loop — repeated for every task

1. **Open a single GitHub issue** (`P<n>-T<n>`) with its bounded objective, allowed file scope, inputs, explicit acceptance tests and out-of-scope work.
2. **Start from last green commit** on `main` and a dedicated short-lived branch. Confirm the correct repo/environment and corpus/benchmark versions.
3. **Give Copilot exactly this issue** (plus relevant interfaces and nearby tests), asking for a narrow patch, tests and a brief list of assumptions. Do not ask it to implement an entire future phase.
4. **Review the diff and assumptions** before accepting changes. Reject unrelated refactors, new services, unpinned dependencies and generated claims about corpus facts without citations.
5. **Run the smallest relevant tests first**, then format/type checks, all tests and any source/cost safety checks implicated by the change. Review retrieval outputs against primary evidence when applicable.
6. **Fix, retest and document** any non-obvious failure. Do not accept “tests passed” from the agent without executing them yourself or seeing trustworthy CI logs.
7. **Commit the scoped change**, write a short evidence-bearing PR description (even if self-reviewed), merge only when green, update `docs/STATUS.md` and the corresponding gate checklist. One completed task is a small verified artifact, not a large chat transcript.
8. **Begin the next dependent task only after this one passes.** A phase closes only when every gate item has a checkable artifact.

**Copilot prompt frame (for each active task, not a massive prompt pack):**

```text
ROLE: Implementer working on ReliabilityGraph, phase P#, task T#.
SOURCE OF TRUTH: docs/PLAN.md, docs/corpus/CORPUS_SPECIFICATION.md,
                docs/STATUS.md, and the named interface/tests.
GOAL: <one small deliverable>
ALLOWED FILES: <specific files or directory>
INPUTS & CONSTRAINTS: <frozen snapshot, rights, cost, API contracts>
ACCEPTANCE: <test commands and expected observable behavior>
OUT OF SCOPE: <no extra dependencies, no unrelated changes, no next task>
Please explain any uncertainty, make the smallest correct patch,
add/update targeted tests, and provide exact validation commands.
Do not assert successful tests, verified sources or benchmark gains without evidence.
```

### 6.2 Safeguards against vibe-coding failure modes

- **Scope creep:** cap each code task to one change type (e.g., one parser with fixtures); split an unexpectedly large task before implementation.
- **Context loss:** the canonical context is the repository (`PLAN`, `STATUS`, ADRs, task issue), not a growing chat transcript; maintain a compact “next action” note.
- **Hallucinated integrations:** confirm library/API signatures against pinned docs or running tests; Copilot-generated config is a proposal, not authority.
- **Agent loops:** stop after two unsuccessful fix cycles, run the failing command manually and reduce to a minimal reproducible case before another attempt.
- **Branch conflicts:** only one agent edits production files on the active branch; no parallel agents touching the same interfaces. Independent documentation/annotation work may happen separately.
- **Secrets:** never paste tokens into Copilot or issues; use environment placeholders, `.env.example`, GitHub Secrets and redacted logs.
- **Source evidence:** AI may help suggest page/section candidates, but a human checks and records source-backed claims. Do not let generated citation strings become gold labels.
- **Dependencies:** every package addition must justify its necessity, license, pinned version and maintenance implications.

### 6.3 What GitHub Copilot Student does **not** guarantee

GitHub's [Copilot Student docs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-students) describe student access, but model/agent availability and usage limits can change and require verification inside the **actual account**. The historical/current plan pages have changed over 2026; this roadmap does **not** promise a specific model, quota, API key, cloud agent or free commercial provider inference. **Copilot access in VS Code is not equivalent to an Anthropic API entitlement** for a separately deployed app.

Before P0 ends, check the actual editor/account entitlements and document them without personal credentials. If paid model inference is unavailable, preserve the ability to build/test the full retriever using deterministic fixtures, local embeddings and a clearly labeled offline demonstration. Do not open a paid API account just to satisfy an arbitrary dependency in the plan.

### 6.4 Session handoff and GitHub evidence

`docs/STATUS.md` always contains:

- active phase, gate and issue;
- last green commit/tag and exact validation commands/results;
- decisions, blockers and source/cost uncertainties;
- files/interfaces changed and any unreviewed changes;
- next **single** task and its prerequisites;
- what can be done safely in parallel while Copilot works.

A small [Architecture Decision Record](https://adr.github.io/) (`docs/adr/NNN-*.md`) records material choices: motivation, alternatives, evidence, consequences and triggers to revisit. GitHub issue/PR templates enforce the task scope and verification record. Continuous integration runs tests and checks on every relevant PR and on protected `main` where supported.

## 7. Productive parallel work without violating sequential verification

**Principle:** the code dependency chain remains sequential. Only tasks that do not modify the active task's assumptions or files may proceed during Copilot generation/review.

| When Copilot is working on... | Safe independent human work | Must **not** start yet |
|---|---|---|
| P0 tests/wrapper | Read source policies; draft issue labels/README structure | Build the P1 fetcher against an unfinished interface |
| P1 acquisition/parser | Inspect candidate incident pages; log status/rights/link leads | Annotate definitive gold spans from mutable content |
| P2 schema/harness | Read reports and draft proposed questions in a **non-gold** scratchpad; assess reviewer availability | Add answer-derived graph edges or tune retrievers on test questions |
| P3 index/retrieval | Manually audit the frozen source titles/sections; check UI copy | Deploy a not-yet-verified API |
| P4 deploy | Draft attribution and limitations; check actual host quotas and terms | Run P5 retrieval changes while P4 interfaces are unstable |
| P5 advanced baselines | Review latency/cost logs; organize error categories without seeing hidden test answers | Construct question-specific “oracle” edges |
| P6 curated relations | Verify unrelated documents; record annotation time | Start automated extraction before Gate G |
| P7 extractor | Review sampled evidence quotes, source claims, held-out document policy | Change final test labels or tune against them |
| P8 evaluation | Draft demo outline and README structure using placeholders | Change frozen systems after the test freeze |
| P9 release | Prepare video script, screenshots, issue cleanup and resume *template* | Publish invented metrics or unverified rights statements |

**Idle-time decision rule:** If the parallel work would change the active task's code, public corpus eligibility, graph labels for a held-out question, or final benchmark outcome, **do not do it in parallel**. Instead review primary sources, create documented future issues, write neutral documentation or inspect CI output.

## 8. Decision gates and pre-registered graph criteria

**All gate checks are backed by files/commands, not verbal assurances.** Record evidence in `docs/gates/<GATE>.md` (link CI run, artifact hash, screenshots when useful). A gate can return **PASS**, **REWORK**, **SIMPLIFY** or **STOP** where specified. Do not silently skip a failed gate to keep momentum.

### Gate G — Continue / Simplify / Stop (core decision)

**[P] Pre-register before dev evaluation** in `docs/decision-criteria.md`:

1. The strongest non-graph comparator is selected fairly from R1–R4 on the development split.
2. R6a (verified relations) is compared with that comparator **and** R5 (same facts, SQL) on genuine multi-document classes, under documented comparable evidence budget.
3. Primary metric is **complete evidence-set success**; secondary priorities are claim-support fidelity, mechanism/temporal mistakes, abstention, latency, total dollar/compute cost, and curation time.
4. Record a paired table per question (R6a win/tie/loss) and a cost/fidelity analysis. **Do not infer a winner from one cherry-picked demo.**
5. Require a **repeatable, practically meaningful** improvement across more than one question type, without an unacceptable increase in unsupported claims or curation burden. The chosen concrete effect threshold must be justified **before the relevant results are inspected**; no universal percentage is asserted here.

**Decision outcomes:**

| Outcome | Meaning | Next steps and honest portfolio claim |
|---|---|---|
| **CONTINUE** | Verified relation guidance has a defensible benefit over best non-graph and SQL controls | Attempt P7 automatic extraction; graph-backed retrieval is still provisional until extraction survives noise |
| **SIMPLIFY** | Structured evidence/SQL helps, but dedicated graph traversal does not materially beat it; or verified edges help but automation is not cost-effective | Prefer the simpler source/evidence-table solution; preserve graph experiment as ablation. Do **not** label the deployed winner as graph-powered if it isn't |
| **STOP graph thesis** | Iterative/hyperlink/long-context or SQL baseline essentially matches or beats relation guidance at lower cost, or evidence chains fail quality review | Ship an honest baseline-first incident evidence app + negative study, or run a **separately scoped** corpus revisit. Do not add Neo4j for résumé optics |
| **REWORK evidence** | Corpus/benchmark rights, source integrity or test-set validity fails | Fix the corpus/test protocol or stop; no final performance claims until a valid comparison exists |

**Gate X — extraction realism:** If R6a wins, run R6b on a frozen extraction method. Compare real extraction precision/recall on a separately reviewed sample and compare complete evidence retrieval against the same baseline. If extracted edges lose the benefit or require untenable curation, **SIMPLIFY**; a human-oracle win alone does not justify claiming scalable Graph RAG.

**Database-specific test:** If an actual graph database is considered later, compare same-edge retrieval quality, query complexity/maintainability, query latency and operational overhead against SQLite recursive queries. R6 outperforming vectors does **not** mean Neo4j beats SQL.

### Other gates at a glance

| Gate | Pass condition, summarized |
|---|---|
| **P0** | Clean setup and CI; mock/cached model adapter; no secrets; entitlements recorded; project controls work |
| **S** | Authorized, reproducible frozen snapshot; source manifest; rights decision; links and token stats; Phabricator unresolved/accepted decision |
| **Q** | Gold questions checked and anchored; diverse genuine cross-source tasks; frozen split; rubric and gate criteria committed |
| **B** | Baseline RAG reproducible on dev, citations trace, errors characterized; first cost figures measured |
| **D0** | Authorized/limited public demo, clean container, smoke tests, attribution and rollback tested |
| **N** | Strongest non-graph dev comparator named with reasons; parity recorded |
| **G** | Verified relation upper-bound comparison and explicit decision |
| **X** | Extracted relation quality and net retrieval value established, or simplified |
| **E** | Final frozen test outcomes and error analysis reproducible; no post-test tuning |
| **R** | README, deployment, rights/security checks, video and honest release metrics verified |

## 9. Sequential phase-by-phase roadmap

**All estimates here are rough planning placeholders, not commitments.** The original draft estimates approximately **126 hours through release without P7** or **140 hours with P7**, excluding any scope changes, external reviews and P10. **[U]** Real effort cannot be known before P1 measurements; manual gold annotation and evidence review are likely high-variance tasks. Do not rush a gate to match the estimates.

| Phase | Focus | Checkpoint | Hard dependency | Why it is in this order |
|---|---|---|---|---|
| **P0** | Repo and guarded workflow | P0 | None | Establish safe reproducible work |
| **P1** | Source acquisition, rights, snapshot | S | P0 | Validate real corpus before designing on it |
| **P2** | Gold evidence and benchmark contract | Q | S | Define correctness before tuning |
| **P3** | Closed-book and strong basic retrieval | B | Q | First real control system |
| **P4** | Public baseline demo | D0 | B | De-risk shipping early |
| **P5** | Strong non-graph alternatives | N | D0 | Give graph a meaningful competitor |
| **P6** | Checked relations and SQL comparison | G | N | Test *whether* structure helps |
| **P7** | Auto-extracted relations, conditional | X | G = CONTINUE | Test whether benefit survives extraction |
| **P8** | Frozen final evaluation | E | G / X | Measure without test-set tuning |
| **P9** | Release, hardening, README and demo | R | E | Finish a portfolio artifact |
| **P10a/b** | Optional graph DB ablation / cross-provider extension | Separate | R, rights gates | Enhancements must never block v1.0 |

**Task granularity:** Every phase consists of individually scoped **P#-T# issues**. The lists below specify delivery units; make an issue for each, complete/verify/commit it, then advance. Do not ask Copilot to build several at once.

### Phase P0 — Foundation and guardrails (planning estimate ~6 h)

**Objective:** A repository that can accept future work safely, reproduce tests and record evidence. **No paid account is required to finish this phase.**

**Sequential tasks**

- **P0-T1:** Create repository structure, `README.md` placeholder, `docs/PLAN.md`, corpus dossier, `docs/STATUS.md`, and minimal issue/PR templates; add provenance/licensing placeholder. Check that no raw content of uncertain rights has been committed.
- **P0-T2:** Pin Python version/dependencies; configure `uv`, `ruff`, tests, type checks, gitignore, environment sample and local commands (`make verify` *or* documented cross-platform equivalent).
- **P0-T3:** Implement model/provider **interface with mock implementation** and record/replay response fixture. No real API call yet.
- **P0-T4:** Add local request/token accounting, configurable pre-call cap, mock exception and no-secret logging tests. Explain that application counters are *not* a substitute for provider-side spending controls.
- **P0-T5:** Configure GitHub CI for lint/type/test and lightweight secret checks; write `docs/gates/P0.md` with precise evidence.

**Verification:** Clean clone can install and run tests; mock calls hit no network; budget-exceeded fixture fails closed; `.env`/keys excluded; CI green; active Copilot Student features and independent inference options checked against user's account without copying credentials.

**Gate P0:** Everything above evidenced. **If unavailable credentials are the only blocker, do not stall:** continue using mock/local modes, record the limitation.

### Phase P1 — Authorized acquisition, corpus selection and frozen snapshot (estimate ~12 h) → Gate S

**Objective:** Establish what actually exists, can be used, and is worth indexing.

**Sequential tasks**

- **P1-T1:** Review and record the **current** Wikimedia access/robot terms, wiki licensing, and Phabricator-specific rights; choose permitted current-page fetch interface. Document user agent, pacing, retries and failure behavior.
- **P1-T2:** Select a small, mixed-family candidate list from W2; inspect sources manually and mark eligibility, draft/final status, event/publication context and inclusion reasons.
- **P1-T3:** Implement respectful current-page fetch to local storage; capture local hash, retrieved date and available revision identifiers. **Do not crawl old revisions or bulk-download external attachments.**
- **P1-T4:** Implement section parser plus evidence-span anchoring; unit-test on hand-reviewed pages, including missing dates, markup and drafts. Stable gold anchors must not depend on chunk size.
- **P1-T5:** Extract outbound links with typed target classes; resolve only permitted links. Attempt **one bounded, documented** verification of T172489/T253832 and the specific later report; set `verified`, `link-only` or `excluded` as appropriate.
- **P1-T6:** Produce corpus statistics (eligible docs, incident families, content tokens, sections, passages, links) and a rights/selection manifest; freeze the local snapshot.

**Verification:** Every included page resolves to an official source URL; manifest and local bytes match SHA-256; repeat indexing gives identical IDs from identical local bytes; section anchors verified against at least three sources and a manual sample of 10 passages; no disallowed material in the public repo; P1 networking complies with recorded access rules. If API fetch fails, a small approved manual snapshot may be valid *if its provenance and usage rights are documented*; do not mislabel it as an API success.

**Gate S:** Reproducible eligible local dataset; rights for intended public use documented; token and linking statistics known; unresolved task links explicitly excluded from asserted gold evidence. **Fail/REWORK** if all useful cross-record chains depend on material you cannot inspect or lawfully use.

### Phase P2 — Evidence schema, gold benchmark and harness (estimate ~22 h) → Gate Q

**Objective:** Define what evidence correctness means **before** results can bias annotations.

**Sequential tasks**

- **P2-T1:** Create typed source/span/claim/relation records and validators from §4.2, with source-status, attribution and temporal fields.
- **P2-T2:** Write annotation guide: how to identify minimal evidence, document-qualified causal language, false analogy, action state and abstention.
- **P2-T3:** Curate natural questions from reviewed source cases; annotate minimal source sets **without** looking at retrieval outputs. Mark hypothetical questions separately and exclude until supported.
- **P2-T4:** Freeze incident-family-aware dev/test partitions, question/evidence hashes and reviewer notes; manually confirm the multi-source count and absence of one-document shortcuts.
- **P2-T5:** Implement gold validator, scoring utilities, evidence-set evaluator, and run artifact writer. Check metrics on hand-calculated toy fixtures and deliberately failing examples.
- **P2-T6:** Pre-register decision priorities, limits, ablations and Gate G rules in `docs/decision-criteria.md` **before retrieval tuning**.

**Verification:** All gold anchors resolve; no source-labeled R/U evidence is treated as verified; each question lists intended source set and unacceptable inferences; answerability and evidence-set counts are reviewed; toy oracle scores as expected while empty/random baselines do not; gold/test set is hash-frozen and committed through reviewed PRs.

**Gate Q:** Sufficient genuine, non-artificial multi-source tasks (target ≥12–15), at least several negative/false-analogy cases, valid split, rubrics and preregistration. **If this fails:** a limited Wikitech expansion can be a separate P1/P2 revision; if still unsupported, record a **corpus rejection/pivot** rather than forcing graph queries.

### Phase P3 — Baseline RAG core (estimate ~14 h) → Gate B

**Objective:** Deliver a credible non-graph system and first measured development results.

**Sequential tasks**

- **P3-T1:** Build read-only SQLite index (FTS5, sources/spans/link tables) from frozen local snapshot; verify hash/rebuild determinism.
- **P3-T2:** Add lexical R0 and closed-book B-1 diagnostic; produce structured evidence trace even for no-answer cases.
- **P3-T3:** Implement cached local embeddings and exact dense top-k; compare a small number of embedding choices **on dev only**, recording hardware and model versions.
- **P3-T4:** Add a reranker and metadata/date/status filters to define strong hybrid R1; test constraints and score ordering.
- **P3-T5:** Implement one answer generator with strict claim/evidence structure and abstention; use mock mode for CI. **Do not claim quote-match validates semantic support.**
- **P3-T6:** Validate citation IDs/quote existence automatically, then manually assess sampled claim entailment; run dev benchmark with full latency/cost tracing.

**Verification:** R0/R1 output only indexed evidence spans; fabricated citation and quote tests fail; no model output is considered verified merely because it references an actual URL; caching/replay works from frozen fixtures; clean-checkout run reproduces deterministic retrieval artifacts and publishes actual measured dev scores.

**Gate B:** A functioning control arm with sourced answers, explicit failures and measured costs; dev results committed and repeatable. R1 is the reference baseline (not presumed best against later R2–R4).

### Phase P4 — Ship a protected baseline demonstration (estimate ~8 h) → Gate D0

**Objective:** Prove early that a small version can be deployed and shown, independent of graph success.

**Sequential tasks**

- **P4-T1:** Define and test FastAPI `/ask`, `/health` and safe `/trace/{id}` contracts, including errors, bounds and non-leakage of raw provider traces.
- **P4-T2:** Build one minimal UI displaying answer, per-claim evidence links, event/source dates, document status, uncertainty and attribution; no decorative network visualizations.
- **P4-T3:** Build immutable, read-only container with eligible snapshot/index or approved rebuild path; verify source-rights requirements of bundled text before publishing.
- **P4-T4:** Select a host after current price/free-tier review; add strict input size caps, concurrency/rate limits, per-request budget, provider-side spend cap if available, and an emergency disable route.
- **P4-T5:** Run clean-clone container smoke tests and *actual deployed* smoke tests; rehearse rollback and capture measured p95/median where sample permits.

**Verification:** Unknown queries abstain rather than invent; test inputs cannot inject system instructions from corpus content; trace endpoint exposes only safe redacted provenance; app returns usable citations; secrets absent from image/logs; costs/rate-limit behavior tested; attribution and safe-use notice visible.

**Gate D0:** Live URL **only if** operational costs, rights and abuse controls are acceptable. If external inference is unavailable, an honest public **read-only prerecorded-evidence demo** can satisfy early portfolio hosting while the live question endpoint remains restricted; record this as a **limited** D0, not a full live RAG deployment.

### Phase P5 — Strong non-graph competitors (estimate ~16 h) → Gate N

**Objective:** Avoid an unfair comparison where the graph wins against weak vector-only search.

**Sequential tasks**

- **P5-T1:** R2 decomposed/iterative retrieval with bounded passes, calls and tokens; deterministic safety limits.
- **P5-T2:** R3 Wikitech hyperlink expansion: source link -> permitted source -> supporting passage, with hop budget and cycle checks.
- **P5-T3:** R4 long-context reference with explicit corpus token accounting. If full set cannot fit or costs are unacceptable, use a stated bounded strategy instead of claiming full-context parity.
- **P5-T4:** Normalize query budget, generator prompt/version, evidence format and attribution across systems; write a comparison harness and test equality where relevant.
- **P5-T5:** Run dev comparisons; measure cost/latency including extra retrieval rounds; publish the strongest non-graph result and its failures.

**Verification:** R3 never follows arbitrary external links or opens disallowed sources; R2 enforces hard iteration cap; context-size logs match actual prompt assembly; results use the same corpus/gold split and are stored immutably.

**Gate N:** Strongest non-graph comparator identified from the development split, cost/fidelity included. If it achieves essentially complete dev evidence recovery, graph justification is already doubtful; still document the R6a *upper-bound* pilot if annotation cost remains acceptable, otherwise record a stop decision before excessive work.

### Phase P6 — Verified relationship upper-bound and SQL control (estimate ~14 h implementation plus ~10 h curation **[high uncertainty]**) → Gate G

**Objective:** Separate the value of *having verified relations* from the value of *traversing them as a graph*.

**Sequential tasks**

- **P6-T1:** Annotate claims/relations across the entire approved pilot according to one stable guideline, **per document rather than per benchmark question**. Log person-minutes and uncertain judgments.
- **P6-T2:** Load typed relations into the existing evidence tables, enforce evidence IDs, preserve unsupported/inferred status and check for contradictions.
- **P6-T3:** Implement R5 SQL evidence-table retrieval on the same facts, using bounded, parameterized queries.
- **P6-T4:** Implement R6a limited relation-guided expansion and path-to-prose rendering; every traversed claim/edge must lead back to original evidence.
- **P6-T5:** Run paired dev comparisons against best non-graph and R5, including false-analogy and temporal controls; record relation-curation effort and a readable win/tie/loss report.
- **P6-T6:** Write Gate G ADR: **CONTINUE**, **SIMPLIFY**, **STOP**, or **REWORK**, supported by preregistered criteria.

**Verification:** Every edge references inspected primary evidence; graph-generated relationships are not silently called source-stated; no unqualified `CAUSED` edge; same-facts SQL comparison works; manually re-annotate a subset on another day and report agreement or disagreement without pretending it is independent expert review; traversal bounded in depth and output budget.

**Gate G:** Explicit project path selected (§8). **If the main gain is simply better annotation, don't attribute it to Neo4j or graph traversal.**

### Phase P7 — Automatic relation extraction **only if Gate G = CONTINUE** (estimate ~14 h) → Gate X

**Objective:** Determine if a practical, repeatable relation layer can be made without manually constructing the answer graph.

**Sequential tasks**

- **P7-T1:** Choose a small bounded ontology from observed source patterns; implement schema-constrained extraction prompt(s) with an attribution/evidence-quote requirement and a low-cost model adapter if viable.
- **P7-T2:** Add deterministic quote matching, entity alias normalization, uncertainty/status preservation and duplicate/retry/idempotence handling; source-hash-based cache keys.
- **P7-T3:** Compare extracted claims/edges against reviewed annotations; report per-type precision/recall, unsupported-edge rate, and annotation time.
- **P7-T4:** Implement R6b using extracted relations; score dev questions, comparing R6a, R5 and best non-graph at controlled budgets.
- **P7-T5:** Document extraction/indexing costs and holdout behavior; record Gate X decision.

**Verification:** Intentionally false quoted edges rejected; malformed model JSON cannot enter storage; reindexing same snapshot is idempotent; spot-check sampled edges with recorded support; no held-out label-based prompt tweaks; extraction logs and cached fixtures are reproducible.

**Gate X:** Continue relationship-guided retrieval only when **the automatically extracted version** shows practical value after error and curation costs. Otherwise **SIMPLIFY** to the best honest architecture. A guided manually curated mode can be retained as a *research upper bound* with an explicit label, not advertised as scalable automatic Graph RAG.

### Phase P8 — Frozen final evaluation (estimate ~12 h) → Gate E

**Objective:** Create the numerical evidence that a recruiter can inspect, not a marketing claim.

**Sequential tasks**

- **P8-T1:** Freeze baseline and candidate commits, model/configs, corpus snapshot, extraction method, test split and judge rubric.
- **P8-T2:** Run the untouched test split once as pre-registered (with predeclared repeats for stochastic generation), capturing evidence IDs, answers, timing/cost and errors.
- **P8-T3:** Run preplanned ablations: no graph edges, verified vs extracted relations when relevant, with/without hyperlinks, metadata filters and rerankers; only comparisons that fit the approved hypothesis are required.
- **P8-T4:** Conduct manual claim-support/false-analogy audit, calibrate any LLM judge against human labels and disclose disagreement; classify failures.
- **P8-T5:** Generate result tables/charts entirely from immutable run artifacts; compare value, latency and annotation/indexing costs; write `docs/results.md` and final architecture ADR.

**Verification:** `make reproduce-results` (or documented command) regenerates published results from committed permitted artifacts; test configuration unchanged; unsupported claims flagged rather than cleaned out after the fact; all comparisons explicitly state counts and uncertainties.

**Gate E:** Honest repeatable final evaluation, failure cases, caveats and declared winner/decision. **Optional original-guide ambition:** if source quality makes it feasible, grow to ~50–100 naturally valid benchmark items and report stratification; never pad the set with fabricated multi-hop questions to reach a number.

### Phase P9 — Hardening, portfolio release and handoff (estimate ~12 h) → Gate R

**Objective:** Ship a dependable v1.0 and a resume claim tied directly to measurements.

**Sequential tasks**

- **P9-T1:** Integrate the chosen retrieval strategy into the deployed interface; remove abandoned experimental pathways from public routes while keeping benchmark scripts archived.
- **P9-T2:** Execute §11 security, licensing, accessibility and cost checks; verify deployment recovery, input limits, citation panel and error states.
- **P9-T3:** Write README with **live demonstration and measured results first**; present corpus scope, baselines, reproducibility, diagram and limitations next.
- **P9-T4:** Record short (~90-second target from original portfolio guide) walkthrough, with real working answers, evidence view, one failure example and observed benchmark comparisons.
- **P9-T5:** Release `v1.0`, publish a clean-clone reproduction guide and clearly scoped resume bullets, confirm active demo URL and links.

**Verification:** Every README metric is machine-derived from run artifacts; clean clone works without developer secrets; example queries resolve to source-linked passages; release includes rights/attribution report, security checks and honest limitations; rollback rehearsed.

**Gate R:** Full §12 release checklist checked and linked to evidence. No unvalidated benchmark improvement, expert review or cloud uptime claim is advertised.

### Phase P10 — Optional research extensions (never block v1.0)

**P10a — Dedicated graph store ablation:** only if it answers an actual research or learning question. Project the **same permitted, reviewed relation set** into Neo4j or another graph DB; use parameterized read-only query templates (no model-produced raw Cypher) and compare identical source-grounded results with SQLite/SQL on latency, path expansion, complexity and operations. Release as a clearly labeled ablation, not a retroactive justification for Graph RAG.

**P10b — Cross-provider reliability generalization, gates X1–X4:**

- **X1 (rights/acquisition):** verify GitHub/Cloudflare/Google Cloud source terms and build an official URL registry; choose a modest number of first-party detailed reports, not status-only fragments.
- **X2 (normalization):** define provider-aware event, publication, symptom, cause and mitigation labels; preserve different reporting granularity and do not force all sources into one simplistic cause ontology.
- **X3 (independent evidence):** create new, genuine cross-provider question/evidence chains; test whether relationship patterns generalize beyond Wikimedia wording, links and incident conventions.
- **X4 (cost and release):** rerun the winning baseline and relationship method on the **same** expanded corpus; report both gains and regressions, rights and incremental maintenance costs; only then promote the expansion to a public release.

**No automatic P10 expansion** if P6/G says relations are not useful, unless a separately documented experiment explicitly hypothesizes why the new source family would change that answer.

## 10. Cost, scheduling, and failure-response safeguards

### 10.1 Budget policy

- **Before paid inference:** confirm a provider account, spending/billing controls, rate limits, model names and current prices from official documentation; record the **as-checked date**. VS Code/GitHub Copilot access is a coding subscription, not application inference credit.
- **At development time:** set a *user-chosen* experiment budget; use cached runs, tiny subsets first, token estimates, prompt truncation and an application-side call/expense ceiling; configure provider-side spending controls where available. Do not state a fictional “free tier.”
- **At query time:** bound prompt length, retrieved evidence, retrieval rounds, concurrent calls, model max output and total per-request spend. If budget is unavailable, fail closed with a clear error/queued-offline option, not an uncapped provider call.
- **Indexing:** record document count, extraction calls, token use, embedding work and actual human review time separately. Cost per online answer must not hide the one-time source preparation cost.
- **Hosting:** document CPU/RAM, cold-start behavior, paid versus free limitations, storage persistence, scale-to-zero sleep/capacity behavior, egress and cost alarms after provider selection.
- **Fallback:** if a hosted model cannot be funded sustainably, release a static recorded-question evaluator plus local CLI/optional inference instructions, accurately labeled. Do not call a canned-only demo an unrestricted live AI service.

### 10.2 Time estimates, contingency and pacing

The phase-hour estimates are **rough prioritization guides**; P1 access and rights, P2 human evidence labeling and P6 verification are most uncertain. Plan in small GitHub issues; log actual duration per task so remaining effort is updated from observed throughput. Never trade off corpus validity or test-set integrity to hit a schedule.

**When blocked:**

1. Stop making dependent code changes.
2. File a blocker issue with exact failing command/request, timestamp, permissions and impact.
3. Try a bounded, permitted alternative (local sample, approved export, smaller model, same API with documented requirements).
4. Decide within the current phase whether to **rework, exclude, simplify or pivot**.
5. Update `STATUS`, ADR and gate; only then resume.

**When Copilot fails:** isolate a minimal repro, preserve failing fixtures, switch from feature-generation to tests/diagnosis, and reject broad speculative rewrites. A half-built branch is never merged into `main` merely to unblock another task.

### 10.3 Failure paths and portfolio integrity

| Failure | Evidence-based response | Portfolio outcome |
|---|---|---|
| Wikitech data inaccessible or rights unclear | Smaller permitted snapshot, exclude dubious tasks, record access failure | Still possible to demonstrate baseline on rights-checked public pages |
| Fewer than useful multi-document questions | Inspect broader incident families once; then reconsider corpus | A valid rejected-corpus decision, not a forced graph benchmark |
| Long-context/iterative retrieval wins | Keep simpler method; explain why | A rigorous retrieval evaluation project, not a graph-win claim |
| R6a wins but R6b fails | Report extraction bottleneck, human curation cost; simplify | Clear learning about graph representation versus automation |
| SQL over same facts matches traversal | Do not attribute improvements to Neo4j | Source-grounded structured RAG / knowledge representation result |
| Model provider unaffordable | Mock/local answerer for tests, restricted/live demo or static labeled showcase | Reproducible repo; be honest about inference limitations |
| Public demonstration rights fail | Source links, small attributed excerpts if allowed, private snapshots, reproducible permitted fetch | Respect licensing instead of redistributing unknown text |
| Domain expert unavailable | Researcher-annotated corpus with admitted uncertainty | Do not claim expert-validation |

## 11. Security, privacy, reliability and source-use checklist

**Before P4 D0 and again at P9 R, verify and record each relevant item.** Source pages and model outputs are **untrusted data** even when the page is first-party and publicly hosted.

### Input and prompt-injection defense

- [ ] Corpus text is treated as evidence, never as an instruction to the model or an executable command.
- [ ] Retrieval snippets are clearly delimited, attributed and not inserted into privileged instruction fields.
- [ ] User question length, token counts and parameters are bounded; unknown/invalid filters rejected.
- [ ] No live infrastructure action, arbitrary file access, shell execution or unfettered URL fetch from user/model output.
- [ ] Web/UI renders evidence as escaped text; no untrusted HTML/JavaScript executes in browser or markdown widgets.
- [ ] Model-generated SQL/Cypher is **not executed directly**; only bounded parameterized read-only templates or validated query representations.
- [ ] Tests include adversarial source text (e.g., a report containing fake “assistant instructions”), oversized inputs, bad citations and malformed model JSON.

### Credentials, logging and resource control

- [ ] No API secrets in repo, screenshot, trace view, container layers, CI output or cached fixtures.
- [ ] Provider API secrets come from appropriate runtime secret management, not checked-in `.env`.
- [ ] Public `/trace` is redacted and scoped; no prompt internals, personal data, secret configuration or full restricted source dump.
- [ ] Rate limits, concurrency caps, input budgets, request timeouts, retries and circuit breaker/kill switch tested.
- [ ] Provider-side spend limits/alerts verified if offered; application-side cap treated as an extra guard only.
- [ ] Dependencies pinned, lockfile retained, software vulnerability/licensing checks considered for final release.
- [ ] Container runs as non-root where practical, exposes only necessary port, with read-only corpus/index and no write permissions it doesn't need.
- [ ] Deployment rollback works and public outage/error responses do not leak internals.

### Rights, attribution and responsible explanations

- [ ] Each included source has source URL, status, acquisition route, snapshot date/hash and documented reuse decision.
- [ ] Wikitech text attribution/share-alike obligations implemented where applicable; external embedded media not inherited under wiki text terms.
- [ ] Phabricator/task comments excluded or linked-only until permission/terms are established.
- [ ] Cross-provider texts not redistributed unless each publisher's applicable terms permit; default to link-backed evidence.
- [ ] Source pages or authors are not treated as infallible; attribution and uncertainty are visible.
- [ ] No claim that a dated recommendation was necessarily implemented, caused later success, or reflects current system behavior.
- [ ] No implied affiliation with Wikimedia, GitHub, Cloudflare, Google or Microsoft.
- [ ] Any user analytics/logs minimized; no personal responder profiling; public sample data contains only necessary technical evidence.

### Correctness and operational tests

- [ ] Citation IDs resolve to original frozen source spans, and visible URL points to the documented source.
- [ ] Verbatim substring validation and **semantic claim entailment review** are distinguished.
- [ ] Date/revision and draft/in-review status filters are enforced where requested.
- [ ] Response explicitly acknowledges when evidence cannot answer the question.
- [ ] Service smoke tests run against deployed endpoint with one supported case, one missing-evidence case and one injection/bounds case.

## 12. Final GitHub / deployment / resume release checklist

**Release `v1.0` only after every applicable item has checkable evidence.**

### Source and results

- [ ] Corpus selection, included/excluded sources, rights decisions and manifest hashes documented.
- [ ] README does not call R/U leads independently verified facts.
- [ ] Gold annotation protocol and class distribution published with source-safe anchors; if source text cannot be redistributed, a legal reconstruction procedure and sample excerpts are provided instead.
- [ ] Development/test split and data-leakage precautions explained.
- [ ] Strong baseline comparisons include non-graph methods, not merely weak vector RAG.
- [ ] Frozen test table reports question count, evidence retrieval, citation support, error types, latency, cost and uncertainty.
- [ ] Ablations and graph-versus-SQL attribution reported without overstating causal proof.
- [ ] Every displayed headline metric is generated by script from immutable run artifacts; no placeholder numbers remain.

### Software and public product

- [ ] Clean checkout installs, builds, runs tests and starts application using documented commands.
- [ ] CI green at release commit; version/license inventories and setup instructions current.
- [ ] Service handles answerable, unanswerable, out-of-scope and malicious-input demonstrations.
- [ ] Evidence panel opens original URLs and visibly distinguishes source facts from derived comparisons.
- [ ] Chosen service is deployed with working URL or the limitations of a static-only demo are prominently disclosed.
- [ ] Cost/rate/abuse controls exercised; secrets and restricted source content absent from public outputs.
- [ ] Source attribution and disclaimers visible; no implied operational authority.
- [ ] Rollback process and maintenance/staleness notes tested and documented.

### Portfolio and communication

- [ ] README above-the-fold order: **measured result → live demo/video → problem/use case → evaluation → architecture → reproducibility → limitations**.
- [ ] Architecture diagram reflects *deployed reality*, not an aspirational Neo4j diagram if Neo4j was rejected.
- [ ] ~90-second demonstration (or similarly concise walkthrough) shows: question, evidence links, a cross-document trace, comparison/benchmark and one limitation.
- [ ] One-page engineering decision narrative explains **why this corpus, why this retrieval approach, why the measured result matters**.
- [ ] Known failure cases, annotation caveats, rights limits and costs documented.
- [ ] Resume bullets use real numbers only and are factually bounded by corpus, benchmark and deployment scope.
- [ ] Final release tag, changelog, screenshots and GitHub milestones linked in README.

**Resume bullet template — replace every bracket before use:**

> Built and deployed an evidence-grounded retrieval application over **[N verified incident/source records]**; compared **[baseline names]** with **[chosen relationship-aware or simpler method]** on **[M source-annotated questions]**, achieving **[actual primary metric and delta, if any]** with **[measured latency/cost]** and source-level citations.

**If no graph improvement exists, do not say “improved RAG using a knowledge graph.”** Instead accurately report that you built and evaluated the graph and documented why a simpler retrieval design was selected.

## 13. GitHub structure, work artifacts and reproducibility

**Proposed structure, not a command to create every directory on day one:**

```text
reliabilitygraph/
├── README.md
├── LICENSE                        # license for YOUR code only
├── pyproject.toml
├── uv.lock
├── .env.example                   # placeholders, no keys
├── .github/
│   ├── workflows/verify.yml
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── copilot-instructions.md    # if supported by current product
├── src/reliabilitygraph/
│   ├── acquisition/               # P1
│   ├── evidence/                  # P2
│   ├── retrieval/                 # P3/P5/P6/P7
│   ├── models/                    # provider adapter / answerer
│   ├── api/                       # P4
│   └── eval/                      # P2 onward
├── tests/
├── eval/
│   ├── gold/                      # only items legal to redistribute
│   └── runs/                      # redacted and source-rights-checked artifacts
├── data/
│   ├── manifests/                 # versioned, safe to publish
│   ├── fixtures/                  # owned / permission-cleared small fixtures
│   └── local_snapshot/            # gitignored if rights uncertain
├── docs/
│   ├── PLAN.md
│   ├── STATUS.md
│   ├── corpus/
│   │   ├── CORPUS_SPECIFICATION.md
│   │   ├── selection.md
│   │   └── rights.md
│   ├── adr/
│   ├── gates/
│   ├── decision-criteria.md
│   ├── results.md
│   └── deploy.md
├── scripts/                        # build, eval, publish metrics
└── demo/                           # screenshot/video links and safe example queries
```

### Minimal issue template

```text
ID / phase / gate:
Task objective (one bounded outcome):
Source of truth / input artifacts:
Files/interfaces in scope:
Explicit out-of-scope work:
Acceptance tests and exact commands:
Relevant rights, costs, security constraints:
Estimated risk / blocker:
Completion evidence (commit, CI link, output hash):
```

### Minimal gate evidence template

```text
Gate ID, date and decision (PASS / REWORK / CONTINUE / SIMPLIFY / STOP):
Verified artifacts (commit, manifest hash, gold hash, logs):
Checks run and results:
Metrics used (with denominators and source provenance):
Unresolved issues and known limitations:
Architecture/next-phase consequences:
Reviewer and review scope:
```

### “Reproduce results” contract

A future reader with legal access to the sources and documented model/environment should be able to rebuild the allowed snapshot, regenerate indexes and inspect the *same recorded outputs*. Where live model determinism cannot be guaranteed, the repo provides cached response fixtures, source hashes, prompt/version metadata, evaluation tables produced from recorded runs, and clear limits on exact end-to-end replication. Never commit confidential credentials, questionable raw data or proprietary output merely to make a one-command reproduction look easy.

## 14. Mapping back to the original Project 1 brief

The user-provided BASWE.ai PDF's Project 1 describes five skills-oriented phases using Python, Neo4j, LangChain, a Claude API, pgvector and FastAPI. This roadmap **preserves the engineering objective and explains deliberate deviations** rather than claiming to implement that fixed reference stack verbatim.

| Original Project 1 expectation | ReliabilityGraph equivalent | Deliberate difference |
|---|---|---|
| 1. Extract entities/relationships into Neo4j | P2 claim/relation schema; P6 checked relations; P7 extraction if justified | Model relationships first; optional Neo4j ablation in P10 rather than mandatory deployment |
| 2. Vector index sharing evidence IDs | P1 stable spans, P3 FTS5 + dense search | SQLite/exact embeddings for small pilot; no premature HNSW/pgvector hosting |
| 3. Route questions to graph versus vector | Common Retriever interface R0–R6; optional query router after measured utility | A model-based router is **not** needed until distinct methods actually win on different question classes |
| 4. Merge graph paths/passages into cited answers | EvidenceSet → claim/evidence generation; provenance and entailment review | Source text remains authority; graph-derived claims not silently treated as source facts |
| 5. Compare with vector RAG on labeled questions | P2 gold, P3 RAG, P5 strong controls, P6/G and P8 evaluation | Include iterative/SQL/explicit links/long context; no assumed increasing gain by hop count |

**Optional routing experiment:** If both graph-guided and conventional retrieval survive P8 with complementary strengths, an additional classifier/router (factual versus relationship-comparison versus unknown) can be evaluated on **dev only**, using a deterministic fallback and logging decisions. Do not add an LLM router merely to check the PDF's Phase 3 box.

**Important portfolio distinction:** If the final system omits Neo4j, LangChain or pgvector, say explicitly that the user-facing *problem and experimentally tested capability* follow Project 1, while the stack was adapted for evidence and scale. If an interviewer expects hands-on Neo4j/Cypher, the optional P10a experiment can provide honest experience without forcing a production dependency.

## 15. Remaining assumptions and go/no-go questions

| Question | When it must be resolved | Responsible evidence | Stop condition |
|---|---|---|---|
| Is Wikitech acquisition allowed and reproducible at pilot scale? | P1/S | Policy links, request logs, frozen manifest | No permitted acquisition |
| Are task comments/attachments reusable? | P1/S | Phabricator-specific rights/access notes | Link-only or exclude; do not silently copy |
| Do ≥12–15 meaningful questions truly require multiple independent records? | P2/Q | Manually reviewed minimum evidence sets | No non-artificial cross-document test set |
| Can gold claims be grounded without private operations information? | P2/Q | Source-span review and unknown labels | Key conclusions unverifiable |
| Are model/provider credits and hosting safe within budget? | P0/P4 | Actual account and deploy checks | Must use capped or static/offline mode |
| Does iterative/hyperlink/SQL retrieval already suffice? | P5/N and P6/G | Matched dev comparisons | Stop or simplify graph path |
| Does automatic extraction preserve any gain? | P7/X | Edge quality, evidence recall, cost | No automated graph superiority claim |
| Can public release cite and show rights-checked evidence? | P4/P9 | Rights matrix and UI test | Limit public excerpts or source-link-only |
| Can published results be reproduced from permitted artifacts? | P8/E/P9/R | Locked sources/config, run logs, scripts | No benchmark performance claim |

## 16. Readiness conclusion and first action

**This revised roadmap is complete as a planning and execution framework**: phases, tasks, dependencies, verification, decision paths, parallel-safe work, security, release and references are now specified. It does **not** mean the corpus, graph advantage, legal rights, API usage or hosted infrastructure are already verified. Those are deliberately assigned to evidence gates.

**First action:** Create the GitHub repository, copy this file to `docs/PLAN.md` and the existing corpus dossier to `docs/corpus/CORPUS_SPECIFICATION.md`, create `docs/STATUS.md`, then open **P0-T1**. Do not ask Copilot to implement all phases simultaneously. Only after P0-T1 is verified should P0-T2 begin.

**Non-negotiable operating rule:** *No gate passes because an AI says it passed. A gate passes when a reproducible artifact, trustworthy log, source record or human review supports it.*

## 17. Sources and verification log

**Review date:** 4 November 2026. Public web pages may change. Links are official source entry points. This plan does not claim all entire repos or corpus/API endpoints have been downloaded or executed.

### Original project / supplied corpus

- **BASWE.ai, _Build These Six Projects_, Project 1: Knowledge Graph RAG for Enterprise Data.** User-supplied PDF; original five phases and portfolio expectations independently reviewed in this session. Source is user-provided, not an external link.
- **ReliabilityGraph — Corpus Specification, Source Dossier, and Selection Rationale**, provided in this conversation; source for Wikitech candidate list, V/R/P/U distinctions, corpus choice and unresolved task-chain details. Repository destination: `docs/corpus/CORPUS_SPECIFICATION.md`.
- **ReliabilityGraph: Project 1 Master Development Plan**, Claude v1.0 draft, 4 November 2026; baseline for the revisions documented in §18.

### Reference implementations and methodology

- **M1 — Microsoft GraphRAG repository:** https://github.com/microsoft/graphrag — code, research status, indexing cost warning and query method overview.
- **M2 — Microsoft GraphRAG indexing:** https://github.com/microsoft/graphrag/blob/main/docs/index/overview.md — text units, entities, relationships/claims, community summaries and embeddings.
- **M3 — Microsoft GraphRAG query approaches:** https://github.com/microsoft/graphrag/blob/main/docs/query/overview.md — local, global, DRIFT and basic retrieval.
- **M4 — HippoRAG (NeurIPS 2024 paper):** https://papers.nips.cc/paper_files/paper/2024/hash/6ddc001d07ca4f319af96a3024f6dbd1-Abstract-Conference.html — knowledge graph + Personalized PageRank retrieval and multi-hop evaluation, as reported by its authors.
- **M5 — HippoRAG public implementation:** https://github.com/OSU-NLP-Group/HippoRAG — reference code and subsequent HippoRAG 2 memory approach.
- **M6 — LightRAG public implementation:** https://github.com/HKUDS/LightRAG — graph/vector retrieval, incremental knowledge management and citations; implementation evolves, so pin versions if using it.
- **M7 — Google SRE incident/postmortem practices:** https://sre.google/ — engineering-method reference, not a replacement for independent incident evidence.

### Corpus operations and policy

- **W1 — Wikitech incident-review evidence:** https://wikitech.wikimedia.org/wiki/Incident_review_ritual — the operator's own description of incident-document quality and rediscovery problems.
- **W2 — Original 2017 read-only incident:** https://wikitech.wikimedia.org/wiki/Incidents/2017-07-28_s5_%28WikiData_and_dewiki%29_read-only — first-party source for the starter failure mechanism and T172489 reference.
- **W3 — Wikimedia Robot policy:** https://wikitech.wikimedia.org/wiki/Robot_policy — current-page crawling, API and other-resource access constraints; rules should be checked again before P1.
- **W4 — Wikimedia API access policy:** https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy — client identity, rate limits and varying reuse terms.
- **W5 — MediaWiki REST policy:** https://www.mediawiki.org/wiki/API:REST_API/Policies — API usage and attribution guidance; versioning may change.
- **C1 — GitHub Copilot Student account setup:** https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-students — eligibility and activation; plan limits/features are account-dependent and subject to change.
- **C2 — GitHub Copilot plan summary:** https://docs.github.com/en/copilot/get-started/plans — review actual plan and account state before assuming models, credits or third-party agent access.

### Source-provenance notes

- Wikimedia's Robot policy warns against historical-revision URL crawling; **this directly changed P1 from the original “revision-pinned API fetching” concept to frozen, locally hashed snapshots of permitted current pages**.
- Microsoft GraphRAG's documentation indicates a much heavier indexing/global-summary pipeline than this pilot needs. Its public repository describes its research maintenance posture as of this review; this may change later.
- HippoRAG and LightRAG provide *examples of graph-guided retrieval* with differing methods, but their reported gains are **not** assumed to transfer to reliability incidents.
- GitHub's Copilot documentation and offerings can shift; no specific Copilot Student model allowance or separate API credit is assumed in this plan.

## 18. Revision audit: v1.0 draft → v2.0 final

| Issue in original Claude draft | Final correction | Where |
|---|---|---|
| Missing §7, §8, §9 | Complete parallel-work, gate criteria and security/release sections | §§7–12 |
| P10 cross-provider X1–X4 left unfinished | Four explicit optional expansion gates, required evidence and stop rules | P10b |
| Source fetch assumed historical revision pinning | Policy-aware current-page fetch + frozen local snapshot, revision/hash metadata, no revision crawling | §2.2, P1 |
| Copilot usage mentioned but not operationalized | One-issue/one-patch/one-verification loop, prompt skeleton, failure recovery and session handoff | §6 |
| Parallel productivity promised without concrete safe tasks | Phase-specific independent tasks and explicit unsafe concurrency | §7 |
| Graph decision vague | Pre-registered practical metric, comparison with R5 SQL, Continue/Simplify/Stop/REWORK consequences | §§5, 8 |
| Gold benchmark risked contamination | Incident-family splitting, source anchors, held-out test, same-source fairness and annotator boundaries | §5 |
| Quote/citation existence might be mistaken for factual support | Separate deterministic checks from human semantic entailment, uncertainty and false analogy scoring | §§5.5, 11 |
| Paid Anthropic API prerequisite was assumed | Provider-agnostic mock-first P0, explicit Copilot-versus-API distinction, budget gates | §§4, 6, 10 |
| Security, rights, and public hosting checklists absent | Source/use and injection policies, deployment abuse controls, release gates | §§10–12 |
| Project 1 fixed stack versus no-overengineering was implicit | Explicit five-phase mapping and honest optional Neo4j/Cypher skills | §14 |
| Popular graph methods not assessed | Primary-source comparison of Microsoft GraphRAG, HippoRAG, LightRAG and SRE practice | §3, §17 |
| Effort and portfolio claims loosely expressed | Estimates as nonbinding, measured-only README and resume checklist | §§9, 10, 12 |

**Final audit:** All cited internal section numbers resolve within this document, all phases have explicit deliverables/gates or defined conditional applicability, and all external unknowns remain named rather than implied resolved. The plan is **execution-ready at P0**, **not** a claim that subsequent gates have passed.
