# Architecture — F-ACC review pack

> Created: 2026-07-04
> Horizon: `f-acc-review-pack` → `f-acc-1109-review-pack`

## Existing Assets

- `kifrs/workflows/kifrs1116/runner.py` — 1116 리스 판단 엔진 runner
- `kifrs/workflows/kifrs1116/review_memo.py` — 1116 검토메모 초안
- `kifrs/workflows/kifrs1116/disclosure.py` — 1116 주석 요구사항 checklist/초안
- `kifrs/workflows/kifrs1109/runner.py` — 1109 금융상품 분류·측정 runner
- `kifrs/workflows/kifrs1109/review_memo.py` — 1109 검토메모 초안
- `tests/test_workflow_1116_regression.py` — 1116 fixture 회귀
- `tests/test_1116_disclosure.py` — 1116 disclosure 회귀
- `tests/test_workflow_1109_regression.py` — 1109 fixture 회귀

## Target Module

새 모듈은 기존 기준서 엔진을 감싸는 orchestration layer로 둔다.

```text
kifrs/workflows/kifrs1116/
  review_pack.py        # 신규: engine output + memo + disclosure + checklist 결합
kifrs/workflows/kifrs1109/
  review_pack.py        # 신규: engine output + memo + checklist 결합
```

필요하면 나중에 공통 패키지로 승격한다.

```text
kifrs/workflows/review_pack/
  schema.py
  renderer.py
```

단, 1116과 1109 두 도메인까지는 각 기준서 전용 모듈로 작게 시작한다. 공통 schema 추출은 FR2에서
두 도메인의 중복과 차이를 비교한 뒤 판단한다.

## Output Contract

review pack은 두 형태를 목표로 한다.

- structured object/json: 테스트와 후속 자동화용
- markdown: 회계자문팀 workpaper 초안 데모용

최소 필드:

- `standard`: `KIFRS1116` 또는 `KIFRS1109`
- `scenario_id` 또는 `case_id`
- `classification` (1109)
- `judgment_summary`
- `journal_entries`
- `review_memo`
- `disclosure_draft` (1116)
- `review_checklist`
- `needs_human_review`
- `citations`

## Boundary

`review_pack.py`는 판단 로직을 새로 만들지 않는다. 기존 1116/1109 모듈이 만든 판단·계산·메모·주석
또는 분개를 하나의 산출물로 묶는다. 신규 판단 로직이 필요하면 먼저 해당 기준서 하위 모듈에 테스트와
함께 넣는다.

## Verification

기본 검증 명령:

```powershell
python -m pytest tests/test_workflow_1116_regression.py tests/test_1116_disclosure.py
```

review pack milestone에서는 별도 테스트를 추가한다.

```powershell
python -m pytest tests/test_1116_review_pack.py
python -m pytest tests/test_1109_review_pack.py
```
