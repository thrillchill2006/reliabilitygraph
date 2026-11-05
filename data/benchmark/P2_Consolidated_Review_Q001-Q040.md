# ReliabilityGraph — P2 consolidated independent evidence audit (Q001–Q040)

**Status: proposed corrections only; no benchmark approvals or freezes.**

## Scope and verification

- Audited the 40 candidate questions against the uploaded `questions.json`, `review_annotations.json`, `passages.json`, and `manifest.json`.
- Checked 61 original citation quote/source pairs for **exact consistency** with the frozen passage file; 0 ID/quote mismatches in those pairs. This does **not** establish semantic correctness.
- Proposed **36 revisions and 4 replacements**; none is approved unchanged for final gold use.
- No primary web pages were independently downloaded in this turn; the uploaded snapshot is the factual basis. `links.json`, raw source HTML and live Phabricator records were not available for independent cross-link checking.
- Related 2017/2021 incident claims are explicitly bounded by their source; later runbooks are context, not proof of historical operating procedure.
- A question citing two different documents is **not automatically genuine multi-hop reasoning**. Gold multi-source necessity still requires independent reviewer confirmation of the minimum evidence set.

## Immediate actions before Gate Q

1. Keep the original benchmark and review annotations unchanged until a human confirms these proposed edits.
2. Use the accompanying JSON patch proposal to revise question, class, answer and evidence references in a review branch; preserve previous versions and keep `review_status=pending`.
3. For each revised question, verify the cited primary source passage and source date/status; label minimum sufficient evidence, unsupported inference, and single-source shortcuts.
4. Ensure the dev/test split is incident-family-aware; documents W15 and W18 each include multiple event episodes—do not blindly treat every page as one independent incident.
5. For explicit-link controls, independently inspect `links.json` and permitted task content. No explicit task-link chain can be certified from these five uploaded files alone.
6. Review passage noise and headings before retrieval: some fragments such as `[edit]` are not useful evidence; do not renumber or invalidate gold anchors without coordinated migration.
7. Freeze only after human decisions, validator checks, confirmed multi-source count and a valid held-out split. Do not manufacture 12–15 multi-source questions to meet quota.

## Overview of proposed corrections

| ID | Decision | Proposed class | Distinct source count | Main issue |
|---|---|---|---:|---|
| Q001 | REVISE | `similar-symptom-different-mechanism` | 3 | Original W3 impact-only citation omitted mechanism; W5 uncertainty was not cited. |
| Q002 | REVISE | `single-document-control` | 1 | The cited W6 query-killer passage was unrelated; the task does not genuinely require multiple documents. |
| Q003 | REVISE | `multi-document-context-comparison` | 2 | Original question could be answered from W4 alone; the revision genuinely compares guide and report. |
| Q004 | REVISE | `multi-document-context-comparison` | 2 | Original W5 summary and W1 scorecard citation did not support the specific uncertainty claim. |
| Q005 | REVISE | `multi-document-context-comparison` | 2 | Original question largely answered by the runbook and could imply a failover not reported in W3. |
| Q006 | REVISE | `multi-document-context-comparison` | 2 | Original W7 introduction did not describe planned read-only; replace with relevant passages. |
| Q007 | REVISE | `cross-incident-comparison` | 2 | Original included unrelated failover guidance and used an impact rather than recovery citation. |
| Q008 | REPLACE | `multi-document-context-comparison` | 2 | Original claimed an incident-to-follow-up link not evidenced by its passages; linked Phabricator data were not uploaded. Replace rather than claim this is a verified explicit-link control. |
| Q009 | REVISE | `missing-evidence-negative` | 2 | Original stem presupposed completed corrective follow-ups. |
| Q010 | REVISE | `multi-document-context-comparison` | 2 | Original W6 binlog-related passage did not directly support the read-only-state claim. |
| Q011 | REVISE | `multi-document-context-comparison` | 2 | Original question was vague; clarify both the actual historical event and the unproven failover. |
| Q012 | REVISE | `cross-incident-comparison` | 3 | Original W9 citation concerned which search UI was affected, not cause uncertainty. |
| Q013 | REVISE | `false-analogy-negative` | 3 | Original W3 impact-only citation did not specify its mechanism. |
| Q014 | REVISE | `time-qualified` | 3 | Original cited unrelated RAID-WriteThrough guidance; use directly relevant historical and contextual spans. |
| Q015 | REVISE | `missing-evidence-negative` | 2 | Original generic prevention question could not be answered solely by the cited incident/review passages. |
| Q016 | REVISE | `single-document-control` | 1 | Original citation does not actually state that report quality varies; revise question to what W1’s available text supports. |
| Q017 | REVISE | `single-document-control` | 1 | Original quoted only the scope sentence and omitted the actual historical discovery link. |
| Q018 | REPLACE | `single-document-control` | 1 | Original question about database host roles was unsupported by its W11 citation; replace with an answerable W11 control. |
| Q019 | REVISE | `single-document-control` | 1 | Original mechanism essentially supported but word “cache-backed traffic” alone obscured the report’s broader impact and draft status. |
| Q020 | REPLACE | `single-document-control` | 1 | Original “limitations in metadata” question cited only an impact passage and was not supported as asked. |
| Q021 | REVISE | `single-document-control` | 1 | Original demanded “how quickly detected,” which cannot be precisely computed from the cited start alert alone. |
| Q022 | REVISE | `single-document-control` | 1 | Original cited only the maintenance-outcome passage, not the motivating conditions or planned mitigations. |
| Q023 | REVISE | `single-document-control` | 1 | Original citation described only the physical trigger, not the wider service effects. Note W15 contains multiple incident narratives in one page. |
| Q024 | REVISE | `single-document-control` | 1 | Original passage supported recovery but not the claimed recommendation. |
| Q025 | REVISE | `single-document-control` | 1 | Original cited only the later test, not the initiating incident. |
| Q026 | REVISE | `single-document-control` | 1 | Original cited only the node/data deletion and not the broken redundancy config or version issue. |
| Q027 | REVISE | `single-document-control` | 1 | Original passage is well-aligned; tighten the proposed answer to a short, attributed summary. |
| Q028 | REVISE | `single-document-control` | 1 | Original citation addresses propagation, but add triggering context and preserve uncertain recovery attribution. |
| Q029 | REVISE | `single-document-control` | 1 | Original passage discussed initial troubleshooting rather than the eventual root-cause evidence. |
| Q030 | REVISE | `cross-incident-comparison` | 2 | Original Q030 referenced only W13; the revised question requires W19 and discloses missing comparative alert timing. |
| Q031 | REVISE | `cross-incident-comparison` | 2 | Original Q031 cited only W16; add independent W17 evidence. |
| Q032 | REVISE | `cross-incident-comparison` | 2 | Original Q032 cited only W9 and mixed two historical search incidents. |
| Q033 | REVISE | `cross-incident-comparison` | 2 | Original Q033 had only W20; add a second independent mechanism. |
| Q034 | REVISE | `time-qualified` | 2 | Original W19-only citation could not compare action states; revised answer keeps source attribution. |
| Q035 | REVISE | `false-analogy-negative` | 2 | Original cited a Commons summary alone and could not meet a cross-source false-analogy design. |
| Q036 | REVISE | `multi-document-context-comparison` | 2 | Original Q036 cited only W14; it was not a true comparison. Preserve W8 draft status. |
| Q037 | REVISE | `multi-document-context-comparison` | 2 | Original Q037 cited only W11; now distinguishes general guidance from actual incident report. |
| Q038 | REVISE | `multi-document-context-comparison` | 2 | Original W3-only evidence could not support a comparison of detection and remediation; W18 provides explicit time points. |
| Q039 | REVISE | `missing-evidence-negative` | 1 | Original asked hypothetically what evidence would be required without clearly anchoring observed-versus-unproven claims. |
| Q040 | REPLACE | `abstention-control` | 2 | Original question was meta (“which comparisons remain unsafe until reviewer confirms”) and has no factual gold answer from the cited W1 passage. |

