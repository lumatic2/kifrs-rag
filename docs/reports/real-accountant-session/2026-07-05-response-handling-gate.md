# RS2 Response Handling Gate

> Scope: verify public-safe follow-up, schedule, and decline handling after the reviewer invite is sent.

## 한 줄 결론

The RS2 response path is ready: follow-up keeps the alias at `sent`, schedule moves a copied ledger to `scheduled`, and decline moves it to `declined` without protected identifiers. This gate does not contact the reviewer.

## Current State

- ok: True
- ledger: `docs/reports/real-accountant-session/outreach-log.sample.jsonl`
- current outreach counts: {'completed': 0, 'declined': 0, 'not_sent': 1, 'responded': 0, 'scheduled': 0, 'sent': 0}

## Response Commands

### decline

- message preview: 확인 감사합니다. 이번에는 어렵다는 점 이해했습니다.

```powershell
python scripts\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status declined --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "reviewer declined"
```

### follow_up

- message preview: 안녕하세요. 앞서 드린 회계 AI PoC 30분 피드백 요청 관련해 짧게 확인드립니다.

```powershell
python scripts\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "follow-up sent"
```

### schedule

- message preview: 가능한 시간 알려주셔서 감사합니다. 30분 세션에서는 public-safe demo만 보고, 고객자료나 계약 원문은 받지 않겠습니다.

```powershell
python scripts\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status scheduled --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "session scheduled"
```

## Simulations

- decline: ok=True, expected_status=declined, counts={'completed': 0, 'declined': 1, 'not_sent': 0, 'responded': 0, 'scheduled': 0, 'sent': 0}
- follow_up: ok=True, expected_status=sent, counts={'completed': 0, 'declined': 0, 'not_sent': 0, 'responded': 0, 'scheduled': 0, 'sent': 1}
- schedule: ok=True, expected_status=scheduled, counts={'completed': 0, 'declined': 0, 'not_sent': 0, 'responded': 0, 'scheduled': 1, 'sent': 0}

## Boundary

- This gate does not contact the reviewer.
- The operator handles the real reply manually, then runs the matching ledger update command.
- Scheduling details that identify a person stay outside the public repo.
- Declines are valid RS2 outcomes but do not satisfy actual feedback evidence.

## Next Leaf

operator handles reviewer reply, updates outreach ledger, then either schedules RS2 or records decline

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "gate_id": "rs2-response-handling-gate",
  "ledger_path": "docs/reports/real-accountant-session/outreach-log.sample.jsonl",
  "current_outreach_counts": {
    "completed": 0,
    "declined": 0,
    "not_sent": 1,
    "responded": 0,
    "scheduled": 0,
    "sent": 0
  },
  "response_packets": {
    "decline": {
      "reviewer_alias": "reviewer-001",
      "response": "decline",
      "ledger_update_command": "python scripts\\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status declined --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"reviewer declined\"",
      "message_preview": "확인 감사합니다. 이번에는 어렵다는 점 이해했습니다."
    },
    "follow_up": {
      "reviewer_alias": "reviewer-001",
      "response": "follow_up",
      "ledger_update_command": "python scripts\\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"follow-up sent\"",
      "message_preview": "안녕하세요. 앞서 드린 회계 AI PoC 30분 피드백 요청 관련해 짧게 확인드립니다."
    },
    "schedule": {
      "reviewer_alias": "reviewer-001",
      "response": "schedule",
      "ledger_update_command": "python scripts\\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status scheduled --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"session scheduled\"",
      "message_preview": "가능한 시간 알려주셔서 감사합니다. 30분 세션에서는 public-safe demo만 보고, 고객자료나 계약 원문은 받지 않겠습니다."
    }
  },
  "response_simulations": {
    "decline": {
      "ok": true,
      "errors": [],
      "expected_status": "declined",
      "counts": {
        "completed": 0,
        "declined": 1,
        "not_sent": 0,
        "responded": 0,
        "scheduled": 0,
        "sent": 0
      },
      "row": {
        "reviewer_alias": "reviewer-001",
        "status": "declined",
        "invite_sent": true,
        "channel": "manual",
        "contacted_at": "2026-07-05",
        "follow_up_by": "2026-07-08",
        "notes": "reviewer declined"
      }
    },
    "follow_up": {
      "ok": true,
      "errors": [],
      "expected_status": "sent",
      "counts": {
        "completed": 0,
        "declined": 0,
        "not_sent": 0,
        "responded": 0,
        "scheduled": 0,
        "sent": 1
      },
      "row": {
        "reviewer_alias": "reviewer-001",
        "status": "sent",
        "invite_sent": true,
        "channel": "manual",
        "contacted_at": "2026-07-05",
        "follow_up_by": "2026-07-08",
        "notes": "follow-up sent"
      }
    },
    "schedule": {
      "ok": true,
      "errors": [],
      "expected_status": "scheduled",
      "counts": {
        "completed": 0,
        "declined": 0,
        "not_sent": 0,
        "responded": 0,
        "scheduled": 1,
        "sent": 0
      },
      "row": {
        "reviewer_alias": "reviewer-001",
        "status": "scheduled",
        "invite_sent": true,
        "channel": "manual",
        "contacted_at": "2026-07-05",
        "follow_up_by": "2026-07-08",
        "notes": "session scheduled"
      }
    }
  },
  "boundary": [
    "This gate does not contact the reviewer.",
    "The operator handles the real reply manually, then runs the matching ledger update command.",
    "Scheduling details that identify a person stay outside the public repo.",
    "Declines are valid RS2 outcomes but do not satisfy actual feedback evidence."
  ],
  "report_path": "docs/reports/real-accountant-session/2026-07-05-response-handling-gate.md",
  "next_leaf": "operator handles reviewer reply, updates outreach ledger, then either schedules RS2 or records decline"
}
```
