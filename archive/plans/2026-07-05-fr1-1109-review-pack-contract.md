# FR1 — 1109 review pack contract + fixture regression

> Date: 2026-07-05
> Horizon: `f-acc-1109-review-pack`
> Phase step: `phases/1109-review-pack/step1.md`

## 산문 요약

FR1은 1116 review pack 패턴을 1109 금융상품 엔진에 이식한다. 기존 1109 판단 로직은 바꾸지 않고,
runner가 내는 분류, 최초분개, 검토메모, NeedsHumanReview 경계를 회계자문팀 workpaper pack으로 묶는다.

## Step tree

- [x] Step 1 — 1109 review pack contract + renderer
  - AC: `python -m pytest tests/test_workflow_1109.py tests/test_workflow_1109_regression.py tests/test_1109_review_pack.py`
  - AC: `python -m pytest tests/test_1116_review_pack.py`
  - AC: `git diff --check`

## 결정 로그

- 결정: 1115 신규 엔진보다 1109 review pack 이식을 먼저 한다.
- 결정: 1116과 1109 공통 schema 추출은 아직 하지 않는다. 두 번째 도메인 pack을 만든 뒤 FR2에서 판단한다.
- 결정: 1109 NeedsHumanReview 4개는 자동화하지 않고, 사람 검토 checklist로 설명한다.

## 산출물

- `kifrs/workflows/kifrs1109/review_pack.py`
- `tests/test_1109_review_pack.py`
- `docs/reports/2026-07-05-fr1-1109-review-pack.md`
- `phases/1109-review-pack/step1.md`
