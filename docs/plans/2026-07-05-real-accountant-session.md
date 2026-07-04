# Plan: Real Accountant Session

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/real-accountant-session.md`
> Status source: `phases/real-accountant-session/index.json`

## 요약

이번 horizon은 실제 회계사 1명에게 30분 세션을 운영하고, public-safe notes를 capture pipeline에 넣어
queue record로 변환하는 것을 목표로 한다. 이번 Codex run에서는 RS1 세션 패킷 준비까지 닫고, 실제
세션 실행은 외부 reviewer가 필요하므로 pending으로 남긴다.

## Step Tree

- [x] RS1 — session packet prep. (verify: `Test-Path docs\reports\real-accountant-session\SESSION_PACKET.md`)
- [ ] RS2 — run actual accountant session. (verify: actual public-safe notes exist)
- [ ] RS3 — capture and queue conversion. (verify: actual capture manifest with `actual_feedback_evidence: true`)
- [ ] RS4 — close gate. (verify: quality preflight + actual feedback evidence)

## 결정 로그

- 결정: 실제 세션이 없으면 horizon을 닫지 않는다.
- 결정: 이번 run은 session invite/evidence template/packet만 만든다.
- 결정: actual feedback evidence는 reviewer metadata와 public-safe notes가 있을 때만 true로 표시한다.
- 사용자 소유 결정: 회계사 reviewer 섭외, 일정 조율, 실제 세션 진행.

## 중단점

- 실제 reviewer가 없으면 RS2 이후로 진행하지 않는다.
- raw contract/customer data를 notes로 받게 되면 capture하지 않는다.
