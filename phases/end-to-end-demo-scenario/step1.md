# Step 1: Demo Asset Inventory And Storyboard

## 읽어야 할 파일

- `docs/horizons/end-to-end-demo-scenario.md` - 왜: E2E1 acceptance와 horizon 경계를 확인한다.
- `docs/plans/2026-07-05-end-to-end-demo-scenario.md` - 왜: 전체 step tree와 결정 로그를 따른다.
- `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` - 왜: local parser stage의 증거다.
- `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md` - 왜: controlled non-IFRS source stage의 증거다.
- `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` - 왜: 1037 provisions workflow stage의 증거다.
- `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` - 왜: retriever promotion/defer stage의 증거다.
- `docs/reports/2026-07-05-operator-experience-hardening-close-report.md` - 왜: operator run/recover stage의 증거다.

## 작업

`scripts/e2e_demo_asset_inventory.py`를 만들어 public-safe demo asset inventory를 생성한다. 결과는 parser, source lane, workflow, retriever, operator stages를 한 줄 demo storyboard로 정렬해야 한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_e2e_demo_asset_inventory.py -q
python scripts\e2e_demo_asset_inventory.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. 보고서에 protected local payload, secret, raw source text가 없는지 확인
3. `phases/end-to-end-demo-scenario/index.json` step 업데이트

## 금지사항

- 기준서 원문, 파싱 DB, 임베딩, dogfood, private payload를 출력하지 마라. 이유: 공개 가능 산출물 경계.
- 존재하지 않는 report를 있는 것처럼 표시하지 마라. 이유: demo smoke의 신뢰성.
