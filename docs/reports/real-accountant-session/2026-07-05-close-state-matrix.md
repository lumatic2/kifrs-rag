# RS4 Close State Matrix

> Scope: prove which real-accountant-session state combinations must remain blocked and which combination can close.

## 한 줄 결론

The close gate behaves correctly across the state matrix: every pre-actual or pre-completed combination stays blocked, and only `actual_feedback` plus `completed` outreach is close-ready.

## Summary

- ok: True
- total rows: 8
- blocked rows: 7
- passing close rows: 1
- only actual_feedback+completed closes: True

## Matrix

| Manifest | Outreach | Expected close | Actual close | Primary blockers |
|---|---|---:|---:|---|
| ready_to_schedule | not_sent | False | False | manifest_not_actual_feedback; missing_notes_file; missing_queue_jsonl; no_completed_outreach |
| ready_to_schedule | sent | False | False | manifest_not_actual_feedback; missing_notes_file; missing_queue_jsonl; no_completed_outreach |
| ready_to_schedule | scheduled | False | False | manifest_not_actual_feedback; missing_notes_file; missing_queue_jsonl; no_completed_outreach |
| ready_to_schedule | completed | False | False | manifest_not_actual_feedback; missing_notes_file; missing_queue_jsonl |
| actual_feedback | not_sent | False | False | no_completed_outreach |
| actual_feedback | sent | False | False | no_completed_outreach |
| actual_feedback | scheduled | False | False | no_completed_outreach |
| actual_feedback | completed | True | True | none |

## Boundary

- This matrix uses copied ledgers and temporary synthetic actual-feedback inputs only.
- It does not update the real session manifest, outreach ledger, notes, capture manifest, or queue JSONL.
- Close is expected only when actual-feedback manifest evidence and completed outreach are both present.

## Next Leaf

operator sends invite; after real notes exist, use the close matrix expectation to verify RS4 close conditions

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "gate_id": "rs4-close-state-matrix",
  "rows": [
    {
      "manifest_mode": "ready_to_schedule",
      "outreach_state": "not_sent",
      "expected_close": false,
      "close_ready": false,
      "primary_blockers": [
        "manifest_not_actual_feedback",
        "missing_notes_file",
        "missing_queue_jsonl",
        "no_completed_outreach"
      ],
      "evidence": {
        "session_mode": "ready_to_schedule",
        "outreach_counts": {
          "completed": 0,
          "declined": 0,
          "not_sent": 1,
          "responded": 0,
          "scheduled": 0,
          "sent": 0
        },
        "quality_preflight": "not_run"
      }
    },
    {
      "manifest_mode": "ready_to_schedule",
      "outreach_state": "sent",
      "expected_close": false,
      "close_ready": false,
      "primary_blockers": [
        "manifest_not_actual_feedback",
        "missing_notes_file",
        "missing_queue_jsonl",
        "no_completed_outreach"
      ],
      "evidence": {
        "session_mode": "ready_to_schedule",
        "outreach_counts": {
          "completed": 0,
          "declined": 0,
          "not_sent": 0,
          "responded": 0,
          "scheduled": 0,
          "sent": 1
        },
        "quality_preflight": "not_run"
      }
    },
    {
      "manifest_mode": "ready_to_schedule",
      "outreach_state": "scheduled",
      "expected_close": false,
      "close_ready": false,
      "primary_blockers": [
        "manifest_not_actual_feedback",
        "missing_notes_file",
        "missing_queue_jsonl",
        "no_completed_outreach"
      ],
      "evidence": {
        "session_mode": "ready_to_schedule",
        "outreach_counts": {
          "completed": 0,
          "declined": 0,
          "not_sent": 0,
          "responded": 0,
          "scheduled": 1,
          "sent": 0
        },
        "quality_preflight": "not_run"
      }
    },
    {
      "manifest_mode": "ready_to_schedule",
      "outreach_state": "completed",
      "expected_close": false,
      "close_ready": false,
      "primary_blockers": [
        "manifest_not_actual_feedback",
        "missing_notes_file",
        "missing_queue_jsonl"
      ],
      "evidence": {
        "session_mode": "ready_to_schedule",
        "outreach_counts": {
          "completed": 1,
          "declined": 0,
          "not_sent": 0,
          "responded": 0,
          "scheduled": 0,
          "sent": 0
        },
        "quality_preflight": "not_run"
      }
    },
    {
      "manifest_mode": "actual_feedback",
      "outreach_state": "not_sent",
      "expected_close": false,
      "close_ready": false,
      "primary_blockers": [
        "no_completed_outreach"
      ],
      "evidence": {
        "session_mode": "actual_feedback",
        "notes_public_safe": true,
        "queue_records": 1,
        "outreach_counts": {
          "completed": 0,
          "declined": 0,
          "not_sent": 1,
          "responded": 0,
          "scheduled": 0,
          "sent": 0
        },
        "quality_preflight": "not_run"
      }
    },
    {
      "manifest_mode": "actual_feedback",
      "outreach_state": "sent",
      "expected_close": false,
      "close_ready": false,
      "primary_blockers": [
        "no_completed_outreach"
      ],
      "evidence": {
        "session_mode": "actual_feedback",
        "notes_public_safe": true,
        "queue_records": 1,
        "outreach_counts": {
          "completed": 0,
          "declined": 0,
          "not_sent": 0,
          "responded": 0,
          "scheduled": 0,
          "sent": 1
        },
        "quality_preflight": "not_run"
      }
    },
    {
      "manifest_mode": "actual_feedback",
      "outreach_state": "scheduled",
      "expected_close": false,
      "close_ready": false,
      "primary_blockers": [
        "no_completed_outreach"
      ],
      "evidence": {
        "session_mode": "actual_feedback",
        "notes_public_safe": true,
        "queue_records": 1,
        "outreach_counts": {
          "completed": 0,
          "declined": 0,
          "not_sent": 0,
          "responded": 0,
          "scheduled": 1,
          "sent": 0
        },
        "quality_preflight": "not_run"
      }
    },
    {
      "manifest_mode": "actual_feedback",
      "outreach_state": "completed",
      "expected_close": true,
      "close_ready": true,
      "primary_blockers": [],
      "evidence": {
        "session_mode": "actual_feedback",
        "notes_public_safe": true,
        "queue_records": 1,
        "outreach_counts": {
          "completed": 1,
          "declined": 0,
          "not_sent": 0,
          "responded": 0,
          "scheduled": 0,
          "sent": 0
        },
        "quality_preflight": "not_run"
      }
    }
  ],
  "summary": {
    "total_rows": 8,
    "passing_close_rows": 1,
    "blocked_rows": 7,
    "only_actual_feedback_completed_closes": true
  },
  "boundary": [
    "This matrix uses copied ledgers and temporary synthetic actual-feedback inputs only.",
    "It does not update the real session manifest, outreach ledger, notes, capture manifest, or queue JSONL.",
    "Close is expected only when actual-feedback manifest evidence and completed outreach are both present."
  ],
  "report_path": "docs/reports/real-accountant-session/2026-07-05-close-state-matrix.md",
  "next_leaf": "operator sends invite; after real notes exist, use the close matrix expectation to verify RS4 close conditions"
}
```