## Full question-by-question proposals

### Q001 — REVISE

**Original:** How do the selected incidents distinguish database crash, configuration, and contention mechanisms?

**Proposed:** Across the 2017 Wikidata/dewiki, 2023 switchover, and 2021 Commons incidents, which different failure mechanisms led to read-only/editing problems?

**Source-grounded reference answer (pending review):** W3 attributes the 2017 failure to an out-of-memory termination of the s5 master and its read-only restart. W4 identifies a 2023 switchover-script/configuration fault (including a string/Boolean mismatch) affecting application editing. W5 reports InnoDB contention as the immediate Commons cause, with GlobalUsage a probable contributor rather than a conclusively proven underlying cause. Similar symptoms are not a shared root cause.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W4** · `bd4538c326cc40b35c64` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2023-02-22_read_only) · While performing a live switchover test in advance of the 2023 WMF datacenter switchover, an existing logical bug on the switchover test script accidentally set the secondary datacenter in read-onl…
- **W4** · `3333cdc089fa5c167d5e` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2023-02-22_read_only) · The cause of read-only is confctl not setting the right type and putting a string instead of a boolean
- **W5** · `beb1aa23975ff1e674ed` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · From 10:28 to 11:43, Wikimedia Commons was unavailable and/or slow to respond. Additionally, from 10:41 to 11:10, commons was set in unscheduled read only mode (unable to create new users, upload f…
- **W5** · `8d300bddb41249b0611d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · GlobalUsage was signaled as the most probable cause, as it was sending large amount of long-running queries at the moment of the issue to the primary DB server. Because of the general InnoDB error…

**Reason:** Original W3 impact-only citation omitted mechanism; W5 uncertainty was not cited.

**Human decision:** Pending (approve corrected / edit / reject).

### Q002 — REVISE

**Original:** How does the 2017 report connect database recovery to delayed detection?

**Proposed:** What do the 2017 s5 incident passages establish about the OOM crash, the read-only interval, and the limits of detection evidence?

**Source-grounded reference answer (pending review):** The s5 master was killed by an out-of-memory event at 05:48 and restarted read-only. The source reports write unavailability until 07:04, when read-write was restored. The two snapshot passages do not identify a particular alert mechanism or exact initial human-detection time.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W3** · `a6c5831a40f60dc47c7f` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · Wikidata and the German Wikipedia were in read-only mode from 5:48 to 7:04 on 2017-07-28. No edits, user creations were possible between these two timestamps.

**Reason:** The cited W6 query-killer passage was unrelated; the task does not genuinely require multiple documents.

**Human decision:** Pending (approve corrected / edit / reject).

### Q003 — REVISE

**Original:** How does the 2023 report distinguish the switchover test from its user impact?

**Proposed:** What does the datacenter guide say a live test is intended to avoid, and what actually happened in the 2023 switchover test?

**Source-grounded reference answer (pending review):** The later/current guide says live-test mode should skip actions hazardous to the primary datacenter or execute them on the secondary. The 2023 report records an accidental secondary read-only setting and a subsequent tool issue that made both datacenters read-only. The 2026 guide is contextual and is not proof of exactly which instructions existed in 2023.

**Exact proposed evidence:**
- **W7** · `7975ea9322dad6530fce` · [official source](https://wikitech.wikimedia.org/wiki/Switch_Datacenter) · A live test ( --live-test) flag will skip actions that could harm the primary DC or perform them on the secondary DC and is available only for the sre.switchdc.mediawiki cookbook. What we should be…
- **W4** · `bd4538c326cc40b35c64` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2023-02-22_read_only) · While performing a live switchover test in advance of the 2023 WMF datacenter switchover, an existing logical bug on the switchover test script accidentally set the secondary datacenter in read-onl…

**Reason:** Original question could be answered from W4 alone; the revision genuinely compares guide and report.

**Caveat:** Temporal caveat: current W7 guidance is not necessarily incident-time procedure.

**Human decision:** Pending (approve corrected / edit / reject).

### Q004 — REVISE

**Original:** What uncertainty about immediate cause is preserved across the Commons incident and the review process?

**Proposed:** What causal uncertainty did the Commons incident preserve, and which principle in the review guidance helps avoid overclaiming?

**Source-grounded reference answer (pending review):** W5 identifies InnoDB contention as the immediate issue and says GlobalUsage was the most probable contributor, while the underlying cause was not proven. W1 encourages discussion and challenging assumptions to avoid hearsay and cargo-cult reasoning. W1 is proposed review practice, not a re-investigation of Commons.

**Exact proposed evidence:**
- **W5** · `8d300bddb41249b0611d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · GlobalUsage was signaled as the most probable cause, as it was sending large amount of long-running queries at the moment of the issue to the primary DB server. Because of the general InnoDB error…
- **W1** · `9f195aec0d7e5eff5768` · [official source](https://wikitech.wikimedia.org/wiki/Incident_review_ritual) · This is a pretty important part of the ritual. People should ask questions to help them clarify their understanding of the situation and the infrastructure. Better understanding of the infrastructu…

**Reason:** Original W5 summary and W1 scorecard citation did not support the specific uncertainty claim.

**Human decision:** Pending (approve corrected / edit / reject).

### Q005 — REVISE

**Original:** What operational distinction applies when a failed database host is a master rather than a replica?

**Proposed:** How does later MariaDB guidance on recovering a master contextualize the 2017 s5 restart, and what recovery action is not documented?

**Source-grounded reference answer (pending review):** W6 distinguishes master failures from replica failures because replicas can be at different transaction positions; it advises waiting when a master is recoverable. W3 describes an s5 master that restarted read-only after an OOM and was later restored to read-write. Neither cited incident passage says a replica was promoted.

**Exact proposed evidence:**
- **W6** · `3abfa35ce58076e6d8bd` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · If the master is not available, or replication is broken, this is a more complex case. The reason is that replicas will have executed different amount of transactions and will be in a close, but di…
- **W6** · `065aae695cdd4a878567` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · Scenario 1 -master is recoverable: just wait until the master restarts, it will avoid headaches and be faster and less disruptive than trying to failover it.
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…

**Reason:** Original question largely answered by the runbook and could imply a failover not reported in W3.

**Human decision:** Pending (approve corrected / edit / reject).

### Q006 — REVISE

**Original:** How does planned datacenter read-only differ from incident-time read-only?

**Proposed:** How does planned read-only during a datacenter switchover differ from the accidental read-only states in the 2023 incident?

**Source-grounded reference answer (pending review):** W7 describes a planned short read-only window and distinct application/database phases. W4 describes a live test accidentally leaving the secondary read-only and subsequent changes affecting both datacenters until reverted. The later guide’s stated expected duration is not the observed 2023 impact duration.

**Exact proposed evidence:**
- **W7** · `7a6f0b7daf106ec01f7b` · [official source](https://wikitech.wikimedia.org/wiki/Switch_Datacenter) · Impact of a switchover is expected to be 2-3 minutes of read-only for MediaWiki including extensions. Any other services/features/infrastructures not participating directly in the Switchover will c…
- **W7** · `a0934f5cd7b39601510b` · [official source](https://wikitech.wikimedia.org/wiki/Switch_Datacenter) · Read-only is a two-step process: we first set MediaWiki itself read-only and then the MediaWiki databases. We allow an amount of time between the two so as to allow the last in-flight edits to land…
- **W4** · `bd4538c326cc40b35c64` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2023-02-22_read_only) · While performing a live switchover test in advance of the 2023 WMF datacenter switchover, an existing logical bug on the switchover test script accidentally set the secondary datacenter in read-onl…

**Reason:** Original W7 introduction did not describe planned read-only; replace with relevant passages.

**Human decision:** Pending (approve corrected / edit / reject).

### Q007 — REVISE

**Original:** Which response actions recur between incident reports and the operational runbook?

**Proposed:** Compare the documented restoration actions for the 2017 s5 and 2021 Commons database incidents. Which steps differed?

**Source-grounded reference answer (pending review):** After its OOM crash, W3’s master restarted in read-only mode and was eventually set back to read-write. In W5, after restart and forced termination, the database came back read-only; GlobalUsage was temporarily disabled before restoring read-write. These are reported recovery actions, not proof of durable preventive fixes.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W5** · `beb1aa23975ff1e674ed` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · From 10:28 to 11:43, Wikimedia Commons was unavailable and/or slow to respond. Additionally, from 10:41 to 11:10, commons was set in unscheduled read only mode (unable to create new users, upload f…

**Reason:** Original included unrelated failover guidance and used an impact rather than recovery citation.

**Human decision:** Pending (approve corrected / edit / reject).

### Q008 — REPLACE

**Original:** What source evidence links an incident to a follow-up record, and what remains unknown?

**Proposed:** What did the 2021 Commons incident recommend about alert-response documentation, and what does the available MariaDB guide establish or leave unknown?

**Source-grounded reference answer (pending review):** W5 includes a recommendation to add links to a runbook and supporting documents for responders, or create an action item if missing. W6 is a later available, still-work-in-progress MariaDB troubleshooting guide. Their coexistence does not show that a specific incident-to-task link or alert documentation update was completed.

**Exact proposed evidence:**
- **W5** · `bc209f1665c6605db0cf` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · Add links to information that someone responding to this alert should have (runbook, plus supporting docs). If that documentation does not exist, add an action item to create it.
- **W6** · `c77817fef035954f1848` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · This guide is a work in progress. See also MariaDB/monitoring and MariaDB/Backups#Recovering a Snapshot
- **W6** · `49cf0417f9da2f41a15e` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · A master coming back in READ ONLY mode is expected after a crash and it is done to prevent accidental corruption (or even more corruption on a crash).

**Reason:** Original claimed an incident-to-follow-up link not evidenced by its passages; linked Phabricator data were not uploaded. Replace rather than claim this is a verified explicit-link control.

**Human decision:** Pending (approve corrected / edit / reject).

### Q009 — REVISE

**Original:** Why does a completed action not by itself establish prevention of recurrence?

**Proposed:** Do the 2017 and 2021 incident descriptions prove that their restorations prevented later similar outages?

**Source-grounded reference answer (pending review):** No. Both passages describe restoration from specific incidents; neither cited passage gives subsequent longitudinal evidence of nonrecurrence or verified preventive effectiveness. The incidents also have distinct immediate mechanisms. This is an absence-of-evidence finding limited to these passages, not proof that no corrective work ever occurred.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W5** · `beb1aa23975ff1e674ed` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · From 10:28 to 11:43, Wikimedia Commons was unavailable and/or slow to respond. Additionally, from 10:41 to 11:10, commons was set in unscheduled read only mode (unable to create new users, upload f…

**Reason:** Original stem presupposed completed corrective follow-ups.

**Human decision:** Pending (approve corrected / edit / reject).

### Q010 — REVISE

**Original:** Which documents describe read-only as a protective state after recovery?

**Proposed:** How does the read-only restart in the 2017 incident relate to the later runbook’s explanation of protective read-only state?

**Source-grounded reference answer (pending review):** W3 reports the s5 master restarting read-only after an OOM crash until returned to read-write. W6 says a primary may return read-only after a crash as protection against corruption, with reads available while writes are blocked. The sources do not prove this specific protection motivation was explicitly recorded in the 2017 incident.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W6** · `49cf0417f9da2f41a15e` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · A master coming back in READ ONLY mode is expected after a crash and it is done to prevent accidental corruption (or even more corruption on a crash).
- **W6** · `157e78b88446aa918ef1` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · Reads will remain unaffected but no writes will be able to go through, the wikis on that master will be on read-only mode.

**Reason:** Original W6 binlog-related passage did not directly support the read-only-state claim.

**Human decision:** Pending (approve corrected / edit / reject).

### Q011 — REVISE

**Original:** What later operational documentation qualifies the response described in the 2017 report?

**Proposed:** Which distinctions in the later MariaDB guidance prevent treating the 2017 s5 read-only restart as a documented replica failover?

**Source-grounded reference answer (pending review):** W3 reports OOM, restart in read-only, and eventual restoration on the s5 master. W6 explains that master recovery and replica promotion depend on recoverability and replication positions. No source passage cited for W3 establishes that promotion occurred; W6 is general later context.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W6** · `3abfa35ce58076e6d8bd` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · If the master is not available, or replication is broken, this is a more complex case. The reason is that replicas will have executed different amount of transactions and will be in a close, but di…
- **W6** · `065aae695cdd4a878567` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · Scenario 1 -master is recoverable: just wait until the master restarts, it will avoid headaches and be faster and less disruptive than trying to failover it.

**Reason:** Original question was vague; clarify both the actual historical event and the unproven failover.

**Human decision:** Pending (approve corrected / edit / reject).

### Q012 — REVISE

**Original:** Which records distinguish documented cause from suspected contributor?

**Proposed:** How do the 2017 s5, 2021 Commons and 2021 CirrusSearch reports differ in certainty about their triggering or contributing conditions?

**Source-grounded reference answer (pending review):** W3 directly attributes the s5 crash to an OOM event. W5 states that GlobalUsage was the most probable source of troublesome queries, with uncertainty over the deeper cause. W9 records a high volume of queries and index recreation, explicitly saying the exact reason for index recreation was not yet understood. Distinguish stated events from uncertain contributors or mechanisms.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W5** · `8d300bddb41249b0611d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · GlobalUsage was signaled as the most probable cause, as it was sending large amount of long-running queries at the moment of the issue to the primary DB server. Because of the general InnoDB error…
- **W9** · `d30c979102e8eaa9b74d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-11-10_cirrussearch_commonsfile_outage) · On 10 November, as part of verifying a bug report, a developer submitted a high volume of search queries against the active production Cirrus cluster (eqiad cirrussearch) via a tunnel from their lo…
- **W9** · `d7d61fe70633cbc00757` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-11-10_cirrussearch_commonsfile_outage) · As a direct consequence, any Elasticsearch queries that targetted media files from commonswiki encountered a hard failure.

**Reason:** Original W9 citation concerned which search UI was affected, not cause uncertainty.

**Human decision:** Pending (approve corrected / edit / reject).

### Q013 — REVISE

**Original:** Can the selected sources establish that all read-only events had one underlying cause?

**Proposed:** Did the three documented read-only/editing incidents share one established technical root cause?

**Source-grounded reference answer (pending review):** No: W3 reports an OOM-related database restart into read-only, W4 a switchover configuration/script error, and W5 database contention with uncertainty over an upstream contributor. The same user-visible write restriction is insufficient to infer the same root cause.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W4** · `bd4538c326cc40b35c64` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2023-02-22_read_only) · While performing a live switchover test in advance of the 2023 WMF datacenter switchover, an existing logical bug on the switchover test script accidentally set the secondary datacenter in read-onl…
- **W5** · `beb1aa23975ff1e674ed` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · From 10:28 to 11:43, Wikimedia Commons was unavailable and/or slow to respond. Additionally, from 10:41 to 11:10, commons was set in unscheduled read only mode (unable to create new users, upload f…
- **W5** · `8d300bddb41249b0611d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · GlobalUsage was signaled as the most probable cause, as it was sending large amount of long-running queries at the moment of the issue to the primary DB server. Because of the general InnoDB error…

**Reason:** Original W3 impact-only citation did not specify its mechanism.

**Human decision:** Pending (approve corrected / edit / reject).

### Q014 — REVISE

**Original:** Which sources are historical evidence rather than current operational instructions?

**Proposed:** Why should the 2017 s5 report not be treated as interchangeable with later MariaDB and datacenter runbooks when explaining a historical outage?

**Source-grounded reference answer (pending review):** W3 documents what was reported about the 2017 OOM event. W6 describes an evolving troubleshooting procedure, and W7 describes operational switchover practices; their snapshot revisions are from 2026. Such guides provide context but do not establish what was documented or done in 2017. Check document revision dates in the manifest.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W6** · `c77817fef035954f1848` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · This guide is a work in progress. See also MariaDB/monitoring and MariaDB/Backups#Recovering a Snapshot
- **W6** · `49cf0417f9da2f41a15e` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · A master coming back in READ ONLY mode is expected after a crash and it is done to prevent accidental corruption (or even more corruption on a crash).
- **W7** · `a0934f5cd7b39601510b` · [official source](https://wikitech.wikimedia.org/wiki/Switch_Datacenter) · Read-only is a two-step process: we first set MediaWiki itself read-only and then the MediaWiki databases. We allow an amount of time between the two so as to allow the last in-flight edits to land…

**Reason:** Original cited unrelated RAID-WriteThrough guidance; use directly relevant historical and contextual spans.

**Caveat:** The source-revision dates underpinning the temporal answer come from manifest.json, not passages alone.

**Human decision:** Pending (approve corrected / edit / reject).

### Q015 — REVISE

**Original:** What evidence would be required before claiming that a corrective action prevented recurrence?

**Proposed:** Does the presence of a later MariaDB troubleshooting guide prove that the 2021 Commons alert-documentation follow-up was implemented at the time?

**Source-grounded reference answer (pending review):** No. W5 proposes adding responder runbook links (or an action item if documentation is missing). W6 is an available later, work-in-progress troubleshooting guide. Without a verified task/change record and timestamp, these sources alone do not establish when, why or whether an alert link was updated.

**Exact proposed evidence:**
- **W5** · `bc209f1665c6605db0cf` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · Add links to information that someone responding to this alert should have (runbook, plus supporting docs). If that documentation does not exist, add an action item to create it.
- **W6** · `c77817fef035954f1848` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · This guide is a work in progress. See also MariaDB/monitoring and MariaDB/Backups#Recovering a Snapshot
- **W6** · `49cf0417f9da2f41a15e` · [official source](https://wikitech.wikimedia.org/wiki/MariaDB%2FTroubleshooting) · A master coming back in READ ONLY mode is expected after a crash and it is done to prevent accidental corruption (or even more corruption on a crash).

**Reason:** Original generic prevention question could not be answered solely by the cited incident/review passages.

**Human decision:** Pending (approve corrected / edit / reject).

### Q016 — REVISE

**Original:** What does the incident review process say about variable report quality?

**Proposed:** What knowledge-sharing benefit does Wikimedia’s proposed incident-review ritual seek beyond publishing incident reports?

**Source-grounded reference answer (pending review):** W1 proposes regular shared reviews so more engineers become familiar with infrastructure and can challenge misunderstandings and inherited assumptions. The passage is evidence of a proposed process goal, not proof the process was adopted or improved outcomes.

**Exact proposed evidence:**
- **W1** · `c2c53ca85e4a382a3250` · [official source](https://wikitech.wikimedia.org/wiki/Incident_review_ritual) · Sharing knowledge is a big part of the incident review process. The aim is that more people get acquainted with the infrastructure, leading to them feeling more comfortable with it, owning it more…
- **W1** · `9f195aec0d7e5eff5768` · [official source](https://wikitech.wikimedia.org/wiki/Incident_review_ritual) · This is a pretty important part of the ritual. People should ask questions to help them clarify their understanding of the situation and the infrastructure. Better understanding of the infrastructu…

**Reason:** Original citation does not actually state that report quality varies; revise question to what W1’s available text supports.

**Human decision:** Pending (approve corrected / edit / reject).

### Q017 — REVISE

**Original:** What does the incident index provide for historical source discovery?

**Proposed:** How does the Wikimedia incident-status page direct readers toward older incident reports?

**Source-grounded reference answer (pending review):** W10 says it tracks reports about Wikimedia Foundation properties and points readers to the “Incident documentation” category for older incidents. The retrieved excerpt does not establish complete coverage, a precise count, or document quality.

**Exact proposed evidence:**
- **W10** · `d2d0b0e07654cb60c232` · [official source](https://wikitech.wikimedia.org/wiki/Incident_status) · This page tracks incident reports about Wikimedia Foundation properties, such as Wikipedia.
- **W10** · `6757e5281a42baa76930` · [official source](https://wikitech.wikimedia.org/wiki/Incident_status) · Check Category:Incident documentation for older incident reports.

**Reason:** Original quoted only the scope sentence and omitted the actual historical discovery link.

**Human decision:** Pending (approve corrected / edit / reject).

### Q018 — REPLACE

**Original:** What is the response sequence for determining whether a failed host is a master or replica?

**Proposed:** What should the incident coordinator document after an incident is resolved, according to the incident-response runbook?

**Source-grounded reference answer (pending review):** W11 says the incident coordinator should follow post-incident documentation to prepare a report and action items. The provided W11 excerpt does not contain the detailed master-versus-replica diagnostic decision tree; that appears in W6 instead.

**Exact proposed evidence:**
- **W11** · `80bb945916cee8f517a1` · [official source](https://wikitech.wikimedia.org/wiki/Incident_response%2FRunbook) · After an incident is resolved, the incident coordinator should follow the post-incident documentation to write a report and action items.

**Reason:** Original question about database host roles was unsupported by its W11 citation; replace with an answerable W11 control.

**Human decision:** Pending (approve corrected / edit / reject).

### Q019 — REVISE

**Original:** What mechanism caused the 2023 wiki outage draft to affect cache-backed traffic?

**Proposed:** What maintenance mistake triggered the February 2023 draft wiki outage and what traffic impacts are reported?

**Source-grounded reference answer (pending review):** The draft W8 report describes HAProxy maintenance that inadvertently depooled ATS backends in esams/eqiad. It reports errors affecting both cached and uncached requests to backed services, with notable geographic differences and unaffected categories. Preserve draft status and do not generalize its figures beyond that source.

**Exact proposed evidence:**
- **W8** · `911114cca64609a7acb7` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2023-02-22_wiki_outage) · During a routine maintenance consisting of upgrading HAProxy on cache hosts, all of the backends (ATS) in the text cache cluster in esams and eqiad were accidentally depooled due to a mismatch on t…

**Reason:** Original mechanism essentially supported but word “cache-backed traffic” alone obscured the report’s broader impact and draft status.

**Human decision:** Pending (approve corrected / edit / reject).

### Q020 — REPLACE

**Original:** What limitations are visible in the CirrusSearch incident metadata?

**Proposed:** Which search surfaces were affected and unaffected in the November 2021 Commons/CirrusSearch incident?

**Source-grounded reference answer (pending review):** W9 reports that media searches on Commons failed and cross-wiki search-sidebars affected other projects. It separately notes that ordinary search suggestions generally continued to work outside Commons. This does not establish that every Wikipedia search was down.

**Exact proposed evidence:**
- **W9** · `160062b35f38f85c8f2d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-11-10_cirrussearch_commonsfile_outage) · During the incident, all media searches on Wikimedia Commons failed. Wikipedia projects were impacted as well,[1] through the "cross-wiki" feature of the sidebar on Search results pages. This cross…
- **W9** · `0043e6864d6bee6fc619` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-11-10_cirrussearch_commonsfile_outage) · Note that the search suggestions feature, as present on all article pages was not affected (except on Wikimedia Commons itself). The search suggestions field is how how most searches are performed…

**Reason:** Original “limitations in metadata” question cited only an impact passage and was not supported as asked.

**Human decision:** Pending (approve corrected / edit / reject).

### Q021 — REVISE

**Original:** What caused the maps service-capacity incident and how quickly was it detected?

**Proposed:** What capacity condition produced maps request timeouts, and what detection/impact timings are reported?

**Source-grounded reference answer (pending review):** W13 says reimaging the last pooled kartotherian node left codfw with no backend to route to. It reports Icinga alerts beginning at 08:21 and user impact of about six minutes (based on Logstash). The excerpt does not establish the exact first failing request or exact detection delay.

**Exact proposed evidence:**
- **W13** · `46026f4f2587d9195bf6` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2019-06-11_maps) · While https://phabricator.wikimedia.org/T224395 is on which led to depooling codfw. Codfw was pooled back and only two nodes were available (see Incident documentation/20190603-maps). It was necess…
- **W13** · `ec835b9def2e5008f149` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2019-06-11_maps) · Users who were currently served from codfw were affect. They were affected for about 6min(from logstash)

