# RP1 plan — 1116 review pack contract + renderer

> Date: 2026-07-04
> Horizon: `f-acc-review-pack`
> Milestone: RP1
> Objective: `docs/OBJECTIVE.md`
> Horizon plan: `docs/horizons/f-acc-review-pack.md`
> Product spec: `docs/PRD.md`, `docs/ARCHITECTURE.md`

## Scope

RP1은 새 회계 판단 로직을 만들지 않는다. 기존 1116 runner, review memo, disclosure draft를 묶어
Accounting Advisory / F-S support 팀이 읽을 수 있는 review pack contract와 markdown renderer를 만든다.

## Step tree

- [ ] Step 1 — output contract 정의: `ReviewPack`, `ReviewPackSection`, `ReviewChecklistItem` 같은 구조를 1116 전용으로 둔다. (verify: `python -m pytest tests/test_1116_review_pack.py`)
- [ ] Step 2 — 기존 1116 output composition: runner 결과, 검토메모, disclosure draft를 하나의 pack으로 결합한다. (verify: 기존 1116 regression + 신규 pack test)
- [ ] Step 3 — markdown renderer: 회계자문팀 workpaper 초안 형태로 판단요약, 분개, 주석, 리뷰 체크리스트를 렌더링한다. (verify: snapshot/string assertions)
- [ ] Step 4 — sample report: fixture 1개로 생성한 sample pack을 `docs/reports/`에 남긴다. (verify: sample 파일 존재 + 민감 원문 미포함)

## Decision log

- 결정 완료: 다음 구현은 `1116 F-ACC review pack`이다.
- 결정 완료: 첫 milestone은 1116 전용 composition layer로 시작한다. 공통 review-pack abstraction은 반복 신호가 생기면 승격한다.
- 결정 완료: 독립 앱/패키징은 이 milestone 범위가 아니다.

## Acceptance criteria

```powershell
python -m pytest tests/test_workflow_1116_regression.py tests/test_1116_disclosure.py tests/test_1116_review_pack.py
git diff --check
```

## Files likely touched

- `kifrs/workflows/kifrs1116/review_pack.py`
- `tests/test_1116_review_pack.py`
- `docs/reports/2026-07-04-rp1-1116-review-pack-sample.md`
- `phases/1116-review-pack/*`
