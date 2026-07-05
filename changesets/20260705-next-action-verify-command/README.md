# Changeset

## Target

- ROADMAP milestone: `real-accountant-session` RS2 operator guidance
- Plan: `docs/plans/2026-07-05-real-accountant-session.md`

## Scope

- Files: decision queue, next-action CLI/report, focused tests
- Reason: the operator-facing next action should show both the action command and the verification command.
- Expected effect: after manual invite dispatch, the expected `sent` verification command is visible without opening deeper packet docs.

## Contract

- Source of truth: decision queue reviewer state still drives next-action output.
- Compatibility: existing `next_command` semantics stay unchanged; `verify_command` is additive.
- Out of scope: sending invites or mutating ledgers.

## Verification

- [x] Targeted tests: decision queue + next-action
- [x] CLI/report smoke: regenerate next-action and decision queue
- [x] Integrated smoke: quality preflight
- [x] Dirty-tree review: `git diff --check` and `git status`

## Result

- Status: completed
- Evidence: `docs/reports/2026-07-05-accounting-intelligence-next-action.md`
- Notes: next-action now shows `real_accountant_outreach_transition_verify.py --expected-status sent` for the current invite step.
