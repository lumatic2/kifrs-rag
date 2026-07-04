# Step RA2: Transaction PoC Adapter

## 읽어야 할 파일

- `kifrs/feedback/case_intake.py` - 왜: public-safe intake validation과 routing 규칙을 재사용한다.
- `kifrs/feedback/queue.py` - 왜: reviewer correction을 eval/backlog queue record로 연결한다.
- `kifrs/workflows/kifrs1116/schema.py` - 왜: 익명화 facts를 `Lease1116` 입력으로 변환한다.
- `kifrs/workflows/kifrs1116/review_pack.py` - 왜: 1116 review pack generation과 markdown renderer를 재사용한다.

## 작업

익명화 거래 카드에서 KIFRS1116 review pack과 feedback queue record를 만드는 adapter를 추가한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_real_transaction_poc.py -q
```

## 검증 절차

1. focused test를 실행한다.
2. protected field가 들어간 case가 실패하는지 확인한다.
3. RA2를 completed로 업데이트한다.

## 금지사항

- 새 회계 판단 로직을 만들지 않는다. 기존 1116 engine/review pack을 감싼다.