**Reason:** Original demanded “how quickly detected,” which cannot be precisely computed from the cited start alert alone.

**Human decision:** Pending (approve corrected / edit / reject).

### Q022 — REVISE

**Original:** What assumptions and mitigations appear in the planned network maintenance record?

**Proposed:** Why was the May 2011 network maintenance scheduled, and what interruptions were reported during it?

**Source-grounded reference answer (pending review):** W14 describes persistent router slowdowns/packet-loss and a planned router software upgrade. During the scheduled work, the site was intermittently unavailable from reboots, a replica DB went down, and some servers needed recovery after a network-driver problem. A report’s “success” assessment should not erase the documented interruptions.

**Exact proposed evidence:**
- **W14** · `921d9cd7184fdcc304ef` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110524-PlannedMaintenance) · The following day, Mark noticed there were packet losses with that router. Users were again commenting and complaining about page load lag. Upon further investigation, he decided the router softwar…
- **W14** · `259cc4030c52c827786e` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110524-PlannedMaintenance) · The plan to address the router problem was finalized. The maintenance was scheduled on Tuesday, 24th May. The plan consists of:
- **W14** · `39eeaa5ca2e96f48e27d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110524-PlannedMaintenance) · Shortly after 13:00 UTC, Mark started the upgrade. It took 1 hour to perform all but 1 of the above. The Juniper EX stack was not upgraded (not a problem) because he ran out of the maintenance wind…

**Reason:** Original cited only the maintenance-outcome passage, not the motivating conditions or planned mitigations.

**Human decision:** Pending (approve corrected / edit / reject).

### Q023 — REVISE

**Original:** How did a local power event create broader application-service effects?

**Proposed:** How did replacement of a non-production management switch disrupt a rack of production application servers and affect wider services?

**Source-grounded reference answer (pending review):** W15 says proximity to a production access switch caused its power lead to loosen during replacement of a management switch. About forty application servers lost network connectivity; reduced capacity and lost memcached cache contributed to additional load and secondary service disruption.

**Exact proposed evidence:**
- **W15** · `26d7c0c92284f42c0bad` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110926-DBandPower) · Chris, our Tampa data center contractor, was replacing the broken management switch msw-d2-sdtpa in sdtpa rack D2. Our management network is completely unrelated to our production network, and does…
- **W15** · `84b470b585e1dd524380` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110926-DBandPower) · As a result, the entire rack, consisting of about 40 MediaWiki application servers, lost network connectivity. Nagios complained about all servers in the rack, and due to all kinds of second order…
- **W15** · `7cc3fec973d548b81856` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110926-DBandPower) · The main problem with a rack of application servers going down, besides the significant reduction in capacity, is the loss of memcached caching - meaning that MediaWiki on the remaining servers wil…

**Reason:** Original citation described only the physical trigger, not the wider service effects. Note W15 contains multiple incident narratives in one page.

**Human decision:** Pending (approve corrected / edit / reject).

### Q024 — REVISE

**Original:** What mitigation restored the Varnish-related service and what recommendation followed?

**Proposed:** What immediate mitigation restored bits.wikimedia.org after the Varnish overload, and what future improvements were proposed?

**Source-grounded reference answer (pending review):** W16 reports moving bits traffic from Ashburn/EQIAD to Tampa/SDTPA and restarting affected Varnish instances, with service restored. It also says operations planned to investigate automatic failover and overload limits; those were proposals, not proof of completed implementation.

**Exact proposed evidence:**
- **W16** · `6afd4877c61878342f3d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20120120-Varnish) · We redirected the bits.wikimedia.org traffic from our Ashburn (EQIAD) site to our Tampa (SDTPA) site and that resolved the issue instantly. At the same time, we restarted the affected EQIAD Varnish…
- **W16** · `c5071e6eb4debd201546` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20120120-Varnish) · Operations will look into a way to implement an automatic failover solution (from EQIAD to SDTPA and vice-versa). Ops is also investigating limits within varnish to prevent this type of query overl…

