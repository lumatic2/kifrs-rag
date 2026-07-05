# Step 1: Promotion Evidence Inventory

## 읽어야 할 파일
- docs/horizons/runtime-retriever-promotion-gate.md — 왜: RPG1 acceptance와 promotion/defer 경계를 확인한다.
- docs/plans/2026-07-05-runtime-retriever-promotion-gate.md — 왜: RPG milestone tree와 decision log를 따른다.
- docs/reports/2026-07-05-rag-quality-refresh-close-report.md — 왜: opt-in repair retriever 평가 증거의 시작점이다.
- docs/reports/2026-07-05-default-retriever-guard.md — 왜: 현재 default 변경이 왜 막혀 있는지 확인한다.
- docs/reports/2026-07-05-product-trust-quality-close-report.md — 왜: 제품 신뢰 gate와 promotion evidence를 연결한다.

## 작업
현재 retriever promotion 판단에 쓰일 증거를 promotion-supporting, promotion-blocking, advisory로 분류한다. 결과는 RPG2의 regression/latency gate 입력이 되어야 한다.

## Acceptance Criteria
```bash
python -m pytest tests\test_retriever_promotion_evidence_inventory.py -q
python scripts\retriever_promotion_evidence_inventory.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. report가 지원 증거, 차단 증거, 자문 증거, missing evidence를 모두 포함하는지 확인.
3. `phases/runtime-retriever-promotion-gate/index.json` step 1 상태를 completed로 갱신한다.

## 금지사항
- 이 step에서 runtime default를 변경하지 마라. 이유: RPG5 close gate 전까지 promotion은 결정되지 않았다.
- protected K-IFRS body, embedding dump, dogfood material을 commit하지 마라.
