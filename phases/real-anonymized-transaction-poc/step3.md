# Step RA3: Public-Safe Sample Package

## 읽어야 할 파일

- `kifrs/feedback/transaction_poc.py` - 왜: sample package 생성 API를 호출한다.
- `docs/reports/firm-facing-poc/INDEX.md` - 왜: firm-facing package와 이어지는 읽기 순서를 맞춘다.

## 작업

명령 하나로 public-safe real transaction PoC sample package를 생성하는 스크립트를 만든다.

## Acceptance Criteria

```powershell
python scripts\real_transaction_poc.py --out docs\reports\real-transaction-poc
Test-Path docs\reports\real-transaction-poc\INDEX.md
Test-Path docs\reports\real-transaction-poc\review-pack.md
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. package가 anonymized input card, review pack, queue JSONL, queue report를 포함하는지 확인한다.
3. RA3을 completed로 업데이트한다.

## 금지사항

- raw contract body나 customer identifier를 sample에 넣지 않는다.
