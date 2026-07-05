# Real Accountant Session Packet

> Date: 2026-07-05
> Status: ready to schedule, not completed feedback evidence

## Purpose

실제 회계사 1명에게 Accounting Intelligence toolkit을 30분 동안 보여주고, 제품이 실제 검토 시간을 줄일
수 있는지와 위험한 부분이 무엇인지 기록한다.

## Packet Files

| File | Role |
|---|---|
| `2026-07-05-session-invite.md` | reviewer에게 보낼 초대/설명 문구 |
| `2026-07-05-reviewer-invite-action-packet.md` | 복사할 invite 문구와 실제 발송 후 ledger update 명령 |
| `2026-07-05-invite-send-receipt.md` | 실제 발송 후 채울 public-safe receipt template/validator |
| `2026-07-05-filled-receipt-guide.md` | 실제 발송 후 receipt 필드 작성, apply, verify 순서 안내 |
| `2026-07-05-invite-receipt-apply.md` | 채워진 receipt 검증 후 ledger sent update를 적용하는 명령 |
| `2026-07-05-post-send-rehearsal-gate.md` | receipt 검증 후 sent ledger 전이를 임시 파일로 rehearsal |
| `2026-07-05-session-evidence-template.md` | 세션 후 public-safe notes 기록 템플릿 |
| `../2026-07-05-accounting-intelligence-next-action.md` | 가장 먼저 할 사용자 결정과 실행 명령만 요약 |
| `../2026-07-05-accounting-intelligence-next-action-sequence-gate.md` | next-action command/after/verify 순서 일관성 검증 |
| `../2026-07-05-accounting-intelligence-decision-queue.md` | 지금 사용자가 결정해야 할 항목과 추천 다음 결정 |
| `../2026-07-05-default-retriever-guard.md` | 기본 retriever가 아직 `hybrid`이고 repair stack은 opt-in인지 검증 |
| `2026-07-05-readiness-index.md` | 전체 RS1~RS4 readiness와 실제 외부 open item 요약 |
| `2026-07-05-external-action-boundary-gate.md` | 내부 readiness 완료 후 다음 repo 작업이 아니라 실제 reviewer 초대 발송이 필요함을 고정 |
| `2026-07-05-invite-dispatch-gate.md` | 초대 발송 전 public-safe packet과 발송 후 ledger update 경로 검증 |
| `2026-07-05-response-handling-gate.md` | 초대 후 follow-up/schedule/decline 응답 처리와 ledger update 경로 검증 |
| `2026-07-05-scheduled-session-gate.md` | 일정 확정 후 세션 당일 실행 경로와 close 차단 조건 검증 |
| `2026-07-05-rs3-capture-readiness-gate.md` | 실제 notes 수령 후 capture/queue/actual manifest/close 경로를 synthetic notes로 검증 |
| `2026-07-05-operator-execution-brief.md` | 초대→스케줄→세션→capture→close까지 실제 운영 순서 압축 브리프 |
| `2026-07-05-pre-send-final-gate.md` | 실제 초대 발송 직전 repo-side readiness와 pre-send boundary 최종 검증 |
| `2026-07-05-after-send-action-matrix.md` | 초대 발송 후 follow-up/schedule/decline 선택지별 ledger 전이와 다음 액션 검증 |
| `2026-07-05-outreach-transition-verify.md` | 현재/발송후 outreach ledger 상태가 올바른 next action으로 라우팅되는지 검증 |
| `2026-07-05-notes-quality-gate.md` | actual notes가 capture/queue/eval 후보로 충분한 품질인지 검증 |
| `2026-07-05-post-session-final-gate.md` | notes safety/quality→capture→actual manifest→completed copied ledger close까지 최종 검증 |
| `2026-07-05-close-state-matrix.md` | ready/actual manifest와 outreach 상태 조합별 close 가능 여부 matrix |
| `session_manifest.json` | 세션 준비 상태와 실제 evidence 여부 |

## Files to Open During Session

1. `docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md`
2. `docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md`
3. `docs/reports/demo-poc/MANIFEST.md`
4. `docs/reports/real-transaction-poc/INDEX.md`
5. `docs/reports/field-feedback-capture/INDEX.md`
6. `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md`
7. `docs/reports/field-feedback/2026-07-05-incorporated-review-questions.md`
8. `docs/reports/2026-07-05-accounting-intelligence-gap-audit.md`
9. `docs/reports/2026-07-05-accounting-intelligence-decision-queue.md`
10. `docs/reports/2026-07-05-espdn1-external-source-connector-post-close-demo-packet-note.md`
11. `docs/reports/2026-07-05-eslrc1-external-source-connector-live-metadata-report-close-gate.md`

