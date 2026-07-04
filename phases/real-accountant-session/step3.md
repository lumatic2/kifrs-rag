# Step RS3: Capture and Queue Conversion

## 읽어야 할 파일

- `kifrs/feedback/capture.py` - 왜: actual notes validation과 queue conversion API.
- `docs/reports/real-accountant-session/actual-feedback-notes.md` - 왜: capture 대상.

## 작업

actual feedback notes를 capture pipeline에 넣고 safe correction을 queue record로 변환한다.

## Acceptance Criteria

```powershell
python scripts\real_accountant_notes_check.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md
python scripts\real_accountant_capture.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md --out docs\reports\real-accountant-session
Test-Path docs\reports\real-accountant-session\capture-manifest.json
rg -n '"actual_feedback_evidence": true' docs\reports\real-accountant-session\capture-manifest.json
python scripts\real_accountant_manifest_build.py --out docs\reports\real-accountant-session\session_manifest.json --notes docs\reports\real-accountant-session\actual-feedback-notes.md --capture-manifest docs\reports\real-accountant-session\capture-manifest.json --queue-jsonl docs\reports\real-accountant-session\feedback-queue.jsonl --reviewer-role "CPA reviewer" --reviewer-service-line "F-ACC" --reviewer-experience-context "reviewed accounting advisory workpapers"
python scripts\real_accountant_session_check.py --manifest docs\reports\real-accountant-session\session_manifest.json
```

## 검증 절차

1. actual notes checker가 public-safe 통과하는지 확인한다.
2. `real_accountant_capture.py`로 capture manifest와 feedback queue JSONL을 생성한다.
3. actual capture manifest가 true인지 확인한다.
4. generated queue records가 public-safe이고 비어 있지 않은지 확인한다.
5. session manifest builder가 `actual_feedback` manifest를 생성하는지 확인한다.
6. RS3을 completed로 업데이트한다.

## 금지사항

- sample notes로 actual feedback evidence를 true로 만들지 않는다.
- `actual_feedback_evidence`를 수동 편집으로 true로 만들지 않는다. builder를 통과시킨다.
