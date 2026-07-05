# Step 1: Retriever Timing Threshold

## 읽어야 할 파일

- `docs/reports/2026-07-05-drq4-demo-improvement-backlog.md` — 왜: DRQ4-1 요구사항의 원천이다.
- `scripts/demo_run_quality_checklist.py` — 왜: stage별 timing check를 렌더한다.
- `tests/test_demo_run_quality_checklist.py` — 왜: threshold 노출을 검증한다.

## 작업

`retriever-decision` stage에 explicit timing variance threshold를 추가하고 report에 보이게 한다.

## Acceptance Criteria

```powershell
python scripts\demo_run_quality_checklist.py --format text --write
python -m pytest tests\test_demo_run_quality_checklist.py -q
```

## 금지사항

- default retriever 동작을 바꾸지 마라. 이유: 이 step은 rehearsal evidence hardening이다.
