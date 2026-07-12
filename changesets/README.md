# Tooling Changesets

| # | Changeset | Date | Scope | Verification | Status |
|---|---|---|---|---|---|
| 1 | `20260630-user-note-quality` | 2026-06-30 | user_note parser/audit/smoke | 4/4 | completed |
| 2 | `20260630-auto-grading` | 2026-06-30 | deterministic local grading loop | 4/4 | completed |
| 3 | `20260630-authority-index` | 2026-06-30 | external authority registry/index | 4/4 | completed |
| 4 | `20260630-auto-grading-expanded` | 2026-06-30 | threshold gate + broader local grading | 4/4 | completed |
| 5 | `20260630-authority-source-pack` | 2026-06-30 | metadata-only authority source pack | 4/4 | completed |
| 6 | `20260630-user-note-schema-v2` | 2026-06-30 | backward-compatible user_note v2 migration | 4/4 | completed |
| 7 | `20260630-user-note-v2-runtime` | 2026-06-30 | v2-priority user_note write/read runtime | 4/4 | completed |
| 8 | `20260630-authority-source-pack-rules` | 2026-06-30 | document-level authority source pack rules | 4/4 | completed |
| 9 | `20260630-quality-preflight-ci` | 2026-06-30 | public-safe quality preflight + CI hook | 4/4 | completed |
| 10 | `20260703-engine-test-safety-net` | 2026-07-03 | mcp_server.py/embed.py retrieval test coverage | 4/4 | completed |
| 11 | `20260703-engine-perf-refactor` | 2026-07-03 | search_reranked N+1 fix + embedding/centroid caching | 4/4 | completed |
| 12 | `20260703-mcp-server-dedup-errors` | 2026-07-03 | mcp_server.py dual-backend dedup + ToolError + startup DB check | 4/4 | completed |
| 13 | `20260703-mcp-search-tool-consolidation` | 2026-07-03 | 5 search tools -> single search(mode=...) + /accounting sync | 4/4 | completed |
| 14 | `20260703-term-bridge-user-note-migration` | 2026-07-03 | TERM_BRIDGE dict -> user_note_v2 seed rows | 4/4 | completed |
| 15 | `20260705-accounting-intelligence-next-action` | 2026-07-05 | single next-action CLI/report from decision queue | 4/4 | completed |
| 16 | `20260705-next-action-state-coverage` | 2026-07-05 | next-action tests for post-invite reviewer states | 4/4 | completed |
| 17 | `20260705-decision-queue-ledger-args` | 2026-07-05 | decision queue and next-action ledger path args | 4/4 | completed |
| 18 | `20260705-outreach-transition-verify` | 2026-07-05 | verify outreach ledger state routes to next action | 4/4 | completed |
| 19 | `20260705-outreach-transition-verify-wiring` | 2026-07-05 | wire outreach transition verifier into session packet/gap audit | 4/4 | completed |
| 20 | `20260705-next-action-verify-command` | 2026-07-05 | show verification command in decision queue and next-action | 4/4 | completed |
| 21 | `20260705-next-action-after-command` | 2026-07-05 | show post-action command in decision queue and next-action | 4/4 | completed |
| 22 | `20260705-next-action-sequence-gate` | 2026-07-05 | gate command-after-verify next-action sequence | 4/4 | completed |
| 23 | `20260705-invite-send-receipt` | 2026-07-05 | public-safe manual invite send receipt contract | 4/4 | completed |
| 24 | `20260705-next-action-receipt-command` | 2026-07-05 | show invite receipt command in next-action sequence | 4/4 | completed |
| 25 | `20260705-post-send-rehearsal-gate` | 2026-07-05 | rehearse receipt-to-sent ledger transition | 4/4 | completed |
| 26 | `20260705-invite-receipt-apply` | 2026-07-05 | apply sent ledger update only after receipt validation | 4/4 | completed |
| 27 | `20260705-next-action-apply-after` | 2026-07-05 | route next-action after step through receipt apply | 4/4 | completed |
| 28 | `20260705-filled-receipt-guide` | 2026-07-05 | operator guide for filling post-send receipt | 4/4 | completed |
| 29 | `20260705-default-retriever-guard` | 2026-07-05 | code guard that keeps repair retriever opt-in | 4/4 | completed |
| 30 | `20260705-progress-map` | 2026-07-05 | objective horizon progress map for operator clarity | 4/4 | completed |
| 31 | `20260712-ib1-repricing-term-bridge` | 2026-07-12 | H4 issue-back: repricing term_bridge seeds (IB1-a) | 4/4 | completed |
| 32 | `20260712-ib1-standard-filter-guidance` | 2026-07-12 | standard filter trap guidance on tool+skill surfaces (IB1-b) | 4/4 | completed |
| 33 | `20260712-ib2-parse-bc-sections` | 2026-07-12 | BC/DO/IN paragraph split + section title repair + BC demotion (IB2) | 4/4 | completed |
| 34 | `20260712-dr1-drift-detection-core` | 2026-07-12 | KASB drift detection core `kifrs/drift.py` + CLI (DR1-S1) | 4/4 | completed |
| 35 | `20260712-dr1-check-drift-mcp-tool` | 2026-07-12 | MCP tool check_drift + /accounting drift guidance (DR1-S2) | 4/4 | completed |
| 36 | `20260712-dr2-unit-update-path` | 2026-07-12 | per-standard update path --update + amendment diff (DR2-S1) | 4/4 | completed |
| 37 | `20260712-dr2-report-update-link` | 2026-07-12 | drift report update_cmd link + full-loop close verify (DR2-S2) | 4/4 | completed |
| 38 | `20260712-dr3-scheduled-drift-check` | 2026-07-12 | PENDING state + weekly Task Scheduler registration (DR3-S1) | 4/4 | completed |
| 39 | `20260712-dr3-mcp-drift-warning` | 2026-07-12 | MCP drift_warning auto-annotation on search/get_paragraph (DR3-S2) | 4/4 | completed |
| 40 | `20260712-pv1-web-data-export` | 2026-07-12 | web metadata export + public-safe gate (PV1-S1) | 4/4 | completed |
