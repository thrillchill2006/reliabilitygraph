# ReliabilityGraph — Corpus Specification, Source Dossier, and Selection Rationale

> **A source-grounded, GitHub-ready reference document for the proposed Knowledge Graph RAG portfolio project.**
>
> **Prepared:** 4 November 2026  
> **Decision status:** **Selected for corpus-validation pilot; graph-based architecture is conditional, not yet validated.**  
> **Recommended repository location:** `docs/corpus/CORPUS_SPECIFICATION.md`  
> **Working project name:** **ReliabilityGraph** — Evidence-Grounded Incident Intelligence for Distributed Systems  
> **Primary corpus:** Wikimedia's public Wikitech incident reports and operations documentation.  
> **Conditional expansion:** First-party availability and incident reports from GitHub, Cloudflare, and Google Cloud.

---

## 1. Executive decision

### 1.1 What has been selected

**Domain:** software and cloud reliability engineering, particularly production incidents and the relationship between failure symptoms, technical mechanisms, affected dependencies, detection, response, and documented follow-up actions.

**Problem:** engineers learning from historical outages must often assemble evidence from separate incident reports, operational guides, and change or follow-up records. A question may begin with a symptom—such as a service accepting connections but not allowing writes—rather than the identifier of the incident that explains it. The useful answer must identify relevant failures, distinguish their mechanisms, and trace actions to *actual supporting documents* without claiming that a proposed or completed task has necessarily eliminated the problem.

**Primary research collection:** Wikimedia's public [Wikitech](https://wikitech.wikimedia.org/) engineering materials, beginning with a **small, deliberately curated collection of incident reports, runbooks, and eligible corrective-action references**. The pilot is intentionally narrow enough to permit careful validation.

**Optional generalization collection:** detailed postmortems from **GitHub, Cloudflare, and Google Cloud**, added only after the initial evidence-retrieval hypothesis survives meaningful testing and relevant reuse conditions have been assessed.

**Intended users:** backend engineers, site reliability engineers (SREs), platform engineers, AI-infrastructure engineers, and students of production system design. This is a **retrospective learning and research assistant**—not a live incident-response agent or an authoritative operational decision-maker.

### 1.2 What is not yet established

The following are **not** completed achievements:

- A downloaded, licensed and curated final corpus of any predetermined size.
- A validated set of 40, 50 or 100 gold-standard benchmark questions.
- Successful automated acquisition of Wikitech via its API.
- Unrestricted reuse of Phabricator task comments or of all commercial providers' report text.
- A demonstrated gain from graph-guided retrieval over iterative/vector/hyperlink-based retrieval.
- A justification for Neo4j, or for any particular graph database, over a relational evidence store.
- A deployed application, production-grade retrieval accuracy, or measured time savings.

**Decision:** select the *problem and initial source ecosystem* now. Defer irreversible architectural choices and broad corpus expansion until evidence justifies them.

### 1.3 Why this project fits the original goal

Your project goal is a meaningful, publicly demonstrated **Knowledge Graph RAG for Enterprise Data** portfolio project that can support a GitHub repository and technical interviews. Your additional conditions are that the domain teaches useful long-term engineering knowledge and that a graph must not be included merely to make an architecture look sophisticated.

This selection responds to those conditions:

1. It exposes **durable engineering concepts**—database roles and replication, service dependencies, configuration safety, failure propagation, monitoring, alerts, recovery, and the distinction between a fix being proposed, merged, and later observed to work.
2. It addresses a **real documented knowledge-sharing workflow**, not an invented “chat with PDFs” application. Wikimedia's own [incident review proposal](https://wikitech.wikimedia.org/wiki/Incident_review_ritual) describes uneven report quality, manual interpretation, and rediscovery of institutional knowledge [W1].
3. Its text contains a credible **relationship-retrieval hypothesis**: an incident may refer to a corrective task, another report may describe a related detection outcome, and a separate runbook may explain the technical boundary. The relationships can matter more than keyword overlap.
4. A small public corpus makes it possible to **measure whether this hypothesis is true** before building an expensive graph stack.
5. Even if a strong non-graph approach wins, the work can still demonstrate defensible engineering judgment, reproducible experiments, and expertise in real production failure modes.

---

## 2. Research provenance and claim-status convention

This document synthesizes the user's previously uploaded Perplexity investigations and independent checks of selected first-party webpages performed for this dossier on **4 November 2026**. It does **not** represent a complete crawl or audited licensed corpus.

| Label | Meaning | How it may be used |
|---|---|---|
| **V — First-party page inspected** | The named original source page was independently found/read and supports the stated fact. | Suitable as a candidate primary source; still needs a recorded corpus snapshot for reproducible evaluation. |
| **R — Research-reported, not independently reproduced here** | The uploaded research describes an inspected source or relationship, but this verification pass could not recover enough primary text to confirm the whole claim. | Discovery lead only; **not** a verified gold answer or settled graph edge. |
| **P — Proposed** | A planned subset, schema, question, metric, or experiment; it is not a factual observation or result. | Suitable for selection criteria and future planning. |
| **U — Unresolved** | Access, license, provenance, correctness, interpretation, or technical advantage remains unknown. | Must be gated, omitted, or explicitly disclosed. |

**Important distinctions:**

- **Publicly readable** ≠ freely redistributable.
- **Official documentation exists** ≠ the data was successfully fetched through an API.
- **A document links to a task** ≠ the task's full content was independently inspected.
- **A task was closed/merged** ≠ a proposed corrective action was operationally effective.
- **Two incidents share a symptom** ≠ they share the same cause.
- **Two sources describe the same event** ≠ they provide independent corroboration.
- **Graph-shaped knowledge** ≠ a graph database is required.

