# Step FC3: Capture Report Command

## 읽어야 할 파일

- `kifrs/feedback/capture.py` - 왜: sample notes와 report renderer를 호출한다.
- `docs/reports/real-transaction-poc/INDEX.md` - 왜: sample case id와 대상 route를 맞춘다.

## 작업

명령 하나로 sample capture package를 생성하는 스크립트를 만든다.

## Acceptance Criteria

```powershell
python scripts\field_feedback_capture.py --out docs\reports\field-feedback-capture
Test-Path docs\reports\field-feedback-capture\INDEX.md
Test-Path docs\reports\field-feedback-capture\feedback-queue.jsonl
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. package가 sample notes, capture report, queue JSONL, queue report를 포함하는지 확인한다.
3. FC3을 completed로 업데이트한다.

## 금지사항

- sample notes를 실제 회계사 세션 결과라고 표현하지 않는다.
