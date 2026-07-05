# Changeset

## Target

- ROADMAP milestone: `real-accountant-session` RS2 operator guidance
- Plan: `docs/plans/2026-07-05-real-accountant-session.md`

## Scope

- Files: decision queue, next-action CLI/report, focused tests
- Reason: next-action should show the post-send ledger update command directly instead of forcing the operator to open the invite packet first.
- Expected effect: current next-action exposes command -> after -> verify for the reviewer invite path.

## Contract

- Source of truth: reviewer state in the decision queue.
- Compatibility: `next_command` and `verify_command` remain unchanged; `after_command` is additive.
- Out of scope: actually sending the invite or mutating the outreach ledger.

## Verification

- [x] Targeted tests: decision queue + next-action
- [x] CLI/report smoke: regenerate next-action and decision queue
- [x] Integrated smoke: quality preflight
- [x] Dirty-tree review: `git diff --check` and `git status`

## Result

- Status: completed
- Evidence: `docs/reports/2026-07-05-accounting-intelligence-next-action.md`
- Notes: current next-action now shows command, after-command, and verify-command for the reviewer invite path.