The detailed source register and stable primary URLs appear in [Section 14](#14-primary-source-register-and-verification-status).

---

## 3. The real-world problem and its boundaries

### 3.1 Problem statement

> **For a historical production reliability question, find the relevant incidents, explain the specific source-supported failure and dependency chains, distinguish similar symptoms with different causes, and connect the incidents to documented responses and corrective actions—while clearly indicating missing or time-limited evidence.**

The challenge is **not** identifying every report with the words “database outage.” It is discovering and faithfully presenting evidence such as:

`Observed symptom → affected system layer → failure mechanism → contributing condition → user/service impact → detection and response → proposed corrective action → later reported evidence`

This is an **illustrative question-to-evidence pattern**, not a mandatory graph schema or a claim that all reports provide every field.

### 3.2 Why it is an authentic engineering workflow

The Wikimedia [incident review ritual](https://wikitech.wikimedia.org/wiki/Incident_review_ritual) explains that incident reports vary in completeness, that extracting specific information can require reading and reasoning across documents, and that important infrastructure knowledge can remain insufficiently shared [W1]. Its proposed review process specifically asks whether similar incidents happened previously and whether follow-up work needs to be reprioritized. The page is a *process proposal*, not quantitative proof of demand for a new AI product.

The broader ecosystem reinforces the relevance: [Google's SRE resources](https://sre.google/) describe incident reviews, postmortems, corrective learning and reliability practices [M1]. Existing incident-management vendors also offer related-incident discovery; therefore the novel claim **cannot** simply be “engineers need incident search.”

The **narrow residual question** is whether evidence-aware retrieval can produce *more complete, better-qualified connections* between incidents, mechanisms, follow-ups and later observations than strong existing retrieval techniques.

### 3.3 In scope

- Historical, publicly documented incidents and their source-linked technical evidence.
- Explanations of reported triggers, contributing factors, dependencies, consequences, detection, mitigation and follow-up.
- Comparison of failure *mechanisms*, not only incident titles or shared keywords.
- Historical and document-status qualifications (final, in-review, draft, current runbook, historical incident).
- Evidence-level statements such as “the report says,” “the task proposes,” “the later incident documents,” and “the available records do not establish.”
- Source-linked, retrospectively framed learning about software reliability.

### 3.4 Explicitly out of scope

- Access to live production systems or private logs.
- Automatic incident triage, emergency recovery, infrastructure changes, or execution of operational runbooks.
- Claims that historical Wikimedia configurations describe a user's present infrastructure.
- Predictions that a particular provider will have another outage.
- Claims of verified root cause beyond the original author's stated certainty.
- Employee- or responder-focused profiling, blame assignment, or person-relationship graphs.
- Claims that an incident assistant replaces professional SRE judgment.

---

## 4. Why this domain has long-term learning value

| Knowledge area | What the source collection can teach | Future engineering relevance |
|---|---|---|
| **Distributed systems** | Dependent services, shared infrastructure and cascading impact | Cloud platforms, backend systems, AI serving |
| **Databases and replication** | Primary/replica roles, failover, database availability versus application write availability | Data engineering, backend services, resilient applications |
| **Observability** | Monitoring blind spots, user-visible symptoms, actionable alerts, detection versus diagnosis | SRE, DevOps, LLMOps |
| **Configuration safety** | String/Boolean mistakes, deployment/switchover states, changes with unexpected scope | Platform engineering, CI/CD |
| **Reliability mechanisms** | Load amplification, connection exhaustion, retries, backoff and failure domains | API systems, cloud infrastructure |
| **Incident analysis** | Trigger versus contributing cause versus uncertain finding | Engineering reviews, debugging |
| **Corrective-action evidence** | Proposed work versus code/documentation change versus observed outcome | Production change management |
| **AI engineering** | Entity extraction, provenance, hybrid retrieval, evaluation, uncertainty handling | Enterprise RAG and applied ML systems |

A **good** project will teach the mechanisms from the source text rather than simply collecting organization-specific shell commands. Domain-specific commands in a runbook should remain *historical/source context*, not instructions generated for a user to execute.

---

## 5. Primary corpus: Wikimedia Wikitech and related records

### 5.1 Corpus identity

**Collection name (project-defined):** *Wikimedia Software Reliability Evidence Pilot*.

**Owner/author of underlying documents:** Wikimedia Foundation technical community and documented contributors; individual pages may have multiple revisions and statuses.

**Discovery and hosting:** [Wikitech](https://wikitech.wikimedia.org/). Incident pages often reside under `Incidents/`, while operational reference pages reside under subject-specific paths. Links from those sources may point to Wikimedia Phabricator tasks or other external records.

**Content forms:** HTML/wiki text, incident timelines, action-item references, incident-status fields, linked runbooks and potentially task descriptions/comments. Some pages contain diagrams, images, logs or embedded links that require separate handling.

**Selection philosophy:** choose a *connected, evaluable subset*, not every page appearing in a search category. The [incident-documentation category](https://wikitech.wikimedia.org/wiki/Category:Incident_documentation) displayed **592 total members** in the source inspection, with separate draft and in-review subcategories [W2]. This is a **point-in-time category listing**, **not** 592 final, distinct, eligible incident reports. The count can change.

### 5.2 What qualifies for the initial pilot

Prefer documents that:

1. Directly describe a specific production incident and identify its time/context.
2. Explain the observed failure mode with an attributable evidence statement.
3. Link to another useful artifact, such as a corrective task, runbook or subsequent incident.
4. Contain enough factual detail to write at least one checked question.
5. Can be preserved with a canonical URL, revision/status, retrieval date, and acceptable rights treatment.
6. Offer **diversity of mechanisms** so a system cannot succeed by memorizing the same read-only issue repeatedly.

Keep **final**, **in-review**, and **draft** reports labeled separately; do not discard their status in the answer or silently treat all reports as final conclusions.

### 5.3 Core independently inspected source documents

| ID | Source | Type / dated context | Factual role in corpus | Status |
|---|---|---|---|---|
| **W1** | [Incident review ritual](https://wikitech.wikimedia.org/wiki/Incident_review_ritual) | Process documentation; page shows later edits | Direct evidence for the knowledge-sharing and incident-learning problem; *not* incident ground truth | **V** |
| **W2** | [Category: Incident documentation](https://wikitech.wikimedia.org/wiki/Category:Incident_documentation) | Discovery index | Candidate discovery, links to pages and document-status categories | **V** |
| **W3** | [2017-07-28 s5 (Wikidata and dewiki) read-only](https://wikitech.wikimedia.org/wiki/Incidents/2017-07-28_s5_%28WikiData_and_dewiki%29_read-only) | Historical incident report | Database process restart, intentional read-only state, healthy-looking replication, delayed detection, linked corrective-action task | **V** |
| **W4** | [2023-02-22 read only](https://wikitech.wikimedia.org/wiki/Incidents/2023-02-22_read_only) | Incident report labeled **final** | Application/configuration-level read-only behavior during switchover testing, type mismatch, differing user impact | **V** |
| **W5** | [2021-04-27 Commons wiki primary db](https://wikitech.wikimedia.org/wiki/Incidents/2021-04-27_Commons_wiki_primary_db) | Incident report labeled **final** | Database contention, uncertain attribution, temporary read-only state, recovery and consequences for related services | **V** |
| **W6** | [MariaDB/Troubleshooting](https://wikitech.wikimedia.org/wiki/MariaDB/Troubleshooting) | Operational guide labeled **work in progress** | Primary-versus-replica distinctions and why read-only state can be protective after a crash | **V**, evolving |
| **W7** | [Switch Datacenter](https://wikitech.wikimedia.org/wiki/Switch_Datacenter) | Operational documentation, includes changing/current procedures | Separates application read-only phases from database read-only phases and explains switchover dependencies | **V**, evolving |
| **W8** | [2023-02-22 wiki outage](https://wikitech.wikimedia.org/wiki/Incidents/2023-02-22_wiki_outage) | Incident report labeled **draft** | HAProxy maintenance/depooling error causing widespread web traffic impact; demonstrates mechanism diversity | **V**, draft |
| **W9** | [2021-11-10 cirrussearch commonsfile outage](https://wikitech.wikimedia.org/wiki/Incidents/2021-11-10_cirrussearch_commonsfile_outage) | Historical incident | Search/index dependency impact and downstream cross-wiki failures | **V**, quality review required |
| **W10** | [Incident status / reporting history](https://wikitech.wikimedia.org/wiki/Incident_status) | Index/process page | Discovery context; notes newer incident tracking via Corto/Phabricator | **V**, not a single incident |

**Why include W5, W8 and W9?** These records broaden the technical failure mechanisms beyond the original read-only cluster. Their inclusion in a final pilot remains **proposed**, not automatically approved; review document quality, status, rights and benchmark usefulness first.

### 5.4 Linked tasks and the 2020 follow-up: source verification boundary

The uploaded Perplexity Wikimedia investigation reports an especially promising chain:

- **W3:** a 2017 read-only detection gap references **[Phabricator T172489](https://phabricator.wikimedia.org/T172489)**.
- **T172489:** the research reports a discussion/implementation history concerning monitoring and paging when a database primary returns in read-only state.
- **A 2020 Commons read-only incident:** the research reports that a subsequent incident explicitly described the read-only alert as working well.
- **[Phabricator T253832](https://phabricator.wikimedia.org/T253832):** the research reports follow-up troubleshooting documentation changes.

**Current status: partially verified / not gold-ready.** W3 was independently inspected and **does** reference T172489. However, direct access to the two Phabricator task URLs failed in this verification environment; the exact 2020 Commons incident page was **not independently reidentified here**. These are usable **research-reported leads (R)**, not yet a fully independently rechecked four-source evidence chain.

Do **not** claim the following as proven until the linked source pages are actually fetched, saved, and reviewed:

- That the relevant task was completed with precisely the scope described in the earlier research.
- That the later alert's successful operation proves causal effectiveness of the earlier change.
- That the 2020 incident identified in the report can be uniquely linked to both tasks.
- That Phabricator comments and attachments are cleared for bulk reuse.

**Practical implication:** W3, W4, W5, W6 and W7 already form a strong small, source-grounded starting set. The complete incident-to-corrective-action-to-later-evidence chain is an important **validation gate**, not a fabricated finished benchmark example.

### 5.5 Specific source-grounded technical lessons

#### Case A — “Process recovered” is not “writes available” (W3)

The [2017 incident](https://wikitech.wikimedia.org/wiki/Incidents/2017-07-28_s5_%28WikiData_and_dewiki%29_read-only) describes a MySQL process terminated by out-of-memory behavior; the server restarted and recovered but remained intentionally in read-only mode. The report says replication appeared normal, which made the source of user-visible editing problems less obvious. It identifies delayed detection as a main problem and lists follow-up monitoring work.

**Supported lesson:** several health signals can be normal while a particular user-facing operation is unavailable. It would be incorrect to infer that a successful restart or replication health by itself proves write availability.

**Important qualification:** this is the incident author's description of *Wikimedia's then-existing setup*. It is not a universal statement about every database configuration.

#### Case B — Same symptom, different layer (W4 versus W3/W5)

The [2023 read-only incident](https://wikitech.wikimedia.org/wiki/Incidents/2023-02-22_read_only) describes application-level read-only behavior during a datacenter switchover test. The report identifies a type mismatch (a string value versus a Boolean) and records different effects for mobile and desktop editing before a broader interruption. It is labeled **final**.

By contrast, W3 involved a database process crash and protective database state; W5 describes serious database contention and a temporary read-only period during recovery. These are **different mechanisms** despite partially overlapping user symptoms.

**Supported lesson:** symptom-level similarity is not enough for causal equivalence. A correct system should explain **which layer, mechanism and evidence** distinguish cases.

#### Case C — Operational guidance is contextual (W6/W7)

[MariaDB/Troubleshooting](https://wikitech.wikimedia.org/wiki/MariaDB/Troubleshooting) emphasizes the difference between a primary and replica and describes a primary returning in read-only mode as an intentional protection after a crash. It explicitly identifies itself as **work in progress**. [Switch Datacenter](https://wikitech.wikimedia.org/wiki/Switch_Datacenter) separately documents application and database read-only phases as part of scheduled operations.

**Supported lesson:** read-only status may be protective, planned, or a symptom of failure; the correct interpretation depends on system role and context.

**Temporal qualification:** a runbook as it appears in November 2026 is not automatically evidence of the exact procedure in July 2017 or February 2023. For historical answers, cite incident-time documents and mark the runbook as *present-day contextual reference* unless a historical revision is deliberately verified.

#### Case D — A different failure family (W8/W9)

[The February 2023 wiki outage](https://wikitech.wikimedia.org/wiki/Incidents/2023-02-22_wiki_outage), marked **draft**, describes a cache/backend-depooling maintenance error; the result was a service-availability failure rather than the same read-only mechanism as W4. [The November 2021 search incident](https://wikitech.wikimedia.org/wiki/Incidents/2021-11-10_cirrussearch_commonsfile_outage) describes a failure affecting search behavior across services through a shared search-index dependency.

**Supported lesson:** a pilot should include unrelated mechanisms to test whether the system can correctly **reject false analogies**, not just retrieve similar documents.

---

## 6. Conditional expansion: first-party cross-provider reliability postmortems

### 6.1 Why expansion is useful—but not the first ingestion step

A Wikimedia-only corpus may overfit one organization's naming conventions, linked tasks, and topology. Cross-provider documents can test whether the retriever recognizes **shared engineering patterns despite different vocabulary**.

However, broadening early introduces additional rights, terminology, extraction and ground-truth burdens. Treat the following documents as **verified expansion candidates**, not already-ingested project data.

### 6.2 Source candidates independently inspected

| ID | Provider / original source | Document | Useful evidence | Status |
|---|---|---|---|---|
| **X1** | GitHub | [Availability report: February 2026](https://github.blog/news-insights/company-news/github-availability-report-february-2026/) (published March 2026) | Cache update/write amplification, background-work overload, replication delays and cascading service effects; several incident accounts in one report | **V**, expansion candidate |
| **X2** | GitHub | [Availability report: May 2026](https://github.blog/news-insights/company-news/github-availability-report-may-2026/) (published June 2026) | Schema-migration load saturating database connections; query contention, dependent-service timeouts, separate database/schema issues | **V**, expansion candidate |
| **X3** | Cloudflare | [Cloudflare service outage: 12 June 2025](https://blog.cloudflare.com/cloudflare-service-outage-june-12-2025/) | Failure in underlying Workers KV storage, broad downstream dependencies, differentiated service impacts, remediation discussion | **V**, expansion candidate |
| **X4** | Google Cloud | [Service incident: 12 June 2025](https://status.cloud.google.com/incidents/ow5i3PPK96RduMcb1SsW) | Service Control code path, globally replicated policy metadata, crash loops, recovery load on Spanner and follow-up safeguards | **V**, expansion candidate |
| **X5** | Cloudflare | [Post Mortem archive](https://blog.cloudflare.com/tag/post-mortem/) | Candidate discovery, not an automatically approved corpus | **V**, index |
| **X6** | Google Cloud | [Cloud Service Health](https://status.cloud.google.com/) | Incident discovery and published updates | **V** as general entry point; individual documents need assessment |
| **M1** | Google | [SRE resources](https://sre.google/) | Terminology and reliability practices; **methodological context, not independent incident proof** | **V** as source family |

### 6.3 Evidence summaries with required caution

**GitHub, February 2026 (X1).** The report describes related cache-update failures in which high write volumes affected shared infrastructure and Git operations; later updates caused additional cascading problems. It also covers other, separate incidents. **Do not** merge the whole monthly report into a single incident node: one monthly article can contain multiple distinct incident episodes.

**GitHub, May 2026 (X2).** The report documents a routine online schema migration whose load, combined with normal traffic, saturated database connection capacity and caused dependent-service timeouts. It also records other failures. **Do not** treat the report's various episodes as one causal chain.

**Cloudflare, June 2025 (X3).** Cloudflare attributes a widespread service failure to underlying storage infrastructure used by Workers KV, including infrastructure associated with a third-party provider. Multiple products depended on Workers KV for configuration, identity or other purposes, expanding impact. **Do not** assert that every Cloudflare product was affected in the same way; the report provides product-specific distinctions.

**Google Cloud, June 2025 (X4).** The official incident report describes a deployed Service Control feature whose faulty code path was exercised after a later policy change. Invalid fields were rapidly replicated, triggering regional crash loops; subsequent recovery load complicated restoration in a major region. Follow-ups include stronger isolation, controlled propagation, testing, feature flags and backoff. **Do not** conflate a planned preventative change with demonstrated later implementation unless further evidence exists.

### 6.4 Generalization question examples (proposed, not gold labels)

1. Across X1 and X2, what different pathways led from changes in database or cache behavior to failures in dependent services?
2. Across X3 and X4, how did a shared infrastructure layer widen the impact of a more localized initiating problem, and which mitigations concerned *containment* rather than only the trigger?
3. Which reports discuss excessive work during recovery, retries or background processing, and what distinctions prevent the incidents from being treated as identical?
4. Which mitigations are **reported as completed**, which are **announced as future work**, and which have no subsequent effectiveness evidence in the available corpus?

Each question requires an independently annotated minimum evidence set. Merely referencing several reports does **not** prove graph superiority: iterative retrieval or broad-context reading may supply the same answer.

---

## 7. Corpus design principles, without prematurely selecting an architecture

### 7.1 Separate document evidence from derived interpretations

An evidence system should distinguish at least four conceptual layers:

1. **Source artifact:** a specific page, report, task or runbook at an identifiable revision or snapshot.
2. **Evidence passage:** the smallest useful passage or section supporting an observation.
3. **Source-stated fact/claim:** what that artifact actually says, including its qualification and time.
4. **Analyst-derived relationship/pattern:** an interpretation connecting claims within or across artifacts, explicitly labeled as an inference until checked.

A **graph**, a **relational table**, or a **search index** could implement portions of this representation. Do not choose one solely because the information can be drawn as nodes and arrows.

### 7.2 Candidate entity concepts — design hypotheses, not discovered inventory

| Concept | Description | Essential caution |
|---|---|---|
| Incident | An identified production event or distinct episode | One monthly report can describe multiple incidents |
| SourceDocument | Report, runbook, task or update | Preserve revision/status and source rights |
| EvidencePassage | Text span supporting a specific claim | Citation must entail its claim |
| Service / Component | Systems identified by the source | Avoid inventing hidden dependencies |
| ObservedSymptom | User-visible or measured failure | Symptoms do not establish causes |
| Trigger / Change | Event preceding or associated with failure | A preceding change is not automatically causal |
| FailureMechanism | Source-described reason an effect occurred | Preserve certainty and attribution |
| Dependency | Explicit or well-supported dependency link | Scope may be time- or context-limited |
| Impact | Affected operation, user population or service | Preserve ranges, dates and uncertainty |
| Detection / Alert | What revealed or failed to reveal an incident | Alert fired ≠ effective diagnosis |
| Mitigation | Action that reduced reported impact | Mitigation ≠ permanent prevention |
| CorrectiveAction | Proposed or later recorded follow-up | Planned, merged, closed and verified are distinct |
| EngineeringPattern | Cross-incident abstraction | Derived analogy, not independently established fact |

### 7.3 Relationships worth testing

Potential relations include:

- `DOCUMENTS_INCIDENT`
- `SUPPORTS_CLAIM`
- `AFFECTED_SERVICE`
- `INVOLVED_COMPONENT`
- `REPORTED_TRIGGER`
- `REPORTED_CONTRIBUTOR`
- `PROPAGATED_THROUGH`
- `DETECTED_BY`
- `MITIGATED_BY`
- `LED_TO_FOLLOWUP`
- `FOLLOWUP_REFERENCED_BY`
- `REPORTED_SIMILAR_MECHANISM`

**Do not encode a general `CAUSED` edge merely because a model inferred it.** If causal language appears in an original report, record its attribution and level of certainty. A cross-incident analogy should be labeled as derived and cited to the source evidence for each case.

### 7.4 Important distinctions for faithful extraction

- Initiating **trigger** versus **root cause** versus **contributing condition**.
- **Observed symptom** versus **investigator explanation**.
- **Detection** versus **mitigation** versus **preventive action**.
- **Planned action** versus **implemented action** versus **later reported effectiveness**.
- **Database read-only** versus **application read-only** versus **planned maintenance read-only**.
- **Same symptom** versus **similar mechanism** versus **same underlying cause**.
- **Document publication date** versus **incident occurrence date** versus **source revision date**.
- **Operator-reported certainty** versus **model-inferred certainty**.

---

## 8. Suggested source manifest and reproducibility fields

A serious portfolio project should let another developer reproduce **which documents and revisions were used**. The following is a *proposed* metadata contract, not a statement that a manifest has been populated.

| Field | Purpose | Example / handling |
|---|---|---|
| `source_id` | Stable local identifier | `W3`, `X4`; internal IDs may be standardized later |
| `publisher` | Authoritative publisher/operator | `Wikimedia`, `GitHub`, `Cloudflare`, `Google Cloud` |
| `canonical_url` | Link to original source | Full official URL |
| `source_type` | Incident, runbook, task, archive, process doc | Do not mix these in evaluation |
| `document_title` | Original title | As displayed by original page |
| `incident_date_start/end` | When the actual event took place | Nullable; use source timezone/UTC explicitly |
| `publication_date` | When the document was released | Different from event date |
| `retrieved_at_utc` | Snapshot acquisition timestamp | Required for reproducibility |
| `revision_id` / `oldid` | Immutable wiki revision when available | Do not invent if unavailable |
| `content_sha256` | Hash of acquired bytes/text | Compute at acquisition time, not by inspection |
| `status_at_snapshot` | `final`, `draft`, `in-review`, `WIP`, etc. | Preserve displayed source status |
| `license_assessment` | Page-level permission status | `reviewed`, `restricted`, `unknown` |
| `embedded_material_exclusions` | Non-reusable images/third-party material | Keep separate from main text |
| `acquisition_method` | Manual access, official API, authorized export | Record which method actually worked |
| `parsing_notes` | Tables, timelines, redirects, missing sections | Record failures and ambiguity |
| `linked_source_ids` | Directly referenced documents/tasks | Preserve actual target URL and access status |
| `quality_review` | Evidence completeness and citation readiness | Reviewer, date, reasons |
| `benchmark_eligibility` | Whether source can support gold labels | Explicit yes/no/pending with rationale |

**Suggested minimal JSON example (schema illustration only):**

```json
{
  "source_id": "W3",
  "publisher": "Wikimedia",
  "source_type": "incident_report",
  "canonical_url": "https://wikitech.wikimedia.org/wiki/Incidents/2017-07-28_s5_%28WikiData_and_dewiki%29_read-only",
  "incident_date": "2017-07-28",
  "retrieved_at_utc": null,
  "revision_id": null,
  "content_sha256": null,
  "license_assessment": "not_yet_completed",
  "benchmark_eligibility": "pending_snapshot_and_review"
}
```

The `null` values are deliberately **unfilled**. No automated acquisition, hash computation or revision pinning is being claimed in this document.

---

## 9. Acquisition, licensing, attribution and public-demo constraints

### 9.1 Wikimedia technical content

- Wikitech pages display a **Creative Commons Attribution-ShareAlike** notice and link to Wikimedia terms; check the specific page footer and current applicable license version before republication. See [W1](https://wikitech.wikimedia.org/wiki/Incident_review_ritual).
- The page's licensing notice does **not** automatically resolve rights to every embedded photograph, attachment, proprietary excerpt, linked external webpage, or Phabricator comment.
- Wikimedia documents official API usage guidelines and user-agent requirements: [API Usage Guidelines](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_API_Usage_Guidelines), [API access policy](https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy), and [User-Agent Policy](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy) [L1–L3].
- The [MediaWiki `categorymembers` API](https://www.mediawiki.org/wiki/API:Categorymembers) and its [continuation mechanism](https://www.mediawiki.org/wiki/API:Continue/en) are documented [L4–L5]. **This does not mean that a full Wikitech extraction was successfully tested here.**
- Automated users must identify their client, respect throttling and robots requirements, avoid excessive crawling and follow each endpoint's policy.
- Historic revision retrieval needs its own compliant acquisition approach; do not assume unlimited revision scraping is permitted.
- **Phabricator reuse remains unresolved.** Test the actual tasks, terms, available exports and any attachments separately before ingestion or redistribution.

### 9.2 GitHub, Cloudflare and Google Cloud postmortems

The official reports in X1–X4 are **publicly readable**, but this check did **not** establish one blanket permission to redistribute all article text, figures or associated content. Treat each publisher's current terms and individual pages as separate rights questions.

A conservative public-demo approach pending rights review is to:

- Retain canonical source URLs, dates, source identity and original attribution.
- Store only the text and derived data that the applicable usage terms permit.
- Show bounded quotations or short evidence excerpts with clear attribution where lawful.
- Link users to the original reports for full context.
- Avoid bulk redistribution of copied articles, third-party images, private task conversations and unreviewed log excerpts.
- Keep your own **project code** license separate from the **source corpus** rights.

This section is a **compliance checklist**, not a legal determination about AI training, embeddings, caching or fair use.

### 9.3 Acquisition statuses as of this document

| Acquisition item | Status |
|---|---|
| Core Wikitech incident and runbook **webpages** readable via independently inspected first-party pages | **Verified** |
| Wikitech incident category/index discoverable | **Verified** |
| Specific Wikitech source **revision snapshots downloaded and checksummed** | **Not done here** |
| Automated Wikitech category traversal and extraction | **Documented API; end-to-end execution not verified** |
| Phabricator task descriptions/comments exported and rights-cleared | **Unresolved** |
| Exact 2020 Commons follow-up incident reidentified | **Unresolved in this check** |
| GitHub/Cloudflare/Google Cloud specific incident report pages accessible | **Verified** |
| Blanket rights to rehost those external articles | **Not established** |
| A final benchmark-ready corpus manifest | **Not yet created** |

---

## 10. Question classes and example evaluation targets

### 10.1 What a real benchmark should distinguish

| Class | Purpose | Example |
|---|---|---|
| **Single-document fact controls** | Check straightforward comprehension | What does W3 report about restart and read-only state? |
| **Same symptom / different mechanism** | Check causal distinction | How do W3 and W4 differ despite both affecting write availability? |
| **Incident-to-document context** | Find operational distinctions | What does W6 explain about protective read-only states that qualifies W3? |
| **Incident-to-corrective-action chain** | Retrieve multiple explicitly linked sources | What monitoring work was linked by W3, and what does the task itself document? **Task verification needed.** |
| **Later-evidence / temporal scope** | Separate a change from subsequent evidence | Did a later incident report describe the proposed alert as effective? **Exact chain verification needed.** |
| **Cross-provider pattern comparison** | Test generalizable technical relationships | How did shared dependencies magnify impact in X3 and X4? |
| **False analogy / unknown** | Prevent invention | Does the presence of a similar read-only symptom prove one shared root cause? **No; source details differ.** |
| **Insufficient evidence** | Measure calibrated abstention | Does a closed task prove a failure mode cannot recur? **Not from closure alone.** |

### 10.2 Initial documented question examples

**Q-A — Mechanism discrimination (source-supported).**  
“How did the 2017 Wikimedia database read-only event and the February 2023 Wikimedia read-only event arise, and why would treating them as the same fault be misleading?”

- Candidate minimum sources: **W3 and W4**.
- Supported contrast: database crash/restart/protective state versus switchover configuration/type behavior.
- Must not infer: one universal repair, one identical database root cause.
- **Category:** genuine comparison across two incident reports; graph improvement **not established**.

**Q-B — Symptom and system-role context (source-supported).**  
“Why can a database server be running without serving writes, and why do primary/replica roles affect the interpretation?”

- Candidate sources: **W3 and W6**.
- Caution: W6 is current/WIP documentation, not evidence of the exact historical runbook at incident time.
- **Category:** multi-source contextual explanation; it might be solved just as well by ordinary retrieval.

**Q-C — Protective versus accidental read-only (source-supported).**  
“What distinguishes an intended database protection after restart from an unintended application read-only configuration during a switchover test?”

- Candidate sources: **W3, W4, W6, W7**.
- Must preserve: different layers, operational contexts and document dates.
- **Category:** technical distinction; multiple cited sources.

**Q-D — Detection/corrective-action continuity (research-reported lead).**  
“What corrective detection work was linked from the 2017 incident, and what later observations support or limit the claim that it helped?”

- Candidate sources: **W3, T172489, specific later Commons report**.
- **Status: R / not gold-ready.** Task content and the later incident need independent acquisition and inspection.
- Must not infer: observed success proves permanent prevention or a quantified reduction in outage duration.

**Q-E — Similar outcome, different dependency path (source-supported expansion).**  
“Compare Cloudflare's Workers KV dependency failure with Google Cloud's Service Control policy-propagation failure. How did shared infrastructure widen impact, and what differs about the triggers?”

- Candidate sources: **X3 and X4**.
- **Category:** cross-provider mechanism comparison; not a pre-scored gold answer.
- Must not infer: the same trigger, same architecture or equivalent user impact.

**Q-F — Change-induced cascading effects (source-supported expansion).**  
“What distinct failure chains did GitHub describe for cache-write amplification in February 2026 and schema-migration load in May 2026?”

- Candidate sources: **X1 and X2**, ensuring the right *incident episode* is identified inside each monthly report.
- **Category:** cross-report comparison; graph advantage untested.

**Q-G — Correct abstention.**  
“Which of the proposed mitigation plans in X4 were independently verified as implemented and effective by a later source contained in this proposed pilot?”

- **Expected behavior at this stage:** do not claim an independently verified later implementation without the relevant later evidence.
- **Category:** insufficient-evidence control.

**Q-H — Quality/status awareness.**  
“How should a draft incident report such as W8 be treated differently from a final report such as W4 when constructing an answer?”

- **Expected behavior:** identify the status difference and refrain from silently raising tentative claims to final conclusions.
- **Category:** document-quality control.

### 10.3 A gold-answer record needs more than a plausible answer

For each selected benchmark question, preserve:

- The **literal user question** and its intended user workflow.
- The **minimum complete evidence set** (specific documents and sections).
- A **source-grounded answer**, with qualifiers and disputed/unknown aspects.
- The **relationships** that the evidence actually establishes.
- Whether one document already answers the entire question.
- Whether the question requires a simple lookup, cross-document synthesis, or genuine relationship expansion.
- The **unacceptable inferences** that should count as errors.
- The question's validation status, reviewer identity/role if applicable, and snapshot date.

**No gold benchmark records have been produced by this document.** The items above are a *curation brief* grounded in real primary-source examples.

---

## 11. How to decide whether Graph RAG is justified

### 11.1 The hypothesis

> **Relationship-guided retrieval may recover a more complete and more faithfully qualified set of historical failure, dependency and corrective-action evidence than strong non-graph retrieval, particularly when the question starts from a symptom or a generalized engineering pattern rather than an incident ID.**

This is a **falsifiable engineering hypothesis**, not a product claim.

### 11.2 Minimum serious baselines

The pilot should compare, wherever feasible and fairly configured:

1. Keyword or hybrid lexical/semantic retrieval with reranking.
2. Metadata- or entity-filtered retrieval.
3. Iterative retrieval/query decomposition.
4. **Direct hyperlink/follow-up expansion** (especially important for Wikimedia, where the sources already link tasks and runbooks).
5. Simple structured evidence tables and relational querying.
6. Long-context reading on a bounded subset, to avoid unfairly limiting a simpler model.
7. Relationship-guided retrieval, comparing **manually verified relationships** with **automatically extracted relationships**.

Use the same underlying source snapshot, comparable generation model, and comparable answer-context/evidence budgets. Any cost or latency improvement should include graph extraction/curation and not only per-query execution.

### 11.3 Measures worth reporting

| Measure | Why it matters |
|---|---|
| **Complete evidence-set recall** | Did retrieval recover *all* required sources, not just one relevant report? |
| **Claim-level citation support** | Does each cited passage actually support the specific sentence? |
| **Mechanism distinction accuracy** | Does the answer avoid conflating distinct causes and system layers? |
| **Temporal correctness** | Does it use the correct report/revision/time-qualified evidence? |
| **Correct action-state handling** | Does it separate proposed, implemented and later observed work? |
| **Unsupported causal inference rate** | Does it invent causal proof from chronology or a linked task? |
| **False analogy rate** | Does it overgeneralize across unrelated incidents? |
| **Abstention/uncertainty fidelity** | Does it accurately disclose missing records? |
| **Human review time** | Is the output useful to an analyst, rather than merely fluent? |
| **Latency, tokens, operating cost** | Is the added complexity proportionate to the benefit? |
| **Extraction and curation effort** | Can the corpus scale without excessive manual edge fixing? |

No values or improvements are supplied here, because **none has been measured**.

### 11.4 Proposed screening experiment (not the full development plan)

A plausible starting screen from the uploaded research is:

- Curate roughly **12–20** incident reports and **5–10** relevant operational/context pages, with a small number of linked task records if permission and access can be resolved.
- Develop roughly **40** questions spanning single-source controls, cross-incident mechanism comparisons, source-to-follow-up evidence, temporal qualification and unsupported-inference cases.
- Check whether at least **12–15** genuinely useful questions naturally require multiple sources, without artificially suppressing the most informative documents.
- Compare the strongest simple baselines against relationship-aware retrieval; repeat on automatically extracted relationships.
- Record the human effort needed to produce reliable evidence chains.

**All counts are design targets, not corpus facts or experimentally validated sample-size requirements.** A later full benchmark can be larger if the pilot justifies investment.

### 11.5 Stop, simplify, expand, or continue

**Continue towards Graph RAG if:**

- The sources and rights can be handled responsibly.
- Genuine multi-document evidence questions are common enough to matter.
- Relationship-guided retrieval improves a meaningful metric **consistently**, not just on a demonstration question.
- The improvement survives automatic extraction noise and reasonable data curation.
- The benefit justifies ongoing complexity in retrieval, maintenance and deployment.

**Prefer the simpler architecture if:**

- Hyperlink expansion or iterative retrieval recovers substantially the same evidence.
- A well-maintained evidence table and SQL already solve the valuable queries.
- Most questions are single-report or straightforward metadata questions.
- Apparent graph gains require manual edges handcrafted around benchmark questions.
- A graph database adds operational cost without practical query-management benefit.

**Reconsider the corpus if:** source rights, essential linked tasks, answerability, breadth of evidence or reliable evaluation fail at the selection stage.

**Cross-provider expansion is earned**, not assumed. Do not add GitHub, Cloudflare and Google Cloud merely to increase document count or UI appeal.

---

## 12. Principal risks and mitigation principles

| Risk | Why it matters | Mitigation principle |
|---|---|---|
| **Incomplete public evidence** | Operational decisions and internal context may be omitted. | State what sources support; refuse unsupported conclusions. |
| **Task-link gaps** | A referenced task may be unavailable or reuse-restricted. | Preserve the link and mark its evidence as unavailable; don't invent its contents. |
| **Report-status differences** | Draft or in-review language may be tentative. | Store/display document status and attribution. |
| **Temporal leakage** | Today's runbook may not describe a 2017 procedure. | Preserve event, publication and revision dates separately. |
| **False causality** | An LLM may turn correlation, chronology or hypothesis into cause. | Require evidence for source-stated causal claims; separate analogy from fact. |
| **Existing search already works** | Graph infrastructure may not add value. | Benchmark against hyperlinks, iterative retrieval and SQL. |
| **Provider disclosure differences** | Cross-provider reports vary in depth and vocabulary. | Score coverage; do not infer absence from non-reporting. |
| **Source rights ambiguity** | Public readability does not imply unrestricted redistribution. | Check individual source rights and use source-linked public display. |
| **Benchmark contamination** | Manual curation can overfit to chosen questions. | Reserve held-out incidents/questions and record annotation decisions. |
| **Extraction errors** | Incorrect relationships may harm answers. | Compare checked and automatic extractions; track errors. |
| **Overly narrow pilot** | Read-only-only questions may not generalize. | Include independent mechanism families and false-analogy controls. |
| **Overly broad product** | Multi-provider ingestion and graph maintenance may overwhelm a solo developer. | Validate one source ecosystem before expanding. |

---

## 13. Project justification, GitHub quality bar and interview narrative

### 13.1 Why this corpus rather than previous research candidates?

The previous research explored several serious alternatives. The reasons for choosing reliability evidence are comparative judgments, **not assertions that the other fields are unimportant**.

| Alternative | Why it was credible | Why it ranks below reliability for this particular goal |
|---|---|---|
| CSB industrial incident learning | Nuanced cross-case technical mechanisms; document-heavy evidence | Industrial process expertise and specialist validation burden are less directly transferable to general AI/backend engineering |
| Corporate debt amendments | Temporal obligations, exceptions, entity roles, multiple filings | Missing agreement exhibits and significant credit/legal interpretation burden |
| NTSB recommendation lineage | Strong identifiers and documentary provenance | Many high-value questions may reduce to explicit relational joins and existing search |
| Dependency remediation | Valuable software/security concepts | Existing dependency resolvers and advisory tools already handle much of the deterministic graph work |
| OpenTelemetry pipeline constraints | Highly valuable observability knowledge and clean documentation | Many questions may be best handled by config validation or documented rules |
| PostgreSQL migration rules | Fundamental database knowledge and favorable documentation rights | Version-aware checks and deterministic validation may outperform RAG |
| General AI incident datasets | Strong future relevance | Mixed evidence provenance, disputed reporting and reuse limitations complicate reliable evaluation |

### 13.2 The defensible interview explanation

> I wanted to build a retrieval system for an actual engineering information problem rather than attach a knowledge graph to an arbitrary dataset. I researched industrial safety, financial document lineage, dependency management and software reliability. I chose public production-incident evidence because it teaches distributed-system fundamentals and because questions about how failures propagate often require connecting incident reports, operational context and later corrective-action evidence. I deliberately started with a narrow Wikimedia corpus and compared relationship-guided retrieval against iterative search, direct hyperlinks and structured evidence tables before deciding whether a graph was justified. My final architectural choices and performance claims were based on the results of that comparison.

This is a **future-facing draft**. Do not claim the comparisons were completed until they actually are.

### 13.3 Evidence of a resume-ready finished project

A high-quality portfolio release should eventually provide:

- A real, publicly accessible **demo**, with reproducible source-linked questions and clearly labeled limitations.
- A GitHub README stating **problem → corpus → baseline → experiment → results → trade-offs**.
- A pinned, rights-reviewed corpus manifest or safe reproducible acquisition process.
- Transparent extraction and source-attribution behavior; no fabricated relationships.
- Actual benchmark tables including **non-graph** competitors and error analysis.
- A documented engineering decision explaining why graph-guided retrieval was kept or rejected.
- Reproducible setup, tests and a record of source and model versions.
- Measured cost/latency figures, if obtained, with precise measurement conditions.

**Do not** put invented accuracy gains, document counts, response times, deployment claims or employer endorsements in the README or on a resume.

### 13.4 Honest resume bullet template

> Built and deployed **[actual system type]** over **[verified N]** first-party software reliability records, connecting source-grounded incident mechanisms and corrective-action evidence; evaluated against **[actual baseline methods]**, obtaining **[measured evidence-recall/citation result]** at **[measured latency and cost]**.

The placeholders must be replaced only after those achievements exist.

### 13.5 Handoff boundary for Claude

This document **selects and defines a research corpus**. It intentionally does **not** dictate the final software architecture, database products, graph ontology cardinality, development milestones or implementation schedule. Claude should determine those after reviewing:

1. The selected problem and verified source register.
2. Acquisition and rights limitations.
3. Actual answerable questions and evidence chains.
4. Baselines and falsification criteria.
5. The solo-developer environment: VS Code, GitHub Copilot Student, GitHub version control, measurable deployment, and low-cost operation.

The high-level design rule is: **prove useful relationship-guided retrieval first; then choose the simplest architecture that delivers it.**

---

## 14. Primary source register and verification status

These are **explicit source URLs**, not search-result placeholders. The register distinguishes individually inspected content from historical-research leads. Webpage contents and licensing can change after the inspection date.

### 14.1 Wikimedia official sources — individually inspected

- **[W1] Incident review ritual** — documented incident-review/knowledge-sharing problem; page contains later amendments and deprecated sections.  
  https://wikitech.wikimedia.org/wiki/Incident_review_ritual  
  **Status:** V.

- **[W2] Incident documentation category** — discovery index, not an eligible-corpus size.  
  https://wikitech.wikimedia.org/wiki/Category:Incident_documentation  
  **Status:** V; displayed 592 members during this source check, subject to change.

- **[W3] 2017 Wikidata/dewiki read-only incident** — crash, restart, read-only, delayed detection, task reference.  
  https://wikitech.wikimedia.org/wiki/Incidents/2017-07-28_s5_%28WikiData_and_dewiki%29_read-only  
  **Status:** V.

- **[W4] 2023 read-only configuration incident** — final report, configuration/type error.  
  https://wikitech.wikimedia.org/wiki/Incidents/2023-02-22_read_only  
  **Status:** V.

- **[W5] 2021 Commons primary database incident** — final report, contention, uncertain attribution and recovery.  
  https://wikitech.wikimedia.org/wiki/Incidents/2021-04-27_Commons_wiki_primary_db  
  **Status:** V.

- **[W6] MariaDB/Troubleshooting** — role-conditional operational documentation; describes itself as work in progress.  
  https://wikitech.wikimedia.org/wiki/MariaDB/Troubleshooting  
  **Status:** V, evolving.

- **[W7] Switch Datacenter** — separates application and database read-only phases.  
  https://wikitech.wikimedia.org/wiki/Switch_Datacenter  
  **Status:** V, evolving.

- **[W8] 2023 wiki outage (HAProxy maintenance)** — draft report; distinct failure family.  
  https://wikitech.wikimedia.org/wiki/Incidents/2023-02-22_wiki_outage  
  **Status:** V, draft.

- **[W9] 2021 search-index outage** — source for dependent-service/search propagation.  
  https://wikitech.wikimedia.org/wiki/Incidents/2021-11-10_cirrussearch_commonsfile_outage  
  **Status:** V, review needed before gold-label inclusion.

- **[W10] Incident status index** — historical incident process/discovery; points to newer tracking arrangements.  
  https://wikitech.wikimedia.org/wiki/Incident_status  
  **Status:** V.

### 14.2 Wikimedia linked records — verification pending

- **[T1] Phabricator T172489** — referenced in W3; earlier research describes monitoring/paging follow-up.  
  https://phabricator.wikimedia.org/T172489  
  **Status:** W3 reference is V; task content R/U (direct retrieval failed here).

- **[T2] Phabricator T253832** — earlier research describes a troubleshooting/documentation follow-up.  
  https://phabricator.wikimedia.org/T253832  
  **Status:** R/U (direct retrieval failed here).

- **[T3] Reported 2020 Commons read-only follow-up report** — earlier research connects it to the alert history.  
  **URL:** *Not independently reidentified; deliberately not guessed.*  
  **Status:** R/U. Must be found and source-checked before use in gold evaluation.

### 14.3 Cross-provider source candidates — individually inspected

- **[X1] GitHub February 2026 availability report** — cache/write and other distinct incident chains.  
  https://github.blog/news-insights/company-news/github-availability-report-february-2026/  
  **Status:** V; public readability verified; redistribution terms not fully reviewed.

- **[X2] GitHub May 2026 availability report** — schema migration pressure and database/dependency impacts.  
  https://github.blog/news-insights/company-news/github-availability-report-may-2026/  
  **Status:** V; redistribution terms not fully reviewed.

- **[X3] Cloudflare June 2025 outage postmortem** — Workers KV underlying storage and downstream service dependencies.  
  https://blog.cloudflare.com/cloudflare-service-outage-june-12-2025/  
  **Status:** V; redistribution terms not fully reviewed.

- **[X4] Google Cloud June 2025 incident report** — Service Control policy, global replication, crash/recovery and follow-ups.  
  https://status.cloud.google.com/incidents/ow5i3PPK96RduMcb1SsW  
  **Status:** V; redistribution terms not fully reviewed.

- **[X5] Cloudflare Post Mortem index** — candidate discovery.  
  https://blog.cloudflare.com/tag/post-mortem/  
  **Status:** V.

- **[X6] Google Cloud Service Health** — source discovery.  
  https://status.cloud.google.com/  
  **Status:** official source entry point; specific reports need separate inspection.

- **[M1] Google SRE resources** — general postmortem/reliability practices rather than independent incident evidence.  
  https://sre.google/  
  **Status:** official reference family.

### 14.4 Official usage and acquisition documentation

- **[L1] Wikimedia Foundation API Usage Guidelines:**  
  https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_API_Usage_Guidelines
- **[L2] Wikimedia API access policy:**  
  https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy
- **[L3] Wikimedia Foundation User-Agent Policy:**  
  https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy
- **[L4] MediaWiki categorymembers API documentation:**  
  https://www.mediawiki.org/wiki/API:Categorymembers
- **[L5] MediaWiki API continuation documentation:**  
  https://www.mediawiki.org/wiki/API:Continue/en

These pages are **documentation of supported mechanisms and obligations**, not evidence that this project has completed its data acquisition.

---

## 15. Decision log: what is frozen and what remains open

| Decision / question | Status | Reason |
|---|---|---|
| **Software-reliability evidence as the project domain** | **Selected** | High long-term engineering relevance and real source-grounded workflow |
| **Wikimedia Wikitech as the initial source ecosystem** | **Selected for pilot** | Source-grounded examples, linked evidence, bounded acquisition |
| **Read-only/write-availability as an initial case family** | **Selected as entry point, not sole topic** | Clearly distinguishable mechanisms and useful context pages |
| **Additional Wikimedia mechanisms** | **Recommended** | Prevent overfitting one symptom |
| **GitHub/Cloudflare/Google Cloud expansion** | **Conditional** | Tests vocabulary and cross-provider generalization |
| **Phabricator task ingestion** | **Blocked pending access/rights review** | Key task content not independently retrieved here |
| **Automatic wiki ingestion** | **Unverified** | Official API is documented; successful acquisition not established |
| **Graph-guided retrieval value** | **Unproven** | Requires comparison with strong non-graph retrieval |
| **Neo4j or another graph database** | **Not decided** | Representation benefit does not prove database benefit |
| **Production deployment** | **Not yet implemented** | Requires architecture, licensing, testing and hosting decisions |
| **Final resume metrics** | **Unknown** | Must come from reproducible benchmark/deployment |

### Final recommendation

> **Use the Wikimedia reliability-evidence pilot as the first corpus-validation project, with cross-provider GitHub, Cloudflare and Google Cloud postmortems reserved as an earned generalization phase. The core thesis to test is complete, faithful recovery of historical incident-to-mechanism-to-action evidence—not that every incident needs a graph or that Graph RAG must win.**
>
> **Do not begin a large graph ingestion until source access, source rights, meaningful multi-document questions, and a real baseline comparison justify doing so.**

---

### Document maintenance note

This dossier is an **as-of-4-November-2026 selection record**, not a live status dashboard. Before turning any proposed source into benchmark data, reconfirm its URL, source status, revision, license, access method, and evidence. Record that review in the project's future manifest and update this file when a material decision changes. Source claims are traceable through the official links above; no benchmark or deployment results have been invented.
