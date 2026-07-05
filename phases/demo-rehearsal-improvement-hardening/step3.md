# Step 3: Operator Summary Surface

## 읽어야 할 파일

- `docs/reports/2026-07-05-drq4-demo-improvement-backlog.md` — 왜: DRQ4-3 요구사항의 원천이다.
- `scripts/accounting_intelligence_progress_map.py` — 왜: operator가 현재 상태를 보는 report를 만든다.
- `tests/test_accounting_intelligence_progress_map.py` — 왜: one-screen summary 노출을 검증한다.

## 작업

progress map 상단에 status, current horizon, next action, automation rate, residual risk, primary evidence를 한 화면 요약으로 추가한다.

## Acceptance Criteria

```powershell
python scripts\accounting_intelligence_progress_map.py --format text --write
python -m pytest tests\test_accounting_intelligence_progress_map.py -q
```

## 금지사항

- 새 external action을 next action으로 만들지 마라. 이유: 이 step은 내부 operator 요약 개선이다.
