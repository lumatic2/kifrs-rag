# Real Accountant Session Execution Brief

> Scope: one execution surface for RS2 invite, RS2 scheduling, RS3 notes capture, and RS4 close gate.

## Current Position

- Horizon: real-accountant-session
- Session mode: ready_to_schedule
- Close ready: False
- Next action: Send reviewer invite and update outreach ledger to sent.
- Send subject: 회계 AI PoC 30분 피드백 요청 초안

## Blocked By

- reviewer invite has not been sent
- no completed reviewer session in outreach ledger
- session manifest is ready_to_schedule, not actual_feedback
- session_manifest: mode must be actual_feedback, got ready_to_schedule
- session_manifest: missing notes_file
- session_manifest: missing queue_jsonl
- outreach: at least one completed reviewer session is required

## Product Proof Snapshot

- Claim: technical demo package is ready for review, but final PoC proof requires an actual accountant session
- Automation rate: 83.33%
- Review packs: 20 automated / 24 total
- Needs human review: 4

## Run Order

### 1. Before sending

Render the invite, check dispatch readiness, then send the message manually.

```powershell
python scripts\real_accountant_status.py
```

```powershell
python scripts\real_accountant_invite_packet.py
```

```powershell
python scripts\real_accountant_invite_dispatch_gate.py --format text --write
```

### 2. After sending

Update the alias-only outreach ledger to sent.

```powershell
python scripts\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "invite sent"
```

### 3. After reviewer reply

Render the matching reply packet and update the ledger to follow-up, scheduled, or declined.

```powershell
python scripts\real_accountant_response_packet.py --response schedule
```

```powershell
python scripts\real_accountant_response_handling_gate.py --format text --write
```

### 4. Session day

Run the scheduled-session gate, open the run sheet, and conduct the 30-minute review.

```powershell
python scripts\real_accountant_scheduled_session_gate.py --format text --write
```

```powershell
python scripts\real_accountant_run_sheet.py
```

```powershell
python scripts\real_accountant_preflight.py
```

### 5. After session

Create public-safe notes, check them, capture queue records, and build the actual manifest.

```powershell
python scripts\real_accountant_capture_readiness_gate.py --format text --write
```

```powershell
python scripts\real_accountant_notes_scaffold.py --out docs\reports\real-accountant-session\actual-feedback-notes.md --date 2026-07-05 --reviewer-role "CPA reviewer" --reviewer-service-line "F-ACC" --reviewer-experience-context "reviewed accounting advisory workpapers" --session-mode "async review"
```

```powershell
python scripts\real_accountant_notes_check.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md
```

```powershell
python scripts\real_accountant_capture.py --notes docs\reports\real-accountant-session\actual-feedback-notes.md --out docs\reports\real-accountant-session
```

```powershell
python scripts\real_accountant_manifest_build.py --out docs\reports\real-accountant-session\session_manifest.json --notes docs\reports\real-accountant-session\actual-feedback-notes.md --capture-manifest docs\reports\real-accountant-session\capture-manifest.json --queue-jsonl docs\reports\real-accountant-session\feedback-queue.jsonl --reviewer-role "CPA reviewer" --reviewer-service-line "F-ACC" --reviewer-experience-context "reviewed accounting advisory workpapers"
```

### 6. Close

Only close the horizon after completed outreach, actual notes, capture manifest, queue JSONL, and close gate pass.

```powershell
python scripts\real_accountant_close_check.py --manifest docs\reports\real-accountant-session\session_manifest.json --outreach-ledger docs\reports\real-accountant-session\outreach-log.sample.jsonl --run-quality-preflight
```

## Decisions

- No repo-side product decision remains for this brief.
- The reviewer identity, real sending, scheduling, and actual feedback content are user/operator-owned.

## Boundary

- Use reviewer aliases only in repo artifacts.
- Do not store reviewer real name, customer name, company name, contract text, private filing body, or copied K-IFRS source text.
- Do not mark actual_feedback_evidence true until actual notes, capture manifest, queue JSONL, and manifest builder all pass.

## Machine Result

