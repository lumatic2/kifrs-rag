# Step RS1: Session Packet Prep

## 읽어야 할 파일

- `docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md` - 왜: 실제 세션 운영 절차의 기준이다.
- `docs/reports/field-feedback-capture/INDEX.md` - 왜: 세션 후 capture package로 이어지는 경로를 확인한다.
- `docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md` - 왜: reviewer에게 보낼 요약 문구의 기반이다.

## 작업

실제 회계사에게 보낼 세션 초대문, 준비 패킷, 증거 템플릿을 작성한다.

## Acceptance Criteria

```powershell
Test-Path docs\reports\real-accountant-session\SESSION_PACKET.md
Test-Path docs\reports\real-accountant-session\2026-07-05-session-invite.md
Test-Path docs\reports\real-accountant-session\2026-07-05-session-evidence-template.md
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. packet이 actual feedback evidence가 아직 없음을 명시하는지 확인한다.
3. RS1을 completed로 업데이트한다.

## 금지사항

- 아직 실제 피드백을 받은 것처럼 쓰지 않는다.
