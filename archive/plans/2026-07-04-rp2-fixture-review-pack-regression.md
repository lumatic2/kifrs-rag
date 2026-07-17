# RP2 plan — fixture review pack regression + summary

> Date: 2026-07-04
> Horizon: `f-acc-review-pack`
> Milestone: RP2
> Objective: `docs/OBJECTIVE.md`
> Horizon plan: `docs/horizons/f-acc-review-pack.md`

## Scope

RP2는 RP1에서 만든 review pack contract가 기존 1116 fixture 전체에 적용되는지 확인한다. 새 회계
판단 로직은 추가하지 않고, 10개 fixture의 automated / needs_human_review 상태가 기존 1116 완료율과
일치하는지 검증한다.

## Step tree

- [x] 전체 fixture pack 생성 테스트 추가. (verify: `python -m pytest tests/test_1116_review_pack.py`)
- [x] fixture별 review pack 상태 요약 리포트 작성. (verify: `docs/reports/2026-07-04-rp2-1116-review-pack-fixture-summary.md`)
- [x] 기존 1116 regression/disclosure 테스트와 함께 재검증. (verify: 20 tests passed)

## Decision log

- 결정 필요 없음. RP2는 RP1 산출물의 fixture 적용 범위를 넓히는 검증 milestone이다.

## Acceptance criteria

```powershell
python -m pytest tests/test_workflow_1116_regression.py tests/test_1116_disclosure.py tests/test_1116_review_pack.py
git diff --check
```
