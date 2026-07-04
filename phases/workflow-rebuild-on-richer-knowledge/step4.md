# Step WR4: Close Gate

## 읽어야 할 파일

- `phases/workflow-rebuild-on-richer-knowledge/index.json` - 왜: WR1~WR3 상태와 summary를 확인한다.
- `docs/reports/2026-07-05-wr3-source-aware-rebuild-report.md` - 왜: close report의 evidence로 참조한다.
- `ROADMAP.md`, `docs/OBJECTIVE.md` - 왜: horizon completion 상태를 동기화한다.

## 작업

관련 테스트와 public-safe gate를 통과시키고 close report를 작성한다. ROADMAP/OBJECTIVE는 다음
진행 후보가 무엇인지 명확히 가리키게 한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_source_aware_rebuild.py tests\test_1109_review_pack.py tests\test_1115_review_pack.py tests\test_1116_review_pack.py tests\test_demo_poc.py -q
python scripts\quality_preflight.py --format text
git diff --check
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. close report를 작성한다.
3. `phases/workflow-rebuild-on-richer-knowledge/index.json`의 WR4와 phase status를 completed로 업데이트한다.

## 금지사항

- 실패한 gate를 통과한 것처럼 기록하지 않는다.
- 다음 horizon을 구현 완료로 표시하지 않는다.
