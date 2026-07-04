# Step WR3: Rebuild Report Command

## 읽어야 할 파일

- `kifrs/workflows/source_aware_rebuild.py` - 왜: WR2 analyzer를 command에서 호출한다.
- `scripts/demo_poc.py` - 왜: 기존 public-safe report generation 스타일을 맞춘다.
- `docs/reports/demo-poc/MANIFEST.md` - 왜: public-safe 출력 경계를 유지한다.

## 작업

`scripts/workflow_rebuild_report.py`를 추가해 source-aware rebuild report를 markdown으로 재생성한다.
기본 출력은 `docs/reports/2026-07-05-wr3-source-aware-rebuild-report.md`이다.

## Acceptance Criteria

```powershell
python scripts\workflow_rebuild_report.py --out docs\reports\2026-07-05-wr3-source-aware-rebuild-report.md
Test-Path docs\reports\2026-07-05-wr3-source-aware-rebuild-report.md
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. report가 1109/1115/1116을 모두 포함하는지 확인한다.
3. `phases/workflow-rebuild-on-richer-knowledge/index.json`의 WR3를 completed로 업데이트한다.

## 금지사항

- report에 원문 body나 raw filing을 붙이지 않는다.
- 회계 결론이 확정됐다고 쓰지 않는다. reason: 사람 검토 boundary 유지.
