# Step 1: review-pack-contract-renderer

## 읽어야 할 파일

- `docs/horizons/f-acc-1109-review-pack.md` — 왜: 이번 기술 확장 horizon의 목표와 범위를 확인한다.
- `docs/plans/2026-07-05-fr1-1109-review-pack-contract.md` — 왜: FR1 결정 로그와 acceptance criteria가 있다.
- `kifrs/workflows/kifrs1109/runner.py` — 왜: 기존 1109 pipeline output을 review pack input으로 사용한다.
- `kifrs/workflows/kifrs1109/review_memo.py` — 왜: 검토메모 초안을 review pack에 포함한다.
- `kifrs/workflows/kifrs1109/initial_entry.py` — 왜: 최초분개 초안을 review pack에 포함한다.
- `kifrs/workflows/kifrs1109/fixtures.py` — 왜: 10개 fixture 전체 pack 생성 상태를 검증한다.
- `kifrs/workflows/kifrs1116/review_pack.py` — 왜: 1116에서 검증된 review pack renderer 패턴을 참고한다.

## 작업

1109 전용 `review_pack.py`를 추가해 기존 runner/review memo/journal entry output을 structured review
pack과 markdown workpaper 초안으로 묶는다. 새 분류·측정 판단 로직은 만들지 않는다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_workflow_1109.py tests/test_workflow_1109_regression.py tests/test_1109_review_pack.py
python -m pytest tests/test_1116_review_pack.py
git diff --check
```

## 검증 절차

1. AC 커맨드 실행
2. 1109 fixture 10개가 모두 pack을 생성하고, 기존 6/10 자동화 경계가 유지되는지 확인
3. `phases/1109-review-pack/index.json` step 상태 갱신

## 금지사항

- FR1에서 1109 NeedsHumanReview 4개를 자동화하지 않는다. 이유: 이번 목표는 pack 이식이지 신규 판단 로직이 아니다.
- 기준서 원문, DB 덤프, 비공개 dogfood 자료를 report에 포함하지 않는다.
