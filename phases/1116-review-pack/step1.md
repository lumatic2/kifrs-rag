# Step 1: review-pack-contract-renderer

## 읽어야 할 파일

- `docs/PRD.md` — 왜: F-ACC review pack의 사용자, 산출물, non-goal이 정의되어 있다.
- `docs/ARCHITECTURE.md` — 왜: RP1의 모듈 경계와 output contract가 정의되어 있다.
- `docs/horizons/f-acc-review-pack.md` — 왜: RP1이 속한 horizon 목표와 close criteria를 확인한다.
- `docs/plans/2026-07-04-rp1-1116-review-pack-contract.md` — 왜: step tree와 acceptance criteria가 있다.
- `kifrs/workflows/kifrs1116/runner.py` — 왜: 기존 판단 엔진의 output을 composition input으로 사용한다.
- `kifrs/workflows/kifrs1116/review_memo.py` — 왜: 검토메모 초안을 review pack에 포함한다.
- `kifrs/workflows/kifrs1116/disclosure.py` — 왜: 리스이용자 주석 초안을 review pack에 포함한다.

## 작업

1116 전용 `review_pack.py`를 추가해 기존 runner/review memo/disclosure output을 하나의 structured
review pack과 markdown workpaper 초안으로 묶는다. 새 판단 로직은 만들지 않는다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_workflow_1116_regression.py tests/test_1116_disclosure.py tests/test_1116_review_pack.py
git diff --check
```

## 검증 절차

1. AC 커맨드 실행
2. `review_pack.py`가 기존 판단 로직을 복제하지 않고 composition만 하는지 확인
3. `phases/1116-review-pack/index.json` step 상태 갱신

## 금지사항

- 기준서 원문, DB 덤프, 비공개 dogfood 자료를 sample report에 넣지 않는다.
- 1116 신규 판단 로직을 RP1에서 추가하지 않는다. 필요한 경우 별도 milestone으로 분리한다.
