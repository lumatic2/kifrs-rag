# RP3 — NeedsHumanReview checklist hardening

> Date: 2026-07-05
> Horizon: `f-acc-review-pack`
> ROADMAP milestone: RP3
> Phase step: `phases/1116-review-pack/step3.md`

## 산문 요약

RP3는 1116 review pack이 자동화 실패를 단순 문자열로 보여주는 문제를 닫는다. 특히
`scenario_09_lessee_modification_expand_shrink`처럼 회계 판단이 필요한 케이스에서, 회계사가 다음으로
무엇을 확인해야 하는지 보이도록 사람 검토 항목을 구조화한다.

## Step tree

- [x] Step 3 — NeedsHumanReview action checklist
  - AC: `python -m pytest tests/test_workflow_1116_regression.py tests/test_1116_disclosure.py tests/test_1116_review_pack.py`
  - AC: `git diff --check`

## 결정 로그

- 결정: RP3는 1116 전용으로 유지하고, 공통 review-pack framework로 승격하지 않는다.
- 결정: `NeedsHumanReview`는 에러 메시지가 아니라 회계사 action checklist로 표시한다.
- 결정: `scenario_09`는 자동 판단을 확장하지 않고, 확장+축소 동시 변경을 수동 검토 경계로 명시한다.

## 산출물

- `kifrs/workflows/kifrs1116/review_pack.py`
- `tests/test_1116_review_pack.py`
- `docs/reports/2026-07-05-rp3-needs-human-review-checklist.md`
- `phases/1116-review-pack/step3.md`
