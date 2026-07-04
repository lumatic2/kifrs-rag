# Step FC4: Close Gate

## 읽어야 할 파일

- `docs/reports/field-feedback-capture/INDEX.md` - 왜: 최종 capture package entry point를 확인한다.
- `ROADMAP.md` - 왜: horizon close와 다음 추천 horizon을 동기화한다.
- `docs/OBJECTIVE.md` - 왜: active horizon과 최근 완료 상태를 동기화한다.

## 작업

focused tests, sample package generation, quality preflight를 실행하고 close report를 작성한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_field_feedback_capture.py tests\test_feedback_queue.py -q
python scripts\field_feedback_capture.py --out docs\reports\field-feedback-capture
python scripts\quality_preflight.py --format text
git diff --check
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. ROADMAP 150줄 제한을 확인한다.
3. close report를 작성하고 FC4를 completed로 업데이트한다.
4. ROADMAP/OBJECTIVE를 다음 horizon 추천 상태로 전환한다.

## 금지사항

- actual reviewer evidence 없이 goal complete를 주장하지 않는다.
