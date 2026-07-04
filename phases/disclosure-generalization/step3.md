# Step 3: 1115-disclosure-pilot

Status: completed (2026-07-05)

## 읽어야 할 파일

- `kifrs/workflows/disclosure/adapters.py` — 왜: 1115 review pack을 common disclosure item으로 변환한다.
- `kifrs/workflows/kifrs1115/review_pack.py` — 왜: 1115 disclosure source다.

## 작업

1115 review pack에서 수익인식 주석 skeleton markdown을 생성한다. 자동 산출 후보와 사람 보완 필요 항목을
분리해 렌더링한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_1115_disclosure.py
git diff --check
```

## 결과

- `kifrs/workflows/kifrs1115/disclosure.py`: `generate_disclosure_skeleton()` 추가.
- 자동 pack, review pack 직접 입력, NeedsHumanReview pack의 skeleton 렌더링을 테스트했다.
