# Step 2: Source Body Policy Record

## 읽어야 할 파일

- `phases/source-body-ingestion-controlled-lane/step1.md` — 왜: SBI1에서 선택한 source class와 authorization boundary를 이어받는다.
- `docs/reports/2026-07-05-sbi1-source-class-selection.md` — 왜: allowed/forbidden fields와 fallback plan 확인.

## 작업

선택된 source lane의 machine-readable policy record를 만들고 storage, citation role, chunking, retention policy를 검증한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_source_body_policy_record.py -q
python scripts\source_body_policy_record.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-sbi2-source-body-policy-record.md` 생성 확인
3. 성공 시 step 2를 completed로 갱신

## 금지사항

- policy record에 실제 protected source body를 넣지 않는다.
- K-IFRS primary authority 우선순위를 바꾸지 않는다.
