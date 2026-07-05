# Field Feedback Operator Checklist

> Use with: `2026-07-05-30min-session-runbook.md`

## Preflight

- [ ] `python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc`
- [ ] `python scripts\real_transaction_poc.py --out docs\reports\real-transaction-poc`
- [ ] `python scripts\feedback_incorporation_report.py --queue docs\reports\real-transaction-poc\feedback-queue.jsonl --out docs\reports\2026-07-05-af3-feedback-incorporation-report.md --questions-out docs\reports\field-feedback\2026-07-05-incorporated-review-questions.md`
- [ ] `python scripts\accounting_intelligence_progress_map.py --format text --write`
- [ ] `python scripts\accounting_intelligence_next_action.py --format text --write`
- [ ] `python scripts\accounting_intelligence_next_action_sequence_gate.py --format text --write`
- [ ] `python scripts\accounting_intelligence_decision_queue.py --format text --write`
- [ ] `python scripts\default_retriever_guard.py --format text --write`
- [ ] `python scripts\real_accountant_invite_packet.py --format text --write`
- [ ] `python scripts\real_accountant_invite_send_receipt.py --write-template --format text --write`
- [ ] `python scripts\real_accountant_filled_receipt_guide.py --format text --write`
- [ ] `python scripts\real_accountant_apply_invite_receipt.py --demo-receipt --dry-run --format text --write`
- [ ] `python scripts\real_accountant_post_send_rehearsal_gate.py --format text --write`
- [ ] `python scripts\real_accountant_readiness_index.py --format text --write`
- [ ] `python scripts\real_accountant_external_action_boundary_gate.py --format text --write`
- [ ] `python scripts\real_accountant_invite_dispatch_gate.py --format text --write`
- [ ] `python scripts\real_accountant_response_handling_gate.py --format text --write`
- [ ] `python scripts\real_accountant_scheduled_session_gate.py --format text --write`
- [ ] `python scripts\real_accountant_capture_readiness_gate.py --format text --write`
- [ ] `python scripts\real_accountant_operator_execution_brief.py --format text --write`
- [ ] `python scripts\real_accountant_pre_send_final_gate.py --format text --write`
- [ ] `python scripts\real_accountant_outreach_transition_verify.py --format text --write`
- [ ] `python scripts\real_accountant_after_send_action_matrix.py --format text --write`
- [ ] `python scripts\real_accountant_notes_quality_gate.py --format text --write`
- [ ] `python scripts\real_accountant_post_session_final_gate.py --format text --write`
- [ ] `python scripts\real_accountant_close_state_matrix.py --format text --write`
- [ ] Open one-page brief.
- [ ] Open demo manifest.
- [ ] Open real-transaction PoC index.
- [ ] Open feedback questionnaire and incorporated review questions.

## Opening Script

- [ ] "이건 최종 회계판단 자동화가 아니라 결정준비 초안 도구입니다."
- [ ] "기준서 원문, DB, 임베딩, 고객자료는 공개 repo에 없습니다."
- [ ] "오늘 목표는 도입 결정이 아니라 실제 검토 시간을 줄일 부분과 위험한 부분을 찾는 것입니다."

## During Session

- [ ] Ask whether F-ACC is the right first target.
- [ ] Ask whether the review pack order matches actual work.
- [ ] Ask whether evidence boundary is clear.
- [ ] Ask which input facts are missing.
- [ ] Ask which human-review questions are useful or useless.
- [ ] Ask what should become eval seed vs backlog.

## Close

- [ ] Capture one strongest positive.
- [ ] Capture one strongest risk.
- [ ] Capture one required input addition.
- [ ] Capture one review question addition.
- [ ] Ask whether an anonymized real transaction can be provided.

## After Session

- [ ] Write feedback notes outside protected-data paths.
- [ ] Convert safe corrections to queue records only if they contain no raw contract/customer identifiers.
- [ ] Regenerate incorporation report.
- [ ] Decide next horizon.
