# Step 4: Horizon Close Gate

## 읽어야 할 파일

- `docs/horizons/demo-rehearsal-improvement-hardening.md` — 왜: close 기준이다.
- `docs/plans/2026-07-06-demo-rehearsal-improvement-hardening.md` — 왜: DRI1~DRI3 step tree다.
- `docs/reports/2026-07-05-drq2-demo-run-quality-checklist.md` — 왜: DRI1 evidence다.
- `docs/reports/2026-07-05-drq3-demo-rehearsal-evidence.md` — 왜: DRI2 evidence다.
- `docs/reports/2026-07-05-accounting-intelligence-progress-map.md` — 왜: DRI3 evidence다.

## 작업

DRI1~DRI3 evidence를 확인하고 close report를 생성한다. ROADMAP, horizon doc, plan doc, phase index를 closed 상태로 동기화한다.

## Acceptance Criteria

```powershell
python scripts\demo_rehearsal_improvement_close_gate.py --format text --write
python -m pytest tests\test_demo_rehearsal_improvement_close_gate.py -q
```

## 금지사항

- close report에서 field validation을 주장하지 마라. 이유: 이 horizon은 internal hardening이다.
