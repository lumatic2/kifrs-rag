# Step 2: Rehearsal Freshness Metadata

## 읽어야 할 파일

- `docs/reports/2026-07-05-drq4-demo-improvement-backlog.md` — 왜: DRQ4-2 요구사항의 원천이다.
- `scripts/demo_rehearsal_evidence_capture.py` — 왜: rehearsal stage evidence를 만든다.
- `tests/test_demo_rehearsal_evidence_capture.py` — 왜: freshness metadata와 freshness check를 검증한다.

## 작업

stage results와 report에 generated-at freshness metadata와 stale-output check를 추가한다.

## Acceptance Criteria

```powershell
python scripts\demo_rehearsal_evidence_capture.py --format text --write
python -m pytest tests\test_demo_rehearsal_evidence_capture.py -q
```

## 금지사항

- 실제 private participant data를 만들지 마라. 이유: rehearsal evidence는 public-safe fixture다.
