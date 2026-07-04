# Step TK2: Readiness Checker

## 읽어야 할 파일

- `docs/toolkit/readiness_manifest.json` - 왜: checker가 읽을 계약이다.
- `scripts/quality_preflight.py` - 왜: public-safe gate command를 readiness에 포함한다.
- `scripts/demo_poc.py`, `scripts/workflow_rebuild_report.py`, `scripts/feedback_queue_report.py` - 왜: 재현 command의 예시다.

## 작업

manifest를 읽어 artifacts와 commands를 확인하는 `scripts/toolkit_readiness.py`와 테스트를 추가한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_toolkit_readiness.py -q
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. missing file, failed command, protected artifact negative case를 포함한다.
3. TK2를 completed로 업데이트한다.

## 금지사항

- checker가 protected data existence를 성공 조건으로 요구하지 않게 한다.
