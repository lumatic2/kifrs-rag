# Step TK3: Readiness Report

## 읽어야 할 파일

- `scripts/toolkit_readiness.py` - 왜: readiness result를 markdown으로 렌더한다.
- `docs/toolkit/readiness_manifest.json` - 왜: default manifest다.

## 작업

readiness checker를 실행해 markdown report를 생성한다.

## Acceptance Criteria

```powershell
python scripts\toolkit_readiness.py --manifest docs\toolkit\readiness_manifest.json --out docs\reports\2026-07-05-tk3-toolkit-readiness-report.md
Test-Path docs\reports\2026-07-05-tk3-toolkit-readiness-report.md
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. report가 PASS/FAIL/SKIP와 next action을 보여주는지 확인한다.
3. TK3을 completed로 업데이트한다.

## 금지사항

- 실제 배포 릴리스가 완료됐다고 쓰지 않는다. readiness package만 만든다.
