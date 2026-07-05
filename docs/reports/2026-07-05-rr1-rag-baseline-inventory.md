# RR1 RAG Baseline Inventory

> Scope: public-safe inventory of current K-IFRS RAG quality commands, evidence reports, and retriever state.

## 한 줄 결론

The current default remains `hybrid`; RAG reliability work can continue with public-safe gates plus one local goldset gate.

## Retriever State

- Runtime default mode: `hybrid`
- Opt-in repair retriever: `ifrs1109_classification_hybrid`
- Opt-in retriever available in eval registry: True
- Opt-in retriever exposed in MCP search modes: False
- Promotion decision: defer
- Promote to default now: False

## Public-Safe Commands

| Name | Command | Purpose |
|---|---|---|
| focused_pytest | `python -m pytest tests/test_eval_gates.py tests/test_authority.py tests/test_authority_source_pack.py tests/test_user_note_v2_runtime.py tests/test_user_notes.py tests/test_user_note_v2_migration.py -q` | Regression tests for eval gates, authority source pack, and user notes. |
| local_rag_threshold_gate | `python scripts/eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format text` | Focused local RAG answer-quality threshold gate. |
| authority_registry | `python scripts/validate_authority_sources.py` | Validate source registry metadata. |
| authority_source_pack | `python scripts/validate_authority_source_pack.py` | Validate authority source pack boundaries. |
| user_note_v2_audit | `python scripts/audit_user_notes.py --source v2 --format json` | Validate user_note v2 trigger and anchor hygiene. |

## Local Data / Protected Boundary Commands

| Name | Command | Local Dependency | Protected Assets Required | Purpose |
|---|---|---|---|---|
| full_retrieval_goldset_gate | `python scripts\rag_quality_final_gate.py --format text` | `data/eval/goldset.json` | True | 50-item retrieval-only gate for the opt-in repair retriever. |
| default_retriever_guard | `python scripts\default_retriever_guard.py --format text` | `cached promotion report` | False | Code-level invariant that keeps MCP search default at hybrid. |

## Existing Evidence Reports

| Report | Path | Present |
|---|---|---|
| rag_quality_refresh_close | `docs/reports/2026-07-05-rag-quality-refresh-close-report.md` | True |
| opt_in_retriever_demo_validation | `docs/reports/2026-07-05-odv1-opt-in-retriever-demo-validation.md` | True |
| promotion_decision_gate | `docs/reports/2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md` | True |
| default_retriever_guard | `docs/reports/2026-07-05-default-retriever-guard.md` | True |

## Minimum RR Verification Set

- `python scripts\quality_preflight.py --format text`
- `python scripts\eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format text`
- `python scripts\default_retriever_guard.py --format text`
- `python scripts\rag_quality_final_gate.py --format text`

## RR2 Input

- Needed: question-type eval matrix and seed coverage split
- Buckets:
  - direct standard lookup
  - judgment and paragraph-combination question
  - workflow seed question
  - disclosure question
  - user_note or source-pack dependent question

## Machine Result

```json
{
  "ok": true,
  "title": "RR1 RAG Baseline Inventory",
  "milestone": "RR1",
  "public_safe_commands": [
    {
      "name": "focused_pytest",
      "command": "python -m pytest tests/test_eval_gates.py tests/test_authority.py tests/test_authority_source_pack.py tests/test_user_note_v2_runtime.py tests/test_user_notes.py tests/test_user_note_v2_migration.py -q",
      "protected_assets_required": false,
      "purpose": "Regression tests for eval gates, authority source pack, and user notes."
    },
    {
      "name": "local_rag_threshold_gate",
      "command": "python scripts/eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format text",
      "protected_assets_required": false,
      "purpose": "Focused local RAG answer-quality threshold gate."
    },
    {
      "name": "authority_registry",
      "command": "python scripts/validate_authority_sources.py",
      "protected_assets_required": false,
      "purpose": "Validate source registry metadata."
    },
    {
      "name": "authority_source_pack",
      "command": "python scripts/validate_authority_source_pack.py",
      "protected_assets_required": false,
      "purpose": "Validate authority source pack boundaries."
    },
    {
      "name": "user_note_v2_audit",
      "command": "python scripts/audit_user_notes.py --source v2 --format json",
      "protected_assets_required": false,
      "purpose": "Validate user_note v2 trigger and anchor hygiene."
    }
  ],
  "local_data_commands": [
    {
      "name": "full_retrieval_goldset_gate",
      "command": "python scripts\\rag_quality_final_gate.py --format text",
      "protected_assets_required": true,
      "local_dependency": "data/eval/goldset.json",
      "purpose": "50-item retrieval-only gate for the opt-in repair retriever."
    },
    {
      "name": "default_retriever_guard",
      "command": "python scripts\\default_retriever_guard.py --format text",
      "protected_assets_required": false,
      "local_dependency": "cached promotion report",
      "purpose": "Code-level invariant that keeps MCP search default at hybrid."
    }
  ],
  "retriever_state": {
    "default_mode": "hybrid",
    "target_retriever": "ifrs1109_classification_hybrid",
    "target_retriever_opt_in_available": true,
    "target_retriever_exposed_in_mcp": false,
    "promotion_decision": "defer",
    "promote_to_default": false,
    "promotion_blockers": [
      "explicit user authorization is required before changing the default retriever"
    ]
  },
  "evidence_reports": [
    {
      "name": "rag_quality_refresh_close",
      "path": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md",
      "present": true
    },
    {
      "name": "opt_in_retriever_demo_validation",
      "path": "docs/reports/2026-07-05-odv1-opt-in-retriever-demo-validation.md",
      "present": true
    },
    {
      "name": "promotion_decision_gate",
      "path": "docs/reports/2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md",
      "present": true
    },
    {
      "name": "default_retriever_guard",
      "path": "docs/reports/2026-07-05-default-retriever-guard.md",
      "present": true
    }
  ],
  "minimum_rr_verification_set": [
    "python scripts\\quality_preflight.py --format text",
    "python scripts\\eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format text",
    "python scripts\\default_retriever_guard.py --format text",
    "python scripts\\rag_quality_final_gate.py --format text"
  ],
  "rr2_input": {
    "needed": "question-type eval matrix and seed coverage split",
    "buckets": [
      "direct standard lookup",
      "judgment and paragraph-combination question",
      "workflow seed question",
      "disclosure question",
      "user_note or source-pack dependent question"
    ]
  },
  "report_path": "docs/reports/2026-07-05-rr1-rag-baseline-inventory.md"
}
```
