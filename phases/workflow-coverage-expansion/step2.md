# Step 2: First New Workflow Candidate Contract

## 읽어야 할 파일
- phases/workflow-coverage-expansion/step1.md — 왜: WCE1 ranking 결과를 WCE2 후보 선택에 이어받는다.
- docs/reports/2026-07-05-wce1-coverage-gap-ranking.md — 왜: 선택할 workflow와 점수 근거를 확인한다.
- docs/horizons/workflow-coverage-expansion.md — 왜: WCE2 acceptance를 확인한다.

## 작업
WCE1에서 추천된 workflow 하나를 선택하고 decision-prep draft output의 input/output, authority boundary, human-review boundary를 machine-readable contract로 정의한다.

## Acceptance Criteria
```bash
python -m pytest tests\test_first_workflow_contract.py -q
python scripts\first_workflow_contract.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. contract가 selected workflow, inputs, outputs, evidence roles, review boundary, not-implemented limits를 포함하는지 확인.
3. `phases/workflow-coverage-expansion/index.json` step 2 상태를 completed로 갱신한다.

## 금지사항
- ranking 근거 없이 임의 후보를 선택하지 마라.
- 사람의 최종 판단이나 서명을 AI가 대체한다고 쓰지 마라.
