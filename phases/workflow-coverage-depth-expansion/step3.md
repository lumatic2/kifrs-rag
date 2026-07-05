# Step 3: Minimal Adapter Expansion

## 읽어야 할 파일

- `docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md` - 왜: adapter input/output contract다.

## 작업

최상위 workflow 하나에 대해 minimal decision-prep adapter를 구현한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_workflow_depth_minimal_adapter.py -q
python scripts\workflow_depth_minimal_adapter.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. decision-prep output이 사람 검토 경계를 명시하는지 확인
3. phase index 업데이트

## 금지사항

- 최종 회계판단이나 서명을 AI가 대신한다고 쓰지 마라.
