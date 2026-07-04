# Step RS2: Run Actual Accountant Session

## 읽어야 할 파일

- `docs/reports/real-accountant-session/SESSION_PACKET.md` - 왜: 세션 순서와 열 파일 목록.
- `docs/reports/field-feedback-runbook/2026-07-05-operator-checklist.md` - 왜: 진행자 체크리스트.

## 작업

실제 회계사 1명과 30분 세션을 진행하고 public-safe notes를 남긴다.

## Acceptance Criteria

```powershell
python scripts\real_accountant_invite_packet.py
python scripts\real_accountant_run_sheet.py
python scripts\real_accountant_outreach_update.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08
python scripts\real_accountant_notes_scaffold.py --out docs\reports\real-accountant-session\actual-feedback-notes.md --date 2026-07-05 --reviewer-role "CPA reviewer" --reviewer-service-line "F-ACC" --reviewer-experience-context "reviewed accounting advisory workpapers" --session-mode "async review"
Test-Path docs\reports\real-accountant-session\actual-feedback-notes.md
python scripts\real_accountant_notes_check.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md
python scripts\real_accountant_outreach_check.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl
```

## 검증 절차

1. invite packet이 public-safe alias와 발송 후 ledger 갱신 명령을 출력하는지 확인한다.
2. run sheet가 세션 전 preflight, 열 파일, 질문, 세션 후 명령을 출력하는지 확인한다.
3. notes scaffold가 작성 시작점으로 생성되는지 확인한다.
4. reviewer role/service-line metadata가 있는지 확인한다.
5. raw contract/customer identifier가 없는지 확인한다.
6. actual feedback notes checker가 통과하는지 확인한다.
7. outreach ledger가 `scheduled` 또는 `completed` 상태를 포함하는지 확인한다.
8. RS2를 completed로 업데이트한다.

## 금지사항

- raw contract, customer identifier, copied source body, private filing을 repo에 저장하지 않는다.