**Reason:** Original passage supported recovery but not the claimed recommendation.

**Human decision:** Pending (approve corrected / edit / reject).

### Q025 — REVISE

**Original:** What dependency failure caused the memcached incident and what changed afterward?

**Proposed:** What triggered the memcached failure chain, and what subsequent twemproxy observation was reported?

**Source-grounded reference answer (pending review):** W17 says a failing mc1009 SFP+ module triggered partial switch reboot, blocked application servers on memcached, and cascaded into cache clusters. Later, after routing through twemproxy, a deliberate mc1009 reboot reportedly did not affect site availability or PHP latency, although this remained a provisional rollout and is not proof of permanent resilience.

**Exact proposed evidence:**
- **W17** · `a8e3bb6fa340c465df9c` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20130508-memcached) · We had an outage today, due to a SFP+ module for a single memcached server (mc1009) going bad in a switch, causing the switch to partially reboot, and causing all application servers to get blocked…
- **W17** · `41f855f21482d02cb914` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20130508-memcached) · As of last night, we've been routing all memcached requests in eqiad via twemproxy. A short while ago, I rebooted mc1009 without any other preparation. The main impact was just log noise (libmemcac…
- **W17** · `eb445fcfa4df05b5315f` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20130508-memcached) · The twemproxy deployment is still provisional and needs additional work (mostly around logging and stats collection) but I'm pleased so far and am going to proceed.

