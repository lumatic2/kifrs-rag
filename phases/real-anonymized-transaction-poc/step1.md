# Step RA1: Horizon and Plan Setup

## 읽어야 할 파일

- `docs/OBJECTIVE.md` - 왜: 실제 피드백/PoC가 objective의 중간 관문임을 확인한다.
- `ROADMAP.md` - 왜: firm-facing brief 다음 추천 horizon을 active로 전환한다.
- `docs/reports/firm-facing-poc/2026-07-05-poc-brief.md` - 왜: PoC ask와 risk boundary를 이어받는다.

## 작업

`real-anonymized-transaction-poc` horizon, plan, phase files를 만든다.

## Acceptance Criteria

```powershell
Test-Path docs\horizons\real-anonymized-transaction-poc.md
Test-Path docs\plans\2026-07-05-real-anonymized-transaction-poc.md
Test-Path phases\real-anonymized-transaction-poc\index.json
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. ROADMAP/OBJECTIVE가 active horizon을 가리키는지 확인한다.
3. RA1을 completed로 업데이트한다.

## 금지사항

- 실제 고객자료, 계약 원문, 기준서 원문, DB, 임베딩을 산출물로 요구하지 않는다.
