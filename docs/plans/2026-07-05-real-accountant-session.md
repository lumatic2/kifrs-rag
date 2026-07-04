# Plan: Real Accountant Session

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/real-accountant-session.md`
> Status source: `phases/real-accountant-session/index.json`

## 요약

이번 horizon은 실제 회계사 1명에게 30분 세션을 운영하고, public-safe notes를 capture pipeline에 넣어
queue record로 변환하는 것을 목표로 한다. RS1 세션 패킷은 완료됐고, RS2는 실제 reviewer 섭외/일정이
필요하므로 pending이다. 다만 RS2를 바로 실행할 수 있도록 alias-only outreach ledger checker와 update
CLI까지 준비했다.
현재 위치와 다음 액션은 `python scripts\real_accountant_status.py`로 확인한다.

## Step Tree

- [x] RS1 — session packet prep. (verify: `Test-Path docs\reports\real-accountant-session\SESSION_PACKET.md`)
- [ ] RS2 — run actual accountant session. (verify: actual public-safe notes exist; prep CLI:
  `python scripts\real_accountant_invite_packet.py`;
  `python scripts\real_accountant_outreach_update.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08`;
  notes gate: `python scripts\real_accountant_notes_check.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md`)
- [ ] RS3 — capture and queue conversion. (verify: actual notes gate + actual capture manifest with `actual_feedback_evidence: true` + `real_accountant_manifest_build.py`)
- [ ] RS4 — close gate. (verify: `real_accountant_close_check.py --run-quality-preflight` + actual feedback evidence)

## 결정 로그

- 결정: 실제 세션이 없으면 horizon을 닫지 않는다.
- 결정: 실제 reviewer가 준비되기 전에는 session invite/evidence template/packet/outreach ledger tooling까지만 만든다.
- 결정: actual feedback evidence는 reviewer metadata와 public-safe notes가 있을 때만 true로 표시한다.
- 결정: actual notes는 `real_accountant_notes_check.py`를 통과하기 전에는 capture/queue 변환하지 않는다.
- 결정: actual session manifest는 수동 편집이 아니라 `real_accountant_manifest_build.py`로 생성한다.
- 결정: horizon close는 `real_accountant_close_check.py`가 actual manifest, notes, queue, outreach completed, quality preflight를 통과할 때만 한다.
- 사용자 소유 결정: 회계사 reviewer 섭외, 일정 조율, 실제 세션 진행.

## 중단점

- 실제 reviewer가 없으면 RS2 이후로 진행하지 않는다.
- raw contract/customer data를 notes로 받게 되면 capture하지 않는다.
