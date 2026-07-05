# Changeset

## Target

- ROADMAP milestone: Accounting Intelligence Expansion technical guardrail
- Plan: `docs/horizons/accounting-intelligence-expansion.md`

## Scope

- Files:
  - `scripts/default_retriever_guard.py`
  - `tests/test_default_retriever_guard.py`
  - `docs/reports/2026-07-05-default-retriever-guard.md`
  - `scripts/accounting_intelligence_gap_audit.py`
  - `tests/test_accounting_intelligence_gap_audit.py`
  - `docs/reports/real-accountant-session/SESSION_PACKET.md`
  - `docs/reports/field-feedback-runbook/2026-07-05-operator-checklist.md`
- Reason: the opt-in repair retriever has strong retrieval metrics, but product policy says it must not become the default before actual accountant evidence and explicit authorization.
- Expected effect: accidental runtime default promotion is detected by a fast code-level guard.

## Contract

- Source of truth: `kifrs/mcp_server.py` search default and `kifrs/eval/retrieval.py` opt-in retriever registry.
- Compatibility: does not change default runtime search behavior.
- Out of scope: changing MCP search modes, promoting default retriever, or overriding promotion blockers.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_default_retriever_guard.py -q`
- [x] CLI smoke: `python scripts\default_retriever_guard.py --format text --write`
- [x] Integrated smoke: `python -m pytest tests\test_default_retriever_guard.py tests\test_opt_in_retriever_promotion_decision_gate.py tests\test_real_accountant_run_sheet.py tests\test_accounting_intelligence_gap_audit.py -q`; `python scripts\quality_preflight.py --format text`; `python scripts\accounting_intelligence_gap_audit.py --format text --write`
- [x] Dirty-tree review: `git diff --check`; `git status --short --branch`

## Result

- Status: completed
- Evidence: `docs/reports/2026-07-05-default-retriever-guard.md`
- Notes: Guard verifies MCP default stays `hybrid`, target retriever stays out of MCP modes, and ORPD cached decision remains defer.
