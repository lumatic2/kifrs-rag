# Step RS2: Run Actual Accountant Session

## 읽어야 할 파일

- `docs/reports/real-accountant-session/SESSION_PACKET.md` - 왜: 세션 순서와 열 파일 목록.
- `docs/reports/field-feedback-runbook/2026-07-05-operator-checklist.md` - 왜: 진행자 체크리스트.

## 작업

실제 회계사 1명과 30분 세션을 진행하고 public-safe notes를 남긴다.

## Acceptance Criteria

```powershell
Test-Path docs\reports\real-accountant-session\actual-feedback-notes.md
python scripts\real_accountant_outreach_check.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl
```

## 검증 절차

1. reviewer role/service-line metadata가 있는지 확인한다.
2. raw contract/customer identifier가 없는지 확인한다.
3. outreach ledger가 `scheduled` 또는 `completed` 상태를 포함하는지 확인한다.
4. RS2를 completed로 업데이트한다.

## 금지사항

- raw contract, customer identifier, copied source body, private filing을 repo에 저장하지 않는다.