**Reason:** Original cited only the later test, not the initiating incident.

**Human decision:** Pending (approve corrected / edit / reject).

### Q026 — REVISE

**Original:** What redundancy and upgrade conditions contributed to the CirrusSearch outage?

**Proposed:** How did redundancy configuration and Elasticsearch versions complicate the November 2013 CirrusSearch recovery?

**Source-grounded reference answer (pending review):** W18 reports that a redundancy setting intended to restore replicas had not taken effect; a node’s data were then removed in the mistaken belief that replicas remained. Later attempts to restore replicas were complicated by errors moving replicas between Elasticsearch 0.90.7 and 0.90.4. Do not infer all the data loss from the initial deletion alone.

**Exact proposed evidence:**
- **W18** · `6d99443f4145afdb35e7` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131118-CirrusSearch) · A few weeks ago we disabled redundancy by default in CirrusSearch because it was causing issues with puppet. We enabled it via configuration in production. This configuration didn't take.
- **W18** · `1103417dec6e33f5f86b` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131118-CirrusSearch) · Around 16:00 UTC to properly set up the partition on the Elasticsearch machines Andrew Otto took down elastic1001 and blasted the data directory and mounted the appropriate disk there. I had assure…
- **W18** · `fea52bd88707620956c1` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131118-CirrusSearch) · At 16:15 UTC icinga warned that Elasticsearch was in "red" state, meaning there were unassigned master shards. I started investigating and I discovered that we'd turned off all the redundancy. The…
- **W18** · `af10e4fd0828a5f6b956` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131118-CirrusSearch) · At 18:09 UTC icinga warned again of Elasticsearch having unassigned master shards. I spent a while digging into this and discovered that there was some kind of error moving replicas from Elasticsea…

