# Plan: Real Accountant Session

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/real-accountant-session.md`
> Status source: `phases/real-accountant-session/index.json`

## 요약

이번 horizon은 실제 회계사 1명에게 30분 세션을 운영하고, public-safe notes를 capture pipeline에 넣어
queue record로 변환하기 위한 보관용 계획이다. RS1 세션 패킷은 완료됐지만, 사용자 요청에 따라 실제
outreach/mail/invite는 active plan에서 제외한다. 필요한 경우에만 사용자가 별도 horizon으로 다시 연다.
현재 active 방향은 `internal-capability-hardening`이며, 다음 위치는
`python scripts\accounting_intelligence_progress_map.py --format text`로 확인한다.

## Step Tree

- [x] RS1 — session packet prep. (verify: `Test-Path docs\reports\real-accountant-session\SESSION_PACKET.md`)
- [ ] RS2 — paused; run actual accountant session only if user explicitly reopens this horizon. (verify: actual public-safe notes exist; prep CLI:
  `python scripts\real_accountant_invite_packet.py`;
  `python scripts\real_accountant_operator_brief.py`;
  `python scripts\real_accountant_response_packet.py --response schedule`;
  `python scripts\real_accountant_run_sheet.py`;
  `python scripts\real_accountant_preflight.py`;
  `python scripts\real_accountant_outreach_update.py --ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08`;
  scaffold: `python scripts\real_accountant_notes_scaffold.py --out docs\reports\real-accountant-session\actual-feedback-notes.md --date 2026-07-05 --reviewer-role "CPA reviewer" --reviewer-service-line "F-ACC" --reviewer-experience-context "reviewed accounting advisory workpapers" --session-mode "async review"`;
  notes gate: `python scripts\real_accountant_notes_check.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md`)
- [ ] RS3 — capture and queue conversion. (verify: actual notes gate + `real_accountant_capture.py` + actual capture manifest with `actual_feedback_evidence: true` + `real_accountant_manifest_build.py`)
- [ ] RS4 — close gate. (verify: `real_accountant_close_check.py --run-quality-preflight` + actual feedback evidence)

## 결정 로그

- 결정: 실제 세션이 없으면 horizon을 닫지 않는다.
- 결정: 실제 reviewer가 준비되기 전에는 session invite/evidence template/packet/outreach ledger tooling까지만 만든다.
- 결정: actual feedback evidence는 reviewer metadata와 public-safe notes가 있을 때만 true로 표시한다.
- 결정: actual notes는 `real_accountant_notes_check.py`를 통과하기 전에는 capture/queue 변환하지 않는다.
- 결정: actual session manifest는 수동 편집이 아니라 `real_accountant_manifest_build.py`로 생성한다.
- 결정: horizon close는 `real_accountant_close_check.py`가 actual manifest, notes, queue, outreach completed, quality preflight를 통과할 때만 한다.
- 사용자 소유 결정: 현재 없음. 회계사 reviewer 섭외, 일정 조율, 실제 세션 진행은 active plan에서 제외한다.

## 중단점

- 사용자가 이 horizon을 다시 열기 전에는 RS2 이후로 진행하지 않는다.
- raw contract/customer data를 notes로 받게 되면 capture하지 않는다.
