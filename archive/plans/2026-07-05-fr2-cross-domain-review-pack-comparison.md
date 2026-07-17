# FR2 — Cross-domain review pack comparison

> Date: 2026-07-05
> Horizon: `f-acc-1109-review-pack`
> Phase step: `phases/1109-review-pack/step2.md`

## 산문 요약

FR2는 1116 리스 review pack과 1109 금융상품 review pack을 나란히 비교해, F-ACC workpaper pack의
공통 구조와 도메인별 차이를 정리한다. 목적은 다음 도메인 확장 전에 공통 schema를 지금 코드로
뽑을지, 아니면 한 번 더 도메인을 확장한 뒤 뽑을지 결정하는 것이다.

## Step tree

- [x] Step 2 — cross-domain comparison
  - AC: `docs/reports/2026-07-05-fr2-cross-domain-review-pack-comparison.md`가 공통 필드, 도메인별 필드, renderer 차이, NeedsHumanReview 차이, schema 결정, 다음 milestone을 포함한다.
  - AC: `python -m pytest tests/test_1109_review_pack.py tests/test_1116_review_pack.py`
  - AC: `git diff --check`

## 결정 로그

- 결정: 공통 제품 개념은 `F-ACC Review Pack`으로 유지한다.
- 결정: `standard`, `case_id`, `status`, `judgment_summary`, `journal_entry`, `review_memo`, `review_checklist`, `needs_human_review`, `citations`는 공통 필드 후보로 본다.
- 결정: 1109 `classification`, 1116 `disclosure_draft`는 도메인별 확장 필드로 둔다.
- 결정: 코드 공통 schema 추출은 FR2에서 하지 않는다. 1115 또는 주석 대사 같은 세 번째 표면이 생긴 뒤 추출한다.

## 산출물

- `docs/reports/2026-07-05-fr2-cross-domain-review-pack-comparison.md`
- `phases/1109-review-pack/step2.md`
- `ROADMAP.md`
