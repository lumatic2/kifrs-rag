# Step FI1: Feedback Queue Store

## 읽어야 할 파일

- `kifrs/feedback/case_intake.py` - 왜: CaseIntake, ReviewerCorrection, eval seed candidate 계약을 재사용한다.
- `docs/horizons/real-case-feedback-loop.md` - 왜: 이전 horizon이 만든 feedback loop 경계를 이어받는다.
- `CLAUDE.md` - 왜: raw 고객자료, 계약 원문, 기준서 본문 commit 금지 경계를 지킨다.

## 작업

validated case/correction/seed candidate를 JSONL queue record로 만들고 저장/로드하는 `kifrs/feedback/queue.py`
를 추가한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_feedback_queue.py -q
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. duplicate record id와 protected payload negative case를 테스트한다.
3. FI1을 completed로 업데이트한다.

## 금지사항

- actual client case를 sample queue에 넣지 않는다.
- queue record에 raw source body/customer identifier를 허용하지 않는다.
