# Changeset

## Target

- ROADMAP milestone: `real-accountant-session` RS2/RS3 state guidance
- Plan: `docs/plans/2026-07-05-real-accountant-session.md`

## Scope

- Files: `scripts/accounting_intelligence_next_action.py`, `tests/test_accounting_intelligence_next_action.py`
- Reason: next-action guidance must stay correct after the reviewer invite is sent and the outreach ledger changes state.
- Expected effect: `sent`, `scheduled`, and `completed` reviewer states are covered by focused next-action tests.

## Contract

- Source of truth: decision queue output remains the source for next-action guidance.
- Compatibility: current CLI behavior and report format stay unchanged.
- Out of scope: mutating the actual outreach ledger or sending reviewer messages.

## Verification

- [x] Targeted tests: next-action state coverage
- [x] CLI smoke: current next-action text output
- [x] Integrated smoke: quality preflight
- [x] Dirty-tree review: `git diff --check` and `git status`

## Result

- Status: completed
- Evidence: `tests/test_accounting_intelligence_next_action.py`
- Notes: current CLI output remains `send_reviewer_invite`; post-invite states are now covered without mutating the real ledger.
