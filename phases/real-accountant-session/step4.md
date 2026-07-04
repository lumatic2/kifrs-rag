# Step RS4: Close Gate

## 읽어야 할 파일

- `docs/reports/real-accountant-session/capture-manifest.json` - 왜: 실제 피드백 evidence 여부 확인.
- `docs/reports/real-accountant-session/feedback-queue.jsonl` - 왜: safe correction queue 확인.
- `ROADMAP.md` - 왜: horizon close와 다음 horizon 동기화.
- `docs/OBJECTIVE.md` - 왜: 중간 관문 달성 여부 반영.

## 작업

actual session evidence와 queue conversion을 검증하고 horizon을 닫는다.

## Acceptance Criteria

```powershell
python scripts\real_accountant_session_check.py --manifest docs\reports\real-accountant-session\session_manifest.json
python scripts\quality_preflight.py --format text
git diff --check
```

## 검증 절차

1. actual feedback evidence가 실제로 있는지 확인한다.
2. quality preflight가 public-safe인지 확인한다.
3. close report를 작성하고 ROADMAP/OBJECTIVE를 갱신한다.

## 금지사항

- 실제 회계사 세션 없이 이 horizon을 close하지 않는다.
