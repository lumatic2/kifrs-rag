# Step FI3: Public-Safe Sample Queue

## 읽어야 할 파일

- `scripts/feedback_queue_report.py` - 왜: sample queue와 report를 command로 생성한다.
- `kifrs/feedback/queue.py` - 왜: sample record 생성이 validator를 통과해야 한다.

## 작업

sample queue와 markdown report를 생성한다.

## Acceptance Criteria

```powershell
python scripts\feedback_queue_report.py --queue docs\feedback\feedback_queue.sample.jsonl --out docs\reports\2026-07-05-fi3-feedback-queue-report.md
Test-Path docs\feedback\feedback_queue.sample.jsonl
Test-Path docs\reports\2026-07-05-fi3-feedback-queue-report.md
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. sample이 actual client case가 아님을 report에 명시한다.
3. FI3을 completed로 업데이트한다.

## 금지사항

- sample queue에 실제 사례를 넣지 않는다.
