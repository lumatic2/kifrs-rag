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
| `2026-07-05-session-evidence-template.md` | 세션 후 public-safe notes 기록 템플릿 |
| `session_manifest.json` | 세션 준비 상태와 실제 evidence 여부 |

## Files to Open During Session

1. `docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md`
2. `docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md`
3. `docs/reports/demo-poc/MANIFEST.md`
4. `docs/reports/real-transaction-poc/INDEX.md`
5. `docs/reports/field-feedback-capture/INDEX.md`
6. `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md`
7. `docs/reports/field-feedback/2026-07-05-incorporated-review-questions.md`

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
```

초대 발송부터 세션 후 capture까지 한 번에 볼 때는 아래 operator brief를 먼저 렌더한다.

```powershell
python scripts\real_accountant_operator_brief.py
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
```

이 checker는 세션 템플릿의 빈칸, 미확인 boundary checkbox, 고객/회사 식별자 패턴, protected marker가
남아 있으면 실패한다.

checker가 통과한 actual notes는 아래 명령으로 capture pipeline에 넣는다. 이 명령은
`capture-manifest.json`, `feedback-queue.jsonl`, `capture-report.md`, `feedback-queue-report.md`를 쓴다.

```powershell
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

초대 발송 후에는 alias 기반 ledger를 아래 명령으로 확인한다.

```powershell
python scripts\real_accountant_outreach_check.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl
```

초대 후 응답 상황별 follow-up/schedule/decline 문구와 ledger 갱신 명령은 아래 명령으로 출력한다.

```powershell
python scripts\real_accountant_response_packet.py --response follow_up
python scripts\real_accountant_response_packet.py --response schedule
python scripts\real_accountant_response_packet.py --response decline
```

실제 ledger도 reviewer 실명, 회사명, 고객명, 계약 정보 없이 alias와 상태만 기록한다.

ledger를 직접 편집하지 말고 아래 명령으로 상태를 갱신한다.

```powershell
python scripts\real_accountant_outreach_update.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "invite sent"
```