**Reason:** Original cited only the node/data deletion and not the broken redundancy config or version issue.

**Human decision:** Pending (approve corrected / edit / reject).

### Q027 — REVISE

**Original:** What chain connected logging, disk pressure, and Parsoid unavailability?

**Proposed:** What failure chain connected verbose logging to Parsoid unavailability and reported user impact?

**Source-grounded reference answer (pending review):** W19 attributes filled disks on roughly three quarters of Parsoid nodes to verbose logging and broken rotation, stopping daemons from accepting requests and creating some VisualEditor errors over a 17-minute interval. The reported percentage is an estimate and should be labeled as such.

**Exact proposed evidence:**
- **W19** · `6271b79698e236830bf6` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20140211-Parsoid) · Verbose logging combined with broken log rotation led to disks on about 3/4 of the Parsoid nodes filling up, which caused the Parsoid daemons to stop accepting requests. This led to some user-visib…

**Reason:** Original passage is well-aligned; tighten the proposed answer to a short, attributed summary.

**Human decision:** Pending (approve corrected / edit / reject).

### Q028 — REVISE

**Original:** How did an rsyslog update cascade from Swift into image services?

**Proposed:** How did the Puppet-managed rsyslog upgrade lead to failures propagating from Swift to image rendering?

**Source-grounded reference answer (pending review):** W20 reports that Puppet upgraded rsyslog, the package restart caused Swift to lose its socket and busy-loop, and overloaded Swift returned errors that affected the imagescaler cluster. The report’s recovery timeline has uncertainty and should not be overinterpreted.

**Exact proposed evidence:**
- **W20** · `15f3723e395e662fecec` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131205-Swift) · rsyslog was automatically upgraded via puppet ("ensure => latest") which triggered a known bug in Swift (media storage) causing it to hang thus cascading down to the imagescalers.
- **W20** · `ec8ddb95dc4939599daf` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131205-Swift) · puppet ran across all boxes in the 30' window; the rsyslog package was upgraded, the package's postinst restarted the service, Swift lost the socket, busy looped, got overloaded and caused all kind…
- **W20** · `77134b9044f2f2d91dc5` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131205-Swift) · Service recovered with no manual action(?) at ~19:40 UTC but still at an increased system load. I fixed this by restarting Swift front/back daemons at about 01:00 UTC.

**Reason:** Original citation addresses propagation, but add triggering context and preserve uncertain recovery attribution.

**Human decision:** Pending (approve corrected / edit / reject).

### Q029 — REVISE

**Original:** What configuration change caused the LVS outage and how was it investigated?

**Proposed:** What sysctl configuration precedence issue caused the LVS outage and why could external checks miss it?

**Source-grounded reference answer (pending review):** W21 attributes failure to a Puppet refactor which lowered the LVS-specific sysctl priority, letting Ubuntu defaults reenable rp_filter. After reboot this broke internal forwarding while many external probes still appeared normal. The operator initially considered and then rejected another suspected HTTPS issue.

**Exact proposed evidence:**
- **W21** · `7042420fad7393cedde5` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20140203-LVS) · This is a big puppet wide change that modularises and improves the handling of sysctl parameter values across our infrastructure. Our LVS balancers rely heavily on specific sysctl settings, includi…
- **W21** · `6025ccc2c63d3591c9e1` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20140203-LVS) · The net effect of this configuration error was that LVS services were broken for _most_ hosts inside of our network after reboot of the respective balancer hosts, but working fine for all external…
- **W21** · `29625b20a33642cfaf10` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20140203-LVS) · Then around 10:55 UTC I moved on to the active LVS balancer, lvs1001 and lvs1002, which are responsible for balancing all public traffic. I failed over traffic to lvs1004 and lvs1005, and verified…
- **W21** · `f75f2242893e48ad271e` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20140203-LVS) · I traced the underlying problem back to this Puppet change: https://gerrit.wikimedia.org/r/#/c/75087/

**Reason:** Original passage discussed initial troubleshooting rather than the eventual root-cause evidence.

**Human decision:** Pending (approve corrected / edit / reject).

### Q030 — REVISE

**Original:** How do the maps and Parsoid incidents differ in affected layer and detection?

**Proposed:** How did the maps and Parsoid outages differ in failed layer, observed impact, and available detection evidence?

**Source-grounded reference answer (pending review):** W13 describes a maps/kartotherian routing-capacity gap during reimaging, request timeouts, Icinga alerting and about six minutes of impact. W19 describes Parsoid daemons refusing requests after log-driven disks filled, affecting VisualEditor users over a reported 17-minute period. W19’s cited passage does not give an exact alert time, so detection speed cannot be compared numerically.

**Exact proposed evidence:**
- **W13** · `46026f4f2587d9195bf6` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2019-06-11_maps) · While https://phabricator.wikimedia.org/T224395 is on which led to depooling codfw. Codfw was pooled back and only two nodes were available (see Incident documentation/20190603-maps). It was necess…
- **W13** · `ec835b9def2e5008f149` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2019-06-11_maps) · Users who were currently served from codfw were affect. They were affected for about 6min(from logstash)
- **W19** · `6271b79698e236830bf6` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20140211-Parsoid) · Verbose logging combined with broken log rotation led to disks on about 3/4 of the Parsoid nodes filling up, which caused the Parsoid daemons to stop accepting requests. This led to some user-visib…

**Reason:** Original Q030 referenced only W13; the revised question requires W19 and discloses missing comparative alert timing.

**Human decision:** Pending (approve corrected / edit / reject).

### Q031 — REVISE

**Original:** How do cache dependency failures differ between Varnish and memcached?

**Proposed:** How did the Varnish overload and mc1009 memcached failure propagate through caching infrastructure by different mechanisms?

**Source-grounded reference answer (pending review):** W16 describes a network bonding/configuration operation that temporarily disrupted Varnish connectivity and overloaded bits servers, mitigated by redirecting traffic. W17 describes a failed SFP+ module and switch disruption affecting a memcached server, blocking applications and cascading into Squid/Varnish. Shared “cache” vocabulary does not imply identical initiating faults.

