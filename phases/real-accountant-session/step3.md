# Step RS3: Capture and Queue Conversion

## 읽어야 할 파일

- `kifrs/feedback/capture.py` - 왜: actual notes validation과 queue conversion API.
- `docs/reports/real-accountant-session/actual-feedback-notes.md` - 왜: capture 대상.

## 작업

actual feedback notes를 capture pipeline에 넣고 safe correction을 queue record로 변환한다.

## Acceptance Criteria

```powershell
Test-Path docs\reports\real-accountant-session\capture-manifest.json
rg -n '"actual_feedback_evidence": true' docs\reports\real-accountant-session\capture-manifest.json
python scripts\real_accountant_session_check.py --manifest docs\reports\real-accountant-session\session_manifest.json
```

## 검증 절차

1. actual feedback evidence manifest가 true인지 확인한다.
2. generated queue records가 public-safe인지 확인한다.
3. RS3을 completed로 업데이트한다.

## 금지사항

- sample notes로 actual feedback evidence를 true로 만들지 않는다.
