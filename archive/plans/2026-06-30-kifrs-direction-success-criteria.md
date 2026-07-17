# kifrs-rag Direction and Success Criteria

> Created: 2026-06-30
> Purpose: keep the next work bounded by a clear plan and stop criteria.

## Direction

`kifrs-rag` is not just a standards search bot. The target is a personal K-IFRS accounting engine that can produce evidence-backed accounting work products:

- classification judgments;
- journal entry reasoning;
- review memos;
- disclosure or note drafting support;
- exam-style and practice-style explanations.

The current shift is from "make more scenarios" to "make quality repeatable." Phase 4 already produced useful dogfood across leases, revenue, fair value, and employee benefits. The next work should make those gains operational: measurable evaluation, typed user notes, authority-aware evidence, and guarded regression checks.

## Operating Plan

### Stage 1 — Stabilize the quality loop

Status: mostly done by EQ1 and EQ2.

Goal: every quality improvement must have a local command, a focused test, and an evidence artifact.

Done when:

- automatic grading can pass/fail selected cases by threshold;
- authority sources are typed and validated without committing protected text;
- user notes are audited and can be migrated without deleting legacy data;
- integrated smoke proves the loop still works.

### Stage 2 — Make `user_note_v2` the operating layer

Status: completed by `EQ4`.

Goal: turn user notes from ad hoc patches into a structured runtime quality layer.

Scope:

- decide whether v2 is the source of truth for new notes;
- route new seed/write/read paths through the v2 shape;
- preserve backward-compatible reads from legacy `user_note`;
- keep conflict/dead-anchor audit as a required check.

Stop condition:

- stop before any destructive migration;
- stop before replacing legacy reads without a passing compatibility smoke.

### Stage 3 — Turn authority metadata into a source pack

Status: completed by `EQ3`.

Goal: define how K-IFRS primary evidence, KASB material, FSS inquiry, commercial law, tax boundary, and exam convention sources are discovered and ranked.

Scope:

- document allowed source types and priorities;
- store metadata and links only;
- define validation for freshness, authority type, and allowed usage;
- keep source body text out of git.

Stop condition:

- stop before committing third-party source body text;
- stop before treating external authority as equal to K-IFRS primary text.

### Stage 4 — Broaden evaluation only after the loop is stable

Status: initial preflight/CI hook completed by `EQ5`.

Goal: expand from focused local smoke to a durable regression suite.

Scope:

- connect more goldset items and scenario traces;
- add CI/preflight gating only after thresholds are stable;
- record every accepted regression threshold in a plan or changeset.

Stop condition:

- stop if a metric improves only because `local-rag` is echoing gold anchors;
- stop if a gate would create noisy failures without a clear owner action.

### Stage 5 — Resume scenario expansion with quality gates attached

Goal: add new accounting domains only when the quality loop can catch regressions.

Preferred domains:

- 1036 impairment;
- consolidation;
- fair value extensions;
- revenue and lease edge cases;
- tax/commercial-law boundary cases.

Stop condition:

- stop if the scenario cannot produce reusable evidence: citation map, retrieval trace, work product, and review memo.

## Success Criteria

### A. Accounting correctness

Success means the answer cites the right standard paragraphs and applies them to the transaction without hiding judgment calls.

Minimum evidence:

- cited paragraph IDs exist in the local DB;
- cited text matches the PDF/parser source when checked;
- review memo names assumptions, boundary cases, and unsupported areas.

### B. Repeatable evaluation

Success means quality can be checked by command, not memory.

Minimum evidence:

- targeted quality gate passes selected cases;
- failure output names the failing item and metric;
- threshold changes are recorded in a plan or changeset.

### C. Runtime learning

Success means recurring failures become typed notes or backlog items, not one-off chat memory.

Minimum evidence:

- every promoted note has type, trigger, expansion/rationale, source, and anchor;
- note audit catches dead anchors or malformed records;
- legacy notes still work during migration.

### D. Authority boundaries

Success means external material improves judgment without polluting primary K-IFRS evidence.

Minimum evidence:

- every external source has type, priority, and allowed usage;
- source registry contains metadata only;
- answer flow can distinguish primary evidence from supporting authority.

### E. Public/private boundary

Success means the public repo remains shareable.

Minimum evidence:

- no K-IFRS PDFs, parsed text, embeddings, DB dumps, or dogfood source questions are committed;
- public artifacts are code, architecture, metrics, plans, and smoke outputs;
- protected local assets remain ignored.

## Current Next Step

Do not start another implementation automatically.

The current Engine Quality Ops scope is complete through:

- automatic grading threshold gate;
- `user_note_v2` runtime layer;
- metadata-only authority source pack;
- public-safe quality preflight and CI hook.

The next implementation should begin only after choosing a new bounded target, either a new horizon or a deliberate return to Phase 4 scenario expansion.
