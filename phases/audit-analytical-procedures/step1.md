# Step 1: analytical-procedure-scope-fixture-inventory

Status: pending

## 읽어야 할 파일

- `docs/horizons/f-audit-analytical-procedures.md` — 왜: horizon 목표와 boundary가 있다.
- `docs/practice-map/team-workflows.md` — 왜: F-AUD workflow에서 분석적 절차가 어디에 들어가는지 확인한다.
- `docs/horizons/f-acc-technical-expansion.md` — 왜: F-ACC 다음 순서로 F-AUD를 왜 선택했는지 sequence가 있다.
- `docs/reports/2026-07-05-fs5-statement-draft-report.md` — 왜: F-ACC statement draft output과 감사 분석 memo 연결 지점을 확인한다.

## 작업

감사 분석적 절차 PoC의 입력 fixture 범위를 정한다. 공개 DART F/S 의존 없이 먼저 synthetic F/S fixture로
닫을 수 있는 line item, ratio, trend, anomaly 후보를 inventory로 정리한다.

## Acceptance Criteria

```powershell
git diff --check
```

## 결과물

- `docs/reports/2026-07-05-ap1-analytical-procedure-scope-inventory.md`