**Exact proposed evidence:**
- **W16** · `db1aeb1c4ff529500f76` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20120120-Varnish) · After putting in the fix into Puppet and pushing out the interface bonding interface, we had to a "ifdown/ifup" on all the bonded interfaces. When the loss of connectivity happened, the varnish pro…
- **W16** · `6afd4877c61878342f3d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20120120-Varnish) · We redirected the bits.wikimedia.org traffic from our Ashburn (EQIAD) site to our Tampa (SDTPA) site and that resolved the issue instantly. At the same time, we restarted the affected EQIAD Varnish…
- **W17** · `a8e3bb6fa340c465df9c` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20130508-memcached) · We had an outage today, due to a SFP+ module for a single memcached server (mc1009) going bad in a switch, causing the switch to partially reboot, and causing all application servers to get blocked…

**Reason:** Original Q031 cited only W16; add independent W17 evidence.

**Human decision:** Pending (approve corrected / edit / reject).

### Q032 — REVISE

**Original:** How do search-index incidents differ between CirrusSearch and Commons file search?

**Proposed:** How did the 2013 CirrusSearch outage and 2021 Commons-file search failure differ in initiating mechanism and scope?

**Source-grounded reference answer (pending review):** W18 describes disabled/inoperative shard redundancy and deletion of data under an incorrect belief that copies existed; a later version mismatch complicated recovery. W9 describes high-volume queries during bug verification, followed by index deletion/recreation for reasons not fully understood, affecting Commons media search and some cross-wiki search pages. These are different data/index incidents.

**Exact proposed evidence:**
- **W18** · `6d99443f4145afdb35e7` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131118-CirrusSearch) · A few weeks ago we disabled redundancy by default in CirrusSearch because it was causing issues with puppet. We enabled it via configuration in production. This configuration didn't take.
- **W18** · `fea52bd88707620956c1` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131118-CirrusSearch) · At 16:15 UTC icinga warned that Elasticsearch was in "red" state, meaning there were unassigned master shards. I started investigating and I discovered that we'd turned off all the redundancy. The…
- **W9** · `d30c979102e8eaa9b74d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-11-10_cirrussearch_commonsfile_outage) · On 10 November, as part of verifying a bug report, a developer submitted a high volume of search queries against the active production Cirrus cluster (eqiad cirrussearch) via a tunnel from their lo…
- **W9** · `160062b35f38f85c8f2d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-11-10_cirrussearch_commonsfile_outage) · During the incident, all media searches on Wikimedia Commons failed. Wikipedia projects were impacted as well,[1] through the "cross-wiki" feature of the sidebar on Search results pages. This cross…

**Reason:** Original Q032 cited only W9 and mixed two historical search incidents.

**Human decision:** Pending (approve corrected / edit / reject).

### Q033 — REVISE

**Original:** Which incidents show a dependency cascade rather than a direct application defect?

**Proposed:** Which two incident reports show a failure propagating into other services through an intermediate dependency rather than a defect in each affected application?

**Source-grounded reference answer (pending review):** W20 reports Swift socket/busy-loop errors after an rsyslog restart propagating into image rendering. W15 reports network loss to a rack of application servers, reducing capacity and memcached caching, which burdened the remaining application services. These are reported dependency paths, not proof that the same software defect caused both.

**Exact proposed evidence:**
- **W20** · `ec8ddb95dc4939599daf` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131205-Swift) · puppet ran across all boxes in the 30' window; the rsyslog package was upgraded, the package's postinst restarted the service, Swift lost the socket, busy looped, got overloaded and caused all kind…
- **W15** · `84b470b585e1dd524380` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110926-DBandPower) · As a result, the entire rack, consisting of about 40 MediaWiki application servers, lost network connectivity. Nagios complained about all servers in the rack, and due to all kinds of second order…
- **W15** · `7cc3fec973d548b81856` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110926-DBandPower) · The main problem with a rack of application servers going down, besides the significant reduction in capacity, is the loss of memcached caching - meaning that MediaWiki on the remaining servers wil…

**Reason:** Original Q033 had only W20; add a second independent mechanism.

**Human decision:** Pending (approve corrected / edit / reject).

### Q034 — REVISE

**Original:** Which candidate records contain explicit action status and which do not?

**Proposed:** How do the 2012 Varnish and 2013 Swift reports distinguish proposed follow-up from an author-reported change?

**Source-grounded reference answer (pending review):** W16 says automatic failover and Varnish limits were to be investigated, without evidence in that passage that they were completed. W20 states the author had fixed one Swift-related behavior in a linked code change and would examine another upstream issue. A source claim of a fix is not independent evidence of deployment or later effectiveness.

**Exact proposed evidence:**
- **W16** · `c5071e6eb4debd201546` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20120120-Varnish) · Operations will look into a way to implement an automatic failover solution (from EQIAD to SDTPA and vice-versa). Ops is also investigating limits within varnish to prevent this type of query overl…
- **W20** · `20a3d98cab9b3bc21717` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131205-Swift) · Iv'e fixed the evil (3) behavior with https://gerrit.wikimedia.org/r/99576. I'll have a look at (1) and see if it's fixed in newer upstream.

**Reason:** Original W19-only citation could not compare action states; revised answer keeps source attribution.

**Human decision:** Pending (approve corrected / edit / reject).

### Q035 — REVISE

**Original:** Which sources explicitly preserve uncertainty instead of asserting one cause?

**Proposed:** Can GlobalUsage be labeled the conclusively proven root cause of the Commons DB incident, and does the LVS investigation illustrate why initial hypotheses require checking?

**Source-grounded reference answer (pending review):** No. W5 names GlobalUsage as a most probable contributor while retaining underlying causal uncertainty. In W21, the operator initially suspected an HTTPS termination issue before tracing the actual failure to rp_filter/sysctl precedence. Similar diagnostic uncertainty does not mean the technical causes of these incidents were related.

**Exact proposed evidence:**
- **W5** · `8d300bddb41249b0611d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2021-04-27_Commons_wiki_primary_db) · GlobalUsage was signaled as the most probable cause, as it was sending large amount of long-running queries at the moment of the issue to the primary DB server. Because of the general InnoDB error…
- **W21** · `29625b20a33642cfaf10` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20140203-LVS) · Then around 10:55 UTC I moved on to the active LVS balancer, lvs1001 and lvs1002, which are responsible for balancing all public traffic. I failed over traffic to lvs1004 and lvs1005, and verified…
- **W21** · `7042420fad7393cedde5` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20140203-LVS) · This is a big puppet wide change that modularises and improves the handling of sysctl parameter values across our infrastructure. Our LVS balancers rely heavily on specific sysctl settings, includi…

**Reason:** Original cited a Commons summary alone and could not meet a cross-source false-analogy design.

**Human decision:** Pending (approve corrected / edit / reject).

### Q036 — REVISE

**Original:** What evidence supports comparing a planned maintenance event with an unplanned outage?

**Proposed:** How does the documented planned network maintenance in 2011 differ from the accidental backend depooling during 2023 cache maintenance?

**Source-grounded reference answer (pending review):** W14 describes scheduled router work addressing packet loss/latency, with planned reboots and intermittent impact during the window. W8, a draft report, describes HAProxy maintenance which accidentally depooled ATS text-cache backends across sites and caused unexpected request errors. Planned maintenance can still have disruption, but the source-described changes and unexpected failure mechanisms differ.

