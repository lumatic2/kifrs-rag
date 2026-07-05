# Step 4: Private Payload Leak Tests

## 읽어야 할 파일

- `phases/real-local-parser-prototype/step2.md` — 왜: adapter output의 public-safe surface 확인.
- `phases/real-local-parser-prototype/step3.md` — 왜: deletion simulation output의 public-safe surface 확인.
- `docs/reports/2026-07-05-product-trust-quality-close-report.md` — 왜: trust/failure boundary와 public-safe gate를 이어받는다.

## 작업

parser output과 report가 body-like, identifier-like, OCR-like, embedding-like payload를 포함하지 않는지 검사하는 leak test를 만든다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_private_payload_leak_tests.py -q
python scripts\private_payload_leak_tests.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-rlp4-private-payload-leak-tests.md` 생성 확인
3. 성공 시 `phases/real-local-parser-prototype/index.json` step 4를 completed로 갱신

## 금지사항

- leak fixture에 실제 개인정보, 계약 원문, OCR text, source body, embedding vector를 넣지 않는다.
- forbidden pattern 테스트를 warning-only로 만들지 않는다.
