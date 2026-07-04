# Step 2: cross-domain-review-pack-comparison

## 읽어야 할 파일

- `docs/horizons/f-acc-1109-review-pack.md` — 왜: FR2의 목표와 close criteria를 확인한다.
- `docs/plans/2026-07-05-fr2-cross-domain-review-pack-comparison.md` — 왜: FR2 결정 로그와 acceptance criteria가 있다.
- `kifrs/workflows/kifrs1116/review_pack.py` — 왜: 1116 review pack schema, renderer, NeedsHumanReview 구조를 비교한다.
- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: 1109 review pack schema, renderer, NeedsHumanReview 구조를 비교한다.
- `tests/test_1116_review_pack.py` — 왜: 1116 pack contract가 테스트로 고정된 지점을 확인한다.
- `tests/test_1109_review_pack.py` — 왜: 1109 pack contract가 테스트로 고정된 지점을 확인한다.

## 작업

1116/1109 review pack을 비교해 공통 필드와 도메인별 확장 필드를 구분한다. 공통 schema 후보를 문서로
정리하되, FR2에서는 코드 추출을 하지 않는다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_1109_review_pack.py tests/test_1116_review_pack.py
git diff --check
```

## 검증 절차

1. AC 커맨드 실행
2. 비교 리포트가 공통 필드, 도메인별 필드, 코드 공통화 결정, 다음 milestone을 포함하는지 확인
3. `phases/1109-review-pack/index.json` step 상태 갱신

## 금지사항

- FR2에서 공통 Python schema를 바로 추출하지 않는다. 이유: 아직 도메인이 2개뿐이라 추상화가 이르다.
- 기존 1109/1116 review pack 테스트 계약을 변경하지 않는다.
