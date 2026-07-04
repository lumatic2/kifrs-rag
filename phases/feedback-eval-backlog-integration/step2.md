# Step FI2: Queue Report and Split

## 읽어야 할 파일

- `kifrs/feedback/queue.py` - 왜: queue record와 summary를 report로 렌더한다.
- `scripts/real_case_feedback_report.py` - 왜: public-safe sample/report 스타일을 맞춘다.

## 작업

queue를 eval seed 후보와 backlog 후보로 분리하고 markdown report를 생성한다. command는
`scripts/feedback_queue_report.py`로 둔다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_feedback_queue.py -q
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. eval/backlog/no_action count와 high severity surfacing을 확인한다.
3. FI2를 completed로 업데이트한다.

## 금지사항

- report에 raw source body/customer identifier를 출력하지 않는다.
