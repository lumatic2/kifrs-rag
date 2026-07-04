# Step 3: measurement-and-journal-entry-draft

Status: completed (2026-07-05)

## 읽어야 할 파일

- `kifrs/workflows/kifrs1115/classify.py` — 왜: 5단계 판단 결과를 측정/분개 입력으로 사용한다.
- `kifrs/workflows/kifrs1109/initial_entry.py` — 왜: 기존 workflow의 `EntryLine`/`JournalEntry` 패턴을 따른다.
- `kifrs/workflows/kifrs1116/initial_entry.py` — 왜: domain별 분개 초안 생성 방식의 전례다.

## 작업

R15-2 decision output에서 다음 산출물을 만든다.

- material right 상대 SSP 배분
- 유의적 금융요소의 현금판매가격 기준 수익 + 이연금융수익
- 재매입 콜옵션의 금융부채/금융비용 초안
- 균형 잡힌 journal entry draft

## Acceptance Criteria

```powershell
python -m pytest tests/test_workflow_1115.py
git diff --check
```

## 결과

- `kifrs/workflows/kifrs1115/measurement.py`: `RevenueMeasurement`와 material right/financing/repurchase 측정 로직 추가.
- `kifrs/workflows/kifrs1115/journal_entry.py`: `JournalEntry` 초안 생성 로직 추가.
- `tests/test_workflow_1115.py`: 배분, 이연금융수익, 재매입약정 수익 미인식, 분개 균형 테스트 추가.