```json
{
  "title": "Real Accountant Session Execution Brief",
  "horizon": "real-accountant-session",
  "session_mode": "ready_to_schedule",
  "close_ready": false,
  "next_action": "Send reviewer invite and update outreach ledger to sent.",
  "blocked_by": [
    "reviewer invite has not been sent",
    "no completed reviewer session in outreach ledger",
    "session manifest is ready_to_schedule, not actual_feedback",
    "session_manifest: mode must be actual_feedback, got ready_to_schedule",
    "session_manifest: missing notes_file",
    "session_manifest: missing queue_jsonl",
    "outreach: at least one completed reviewer session is required"
  ],
  "proof_snapshot": {
    "automation_rate": 0.8333,
    "total_review_packs": 24,
    "automated_packs": 20,
    "human_review_packs": 4,
    "objective_ready_claim": "technical demo package is ready for review, but final PoC proof requires an actual accountant session",
    "remaining_gaps": [
      "actual accountant session evidence is still external/user-owned; invite, response handling, scheduled-session, RS3 capture-readiness, and operator execution brief are ready but the reviewer invite has not been sent",
      "local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation",
      "external source connector metadata-only lane is closed and demo-noted, but source-body connector is still not implemented",
      "opt-in retriever promotion decision gate is present, but default retriever change remains deferred until actual accountant evidence and explicit authorization"
    ]
  },
  "send_now_subject": "회계 AI PoC 30분 피드백 요청 초안",
  "post_send_update_command": "python scripts\\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"invite sent\"",
  "readiness_gates": {
    "invite_dispatch": "python scripts\\real_accountant_invite_dispatch_gate.py --format text --write",
    "response_handling": "python scripts\\real_accountant_response_handling_gate.py --format text --write",
    "scheduled_session": "python scripts\\real_accountant_scheduled_session_gate.py --format text --write",
    "capture_readiness": "python scripts\\real_accountant_capture_readiness_gate.py --format text --write"
  },
  "run_order": [
    {
      "phase": "1. Before sending",
      "operator_action": "Render the invite, check dispatch readiness, then send the message manually.",
      "commands": [
        "python scripts\\real_accountant_status.py",
        "python scripts\\real_accountant_invite_packet.py",
        "python scripts\\real_accountant_invite_dispatch_gate.py --format text --write"
      ]
    },
    {
      "phase": "2. After sending",
      "operator_action": "Update the alias-only outreach ledger to sent.",
      "commands": [
        "python scripts\\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"invite sent\""
      ]
    },
    {
      "phase": "3. After reviewer reply",
      "operator_action": "Render the matching reply packet and update the ledger to follow-up, scheduled, or declined.",
      "commands": [
        "python scripts\\real_accountant_response_packet.py --response schedule",
        "python scripts\\real_accountant_response_handling_gate.py --format text --write"
      ]
    },
    {
      "phase": "4. Session day",
      "operator_action": "Run the scheduled-session gate, open the run sheet, and conduct the 30-minute review.",
      "commands": [
        "python scripts\\real_accountant_scheduled_session_gate.py --format text --write",
        "python scripts\\real_accountant_run_sheet.py",
        "python scripts\\real_accountant_preflight.py"
      ]
    },
    {
      "phase": "5. After session",
      "operator_action": "Create public-safe notes, check them, capture queue records, and build the actual manifest.",
      "commands": [
        "python scripts\\real_accountant_capture_readiness_gate.py --format text --write",
        "python scripts\\real_accountant_notes_scaffold.py --out docs\\reports\\real-accountant-session\\actual-feedback-notes.md --date 2026-07-05 --reviewer-role \"CPA reviewer\" --reviewer-service-line \"F-ACC\" --reviewer-experience-context \"reviewed accounting advisory workpapers\" --session-mode \"async review\"",
        "python scripts\\real_accountant_notes_check.py --notes docs\\reports\\real-accountant-session\\actual-feedback-notes.md",
        "python scripts\\real_accountant_capture.py --notes docs\\reports\\real-accountant-session\\actual-feedback-notes.md --out docs\\reports\\real-accountant-session",
        "python scripts\\real_accountant_manifest_build.py --out docs\\reports\\real-accountant-session\\session_manifest.json --notes docs\\reports\\real-accountant-session\\actual-feedback-notes.md --capture-manifest docs\\reports\\real-accountant-session\\capture-manifest.json --queue-jsonl docs\\reports\\real-accountant-session\\feedback-queue.jsonl --reviewer-role \"CPA reviewer\" --reviewer-service-line \"F-ACC\" --reviewer-experience-context \"reviewed accounting advisory workpapers\""
      ]
    },
    {
      "phase": "6. Close",
      "operator_action": "Only close the horizon after completed outreach, actual notes, capture manifest, queue JSONL, and close gate pass.",
      "commands": [
        "python scripts\\real_accountant_close_check.py --manifest docs\\reports\\real-accountant-session\\session_manifest.json --outreach-ledger docs\\reports\\real-accountant-session\\outreach-log.sample.jsonl --run-quality-preflight"
      ]
    }
  ],
  "decisions": [
    "No repo-side product decision remains for this brief.",
    "The reviewer identity, real sending, scheduling, and actual feedback content are user/operator-owned."
  ],
  "boundary": [
    "Use reviewer aliases only in repo artifacts.",
    "Do not store reviewer real name, customer name, company name, contract text, private filing body, or copied K-IFRS source text.",
    "Do not mark actual_feedback_evidence true until actual notes, capture manifest, queue JSONL, and manifest builder all pass."
  ],
  "report_path": "docs/reports/real-accountant-session/2026-07-05-operator-execution-brief.md"
}
```
