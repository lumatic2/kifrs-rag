# Step 3: Minimal Review-Pack Adapter

## 읽어야 할 파일
- docs/reports/2026-07-05-wce2-first-workflow-contract.md — 왜: adapter가 구현해야 할 input/output contract 정본이다.
- kifrs/feedback/ — 왜: 기존 review-pack/reporting helper 패턴을 재사용한다.
- scripts/ — 왜: 기존 horizon report script의 render/write/test 패턴을 따른다.

## 작업
선택된 workflow contract를 받아 structured summary와 human-review checklist를 생성하는 최소 adapter를 구현한다. 산출물은 decision-prep draft이며, confidence/failure boundary를 같이 드러낸다.

## Acceptance Criteria
```bash
python -m pytest tests\test_minimal_workflow_review_pack_adapter.py -q
python scripts\minimal_workflow_review_pack_adapter.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. adapter output이 structured summary, review checklist, evidence roles, limitations를 포함하는지 확인.
3. 공개 리포트가 private payload나 protected body text를 포함하지 않는지 확인.
4. `phases/workflow-coverage-expansion/index.json` step 3 상태를 completed로 갱신한다.

## 금지사항
- 기존 review-pack surface와 무관한 새 UX를 크게 만들지 마라. 이유: 이번 step은 minimal adapter다.