**Exact proposed evidence:**
- **W14** · `259cc4030c52c827786e` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110524-PlannedMaintenance) · The plan to address the router problem was finalized. The maintenance was scheduled on Tuesday, 24th May. The plan consists of:
- **W14** · `39eeaa5ca2e96f48e27d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20110524-PlannedMaintenance) · Shortly after 13:00 UTC, Mark started the upgrade. It took 1 hour to perform all but 1 of the above. The Juniper EX stack was not upgraded (not a problem) because he ran out of the maintenance wind…
- **W8** · `911114cca64609a7acb7` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2023-02-22_wiki_outage) · During a routine maintenance consisting of upgrading HAProxy on cache hosts, all of the backends (ATS) in the text cache cluster in esams and eqiad were accidentally depooled due to a mismatch on t…

**Reason:** Original Q036 cited only W14; it was not a true comparison. Preserve W8 draft status.

**Human decision:** Pending (approve corrected / edit / reject).

### Q037 — REVISE

**Original:** What evidence supports comparing operational response guidance with historical remediation?

**Proposed:** How does the post-incident reporting obligation in the incident-response runbook relate to the documented Varnish response and proposed follow-ups?

**Source-grounded reference answer (pending review):** W11 states that after resolving an incident the coordinator should prepare an incident report and action items. W16 documents traffic redirection and Varnish restarts during one historical outage, and lists future investigation of automatic failover and overload limits. W11’s current procedure does not prove the historical operators followed it at that time.

**Exact proposed evidence:**
- **W11** · `80bb945916cee8f517a1` · [official source](https://wikitech.wikimedia.org/wiki/Incident_response%2FRunbook) · After an incident is resolved, the incident coordinator should follow the post-incident documentation to write a report and action items.
- **W16** · `6afd4877c61878342f3d` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20120120-Varnish) · We redirected the bits.wikimedia.org traffic from our Ashburn (EQIAD) site to our Tampa (SDTPA) site and that resolved the issue instantly. At the same time, we restarted the affected EQIAD Varnish…
- **W16** · `c5071e6eb4debd201546` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20120120-Varnish) · Operations will look into a way to implement an automatic failover solution (from EQIAD to SDTPA and vice-versa). Ops is also investigating limits within varnish to prevent this type of query overl…

**Reason:** Original Q037 cited only W11; now distinguishes general guidance from actual incident report.

**Human decision:** Pending (approve corrected / edit / reject).

### Q038 — REVISE

**Original:** Which records show that detection speed and remediation speed are separate properties?

**Proposed:** What can and cannot be inferred about detection and restoration timelines from the 2017 s5 and 2013 CirrusSearch incident descriptions?

**Source-grounded reference answer (pending review):** W3 records an impact interval from 05:48 to 07:04 and a recovery after the read-only state was noticed, but the cited passages give no timestamp for the first alert or human recognition. W18 reports an Icinga “red” alert at 16:15, a partial assignment milestone at 17:01, and further recovery work later. The evidence permits reporting these timings, not equating time-to-alert with time-to-full-remediation.

**Exact proposed evidence:**
- **W3** · `bbc3272fd75f7eceaf02` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · The s5 master MySQL process (containing wikidatawiki and dewiki) was killed at 5:48 due to an Out Of Memory error- which lead to the server automatically reboot in read only, recover its data and s…
- **W3** · `a6c5831a40f60dc47c7f` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F2017-07-28_s5_(WikiData_and_dewiki)_read-only) · Wikidata and the German Wikipedia were in read-only mode from 5:48 to 7:04 on 2017-07-28. No edits, user creations were possible between these two timestamps.
- **W18** · `fea52bd88707620956c1` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131118-CirrusSearch) · At 16:15 UTC icinga warned that Elasticsearch was in "red" state, meaning there were unassigned master shards. I started investigating and I discovered that we'd turned off all the redundancy. The…
- **W18** · `2907bf4f46963bf83327` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131118-CirrusSearch) · At 17:01 UTC I got all the shards assigned. They were empty but we were going to perform a rebuild anyway. All elasticsearch wikis were limping along now.
- **W18** · `826085c64bfd7bd69bdd` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20131118-CirrusSearch) · Around 18:40 UTC I configured Elasticsearch to remove any data on those nodes and at 18:50 UTC Elasticsearch recovered again, having assigned all nodes replicas.

**Reason:** Original W3-only evidence could not support a comparison of detection and remediation; W18 provides explicit time points.

**Human decision:** Pending (approve corrected / edit / reject).

### Q039 — REVISE

**Original:** What evidence would be needed to claim that a documented action was operationally effective?

**Proposed:** What does the post-twemproxy mc1009 reboot test show about immediate resilience, and what remains unproven?

**Source-grounded reference answer (pending review):** W17 reports that after traffic was routed via twemproxy a deliberate mc1009 reboot caused no observed site availability or general latency impact during that test. The same report describes the deployment as provisional and still requiring logging/statistics work. This supports one observed improvement, not demonstrated permanent immunity to future memcached failures.

**Exact proposed evidence:**
- **W17** · `41f855f21482d02cb914` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20130508-memcached) · As of last night, we've been routing all memcached requests in eqiad via twemproxy. A short while ago, I rebooted mc1009 without any other preparation. The main impact was just log noise (libmemcac…
- **W17** · `eb445fcfa4df05b5315f` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20130508-memcached) · The twemproxy deployment is still provisional and needs additional work (mostly around logging and stats collection) but I'm pleased so far and am going to proceed.

**Reason:** Original asked hypothetically what evidence would be required without clearly anchoring observed-versus-unproven claims.

**Human decision:** Pending (approve corrected / edit / reject).

### Q040 — REPLACE

**Original:** Which cross-document comparisons remain unsafe until a reviewer confirms the minimum evidence set?

**Proposed:** Does the incident-review ritual alone establish that the proposed Varnish failover and overload measures were implemented?

**Source-grounded reference answer (pending review):** No. W1 proposes shared incident review to improve organizational learning; W16 proposes investigating automatic failover and Varnish limits. The passages contain no verified later implementation or effect record. The system should report the proposal and abstain from claiming completion.

**Exact proposed evidence:**
- **W1** · `c2c53ca85e4a382a3250` · [official source](https://wikitech.wikimedia.org/wiki/Incident_review_ritual) · Sharing knowledge is a big part of the incident review process. The aim is that more people get acquainted with the infrastructure, leading to them feeling more comfortable with it, owning it more…
- **W16** · `c5071e6eb4debd201546` · [official source](https://wikitech.wikimedia.org/wiki/Incidents%2F20120120-Varnish) · Operations will look into a way to implement an automatic failover solution (from EQIAD to SDTPA and vice-versa). Ops is also investigating limits within varnish to prevent this type of query overl…

**Reason:** Original question was meta (“which comparisons remain unsafe until reviewer confirms”) and has no factual gold answer from the cited W1 passage.

**Human decision:** Pending (approve corrected / edit / reject).

## Machine-readable artifact

`ReliabilityGraph_P2_Consolidated_Proposed_Corrections.json` contains all 40 records, exact passage identifiers, source keys, reasons, and explicit `human_approved: false`.

## Recommended Copilot handoff (after reviewer decisions)

> Import only the human-confirmed changes from the consolidated correction artifact. Preserve originals and use the existing schema/validator; keep unapproved entries pending. Verify every passage ID and claim, check incident-family and dev/test leakage, run lint/type/tests and corpus validation, then freeze only if all Gate Q prerequisites are genuinely satisfied. Do not begin P3 until Gate Q passes.