## Before Sending

- Reviewer에게 실제 고객자료나 계약 원문을 보내지 말라고 말한다.
- 세션 목적이 도입 결정이 아니라 제품 검증임을 말한다.
- 익명화 거래는 structured facts card로만 받을 수 있다고 말한다.
- 세션 후 notes는 public-safe correction 후보만 queue로 변환한다고 말한다.
- invite 발송/응답 상태는 `outreach-log.sample.jsonl` 형식으로 alias만 기록한다.

## Completion Boundary

이 packet은 세션 준비 산출물이다. 아래가 생기기 전에는 `real-accountant-session` horizon을 close하지 않는다.

- actual reviewer metadata
- actual public-safe feedback notes
- actual capture manifest with `actual_feedback_evidence: true`
- safe feedback queue records generated from the actual notes

## Evidence Check

현재 위치와 다음 액션은 아래 명령으로 먼저 확인한다.

```powershell
python scripts\real_accountant_status.py
python scripts\accounting_intelligence_next_action.py --format text --write
python scripts\accounting_intelligence_next_action_sequence_gate.py --format text --write
python scripts\accounting_intelligence_decision_queue.py --format text --write
python scripts\default_retriever_guard.py --format text --write
python scripts\real_accountant_invite_packet.py --format text --write
python scripts\real_accountant_invite_send_receipt.py --write-template --format text --write
python scripts\real_accountant_filled_receipt_guide.py --format text --write
python scripts\real_accountant_apply_invite_receipt.py --demo-receipt --dry-run --format text --write
python scripts\real_accountant_post_send_rehearsal_gate.py --format text --write
python scripts\real_accountant_readiness_index.py --format text --write
python scripts\real_accountant_external_action_boundary_gate.py --format text --write
```

초대 발송부터 세션 후 capture까지 한 번에 볼 때는 아래 operator brief를 먼저 렌더한다.

```powershell
python scripts\real_accountant_operator_brief.py
```

실제 실행 순서만 압축해서 파일로 남길 때는 아래 execution brief를 쓴다.

```powershell
python scripts\real_accountant_operator_execution_brief.py --format text --write
```

실제 초대 발송 직전에는 아래 final gate로 현재 repo 상태가 아직 pre-send이고 모든 readiness gate가
통과하는지 확인한다.

```powershell
python scripts\real_accountant_pre_send_final_gate.py --format text --write
python scripts\real_accountant_outreach_transition_verify.py --format text --write
```

상태 전이별 close 판단은 아래 matrix로 확인한다. actual-feedback manifest와 completed outreach가 모두
있을 때만 close-ready가 되어야 한다.

```powershell
python scripts\real_accountant_close_state_matrix.py --format text --write
```

세션 당일 운영표는 아래 명령으로 확인한다.

```powershell
python scripts\real_accountant_run_sheet.py
```

세션 직전에는 아래 preflight로 열 파일과 준비 manifest를 확인한다. 산출물을 재생성해야 할 때만
`--run-generators`를 붙인다.

```powershell
python scripts\real_accountant_preflight.py
python scripts\real_accountant_preflight.py --run-generators
```

세션 전에는 아래 명령이 `mode: ready_to_schedule`로 통과해야 한다.

```powershell
python scripts\real_accountant_session_check.py --manifest docs\reports\real-accountant-session\session_manifest.json
```

세션 후에는 같은 checker가 `mode: actual_feedback`로 통과해야 하며, manifest에는 reviewer metadata,
actual notes, capture manifest, queue JSONL이 연결되어 있어야 한다.

actual notes를 capture pipeline에 넣기 전에는 아래 명령이 먼저 통과해야 한다.

```powershell
python scripts\real_accountant_notes_check.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md
python scripts\real_accountant_notes_quality_gate.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md
```

이 checker들은 세션 템플릿의 빈칸, 미확인 boundary checkbox, 고객/회사 식별자 패턴, protected marker가
남아 있거나 scores/positive/risk/missing input/review question/correction candidate가 부족하면 실패한다.

checker가 통과한 actual notes는 아래 명령으로 capture pipeline에 넣는다. 이 명령은
`capture-manifest.json`, `feedback-queue.jsonl`, `capture-report.md`, `feedback-queue-report.md`를 쓴다.

