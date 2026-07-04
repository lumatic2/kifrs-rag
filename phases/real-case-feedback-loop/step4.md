# Step RC4: Feedback Loop Report and Close Gate

## 읽어야 할 파일

- `phases/real-case-feedback-loop/index.json` - 왜: RC1~RC3 상태를 확인한다.
- `kifrs/feedback/case_intake.py` - 왜: report에 정확한 schema 경계를 적는다.
- `ROADMAP.md`, `docs/OBJECTIVE.md` - 왜: horizon 완료 상태와 다음 후보를 정리한다.

## 작업

sample intake/correction과 close gate 결과를 report로 묶고 horizon을 닫는다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_real_case_feedback.py tests\test_source_aware_rebuild.py -q
python scripts\quality_preflight.py --format text
git diff --check
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. close report를 작성한다.
3. phase와 horizon을 completed/closed로 업데이트한다.

## 금지사항

- 실제 사례를 수집한 것처럼 표현하지 않는다. 이번 horizon은 loop structure와 public-safe sample만 만든다.
