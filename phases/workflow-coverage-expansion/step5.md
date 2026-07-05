# Step 5: Workflow Coverage Close Gate

## 읽어야 할 파일
- docs/reports/2026-07-05-wce1-coverage-gap-ranking.md — 왜: 후보 선정 근거를 close gate에 연결한다.
- docs/reports/2026-07-05-wce2-first-workflow-contract.md — 왜: workflow contract 통과 여부를 확인한다.
- docs/reports/2026-07-05-wce3-minimal-review-pack-adapter.md — 왜: adapter evidence를 확인한다.
- docs/reports/2026-07-05-wce4-coverage-metric-update.md — 왜: objective coverage 반영 여부를 확인한다.
- docs/reports/2026-07-05-product-trust-quality-close-report.md — 왜: 신뢰/품질 evidence와 연결한다.

## 작업
WCE1~WCE4가 모두 통과했는지 확인하고, workflow coverage expansion horizon을 닫는 close gate를 구현한다. 다음 horizon은 runtime-retriever-promotion-gate다.

## Acceptance Criteria
```bash
python -m pytest tests\test_workflow_coverage_close_gate.py -q
python scripts\workflow_coverage_close_gate.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. close gate가 required reports, public-safe boundary, product trust 연결, next horizon을 확인하는지 본다.
3. horizon 문서, ROADMAP, phase index를 completed/next active로 갱신한다.

## 금지사항
- WCE1~WCE4 evidence 없이 close 처리하지 마라.