```powershell
python scripts\real_accountant_post_session_final_gate.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md
python scripts\real_accountant_capture.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md --out docs\reports\real-accountant-session
```

세션 직후 notes 작성을 시작할 때는 아래 scaffold를 먼저 만들 수 있다. 이 scaffold는 실제 피드백 내용과
boundary 확인을 채우기 전에는 checker에 실패해야 정상이다.

```powershell
python scripts\real_accountant_notes_scaffold.py --out docs\reports\real-accountant-session\actual-feedback-notes.md --date 2026-07-05 --reviewer-role "CPA reviewer" --reviewer-service-line "F-ACC" --reviewer-experience-context "reviewed accounting advisory workpapers" --session-mode "async review"
```

actual notes, actual capture manifest, queue JSONL이 모두 생긴 뒤에는 수동으로
`actual_feedback_evidence`를 켜지 말고 아래 builder로 actual session manifest를 만든다.

```powershell
python scripts\real_accountant_manifest_build.py --out docs\reports\real-accountant-session\session_manifest.json --notes docs\reports\real-accountant-session\actual-feedback-notes.md --capture-manifest docs\reports\real-accountant-session\capture-manifest.json --queue-jsonl docs\reports\real-accountant-session\feedback-queue.jsonl --reviewer-role "CPA reviewer" --reviewer-service-line "F-ACC" --reviewer-experience-context "reviewed accounting advisory workpapers"
```

horizon을 close하기 전에는 아래 close gate가 통과해야 한다.

```powershell
python scripts\real_accountant_close_check.py --manifest docs\reports\real-accountant-session\session_manifest.json --outreach-ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl --run-quality-preflight
```

## Outreach Check

초대문을 보내기 전에는 아래 명령으로 보낼 본문과 발송 후 ledger 갱신 명령을 확인한다.

```powershell
python scripts\real_accountant_invite_packet.py
```

실제 발송 전에는 아래 gate로 현재 ledger가 아직 `not_sent` 상태인지, 발송 후 update command가 안전하게
`sent` 상태를 만들 수 있는지 확인한다.

```powershell
python scripts\real_accountant_invite_dispatch_gate.py --format text --write
```

초대 발송 후에는 alias 기반 ledger를 아래 명령으로 확인한다.

```powershell
python scripts\real_accountant_outreach_check.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl
```

발송 후 follow-up/schedule/decline 선택지는 아래 matrix로 확인한다.

```powershell
python scripts\real_accountant_after_send_action_matrix.py --format text --write
```

초대 발송 후 ledger가 `sent`로 바뀌었는지는 아래 명령으로 확인한다. 실제 발송 전 기본 sample ledger는
`not_sent` 상태여야 하므로, 발송 후 갱신 ledger 경로를 `--ledger`로 넣는다.

```powershell
python scripts\real_accountant_outreach_transition_verify.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl --expected-status sent --format text
```

초대 후 응답 상황별 follow-up/schedule/decline 문구와 ledger 갱신 명령은 아래 명령으로 출력한다.

```powershell
python scripts\real_accountant_response_packet.py --response follow_up
python scripts\real_accountant_response_packet.py --response schedule
python scripts\real_accountant_response_packet.py --response decline
```

아래 gate로 follow-up/schedule/decline 세 경로가 copied ledger에서 유효한 상태 전이를 만드는지 확인한다.

```powershell
python scripts\real_accountant_response_handling_gate.py --format text --write
```

세션 일정이 잡힌 뒤에는 아래 gate로 copied ledger의 `scheduled` 상태가 세션 당일 실행으로 라우팅되고,
actual feedback evidence 없이는 close gate가 계속 막히는지 확인한다.

```powershell
python scripts\real_accountant_scheduled_session_gate.py --format text --write
```

실제 public-safe notes를 받기 전에는 아래 gate로 synthetic notes가 capture artifact, queue record,
actual-feedback manifest, completed copied ledger close gate까지 이어지는지 확인한다.

```powershell
python scripts\real_accountant_capture_readiness_gate.py --format text --write
```

실제 ledger도 reviewer 실명, 회사명, 고객명, 계약 정보 없이 alias와 상태만 기록한다.

ledger를 직접 편집하지 말고 아래 명령으로 상태를 갱신한다.

```powershell
python scripts\real_accountant_outreach_update.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "invite sent"
```
