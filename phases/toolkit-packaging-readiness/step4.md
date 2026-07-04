# Step TK4: Close Gate

## 읽어야 할 파일

- `phases/toolkit-packaging-readiness/index.json` - 왜: TK1~TK3 상태를 확인한다.
- `docs/reports/2026-07-05-tk3-toolkit-readiness-report.md` - 왜: close evidence로 참조한다.
- `ROADMAP.md`, `docs/OBJECTIVE.md` - 왜: horizon 완료 상태와 다음 후보를 정리한다.

## 작업

tests, readiness command, public-safe preflight, close report, ROADMAP/OBJECTIVE sync를 끝낸다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_toolkit_readiness.py tests\test_feedback_queue.py -q
python scripts\toolkit_readiness.py --manifest docs\toolkit\readiness_manifest.json --out docs\reports\2026-07-05-tk3-toolkit-readiness-report.md
python scripts\quality_preflight.py --format text
git diff --check
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. close report를 작성한다.
3. phase와 horizon을 completed/closed로 업데이트한다.

## 금지사항

- readiness를 실제 설치형 release와 혼동하지 않는다.
