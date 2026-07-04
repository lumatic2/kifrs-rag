from __future__ import annotations

import json

from scripts.real_accountant_close_check import check_close_gate


def _safe_notes() -> str:
    return """# Real Accountant Session Evidence

## Session Metadata

- Date: 2026-07-05
- Reviewer role: CPA reviewer
- Reviewer service-line: F-ACC
- Reviewer experience context: reviewed accounting advisory workpapers
- Session mode: async review
- Actual feedback evidence: true

## Scores

- Workflow fit (1-5): 4
- Evidence boundary clarity (1-5): 5
- Review pack usefulness (1-5): 4
- Human-review boundary clarity (1-5): 5
- Real-case PoC willingness (1-5): 3

## Top Positive

The review pack structure is understandable.

## Top Risk

Evidence requests need sharper wording.

## Missing Inputs

- approval memo existence

## Review Question Additions

- Ask whether approval memo evidence exists.

## Safe Correction Candidates

### Candidate 1

- Case id: anon-lease-poc-001
- Issue: reviewer question should mention approval memo evidence
- Severity: medium
- Suggested fix: add approval memo evidence question
- Missing evidence: approval memo existence
- Disposition: eval_seed_candidate
- Affected outputs: human_review_questions

## Boundary Confirmation

- [x] No raw contract copied
- [x] No customer/client/company identifier copied
- [x] No private filing body copied
- [x] No K-IFRS source text copied
- [x] Notes are safe to convert into queue candidates
"""


def _queue_record() -> dict[str, object]:
    return {
        "affected_outputs": ["human_review_questions"],
        "case_id": "anon-lease-poc-001",
        "disposition": "candidate",
        "domain": "KIFRS1116",
        "expected_improvement": "Add approval memo evidence question.",
        "issue": "reviewer question should mention approval memo evidence",
        "missing_evidence": ["approval memo existence"],
        "record_id": "anon-lease-poc-001:eval_seed_candidate:approval-memo",
        "route": "kifrs1116_review_pack",
        "severity": "medium",
        "source": "real-accountant-session",
        "version": 1,
    }


def _write_actual_close_inputs(tmp_path, *, outreach_status: str = "completed", queue_records: int = 1):
    notes = tmp_path / "actual-feedback-notes.md"
    notes.write_text(_safe_notes(), encoding="utf-8")
    capture = tmp_path / "capture-manifest.json"
    capture.write_text(json.dumps({"actual_feedback_evidence": True}), encoding="utf-8")
    queue = tmp_path / "feedback-queue.jsonl"
    queue.write_text(
        "".join(json.dumps(_queue_record(), ensure_ascii=False) + "\n" for _ in range(queue_records)),
        encoding="utf-8",
    )
    manifest = tmp_path / "session_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "actual_feedback_evidence": True,
                "reviewer_metadata": {
                    "role": "CPA reviewer",
                    "service_line": "F-ACC",
                    "experience_context": "reviewed accounting advisory workpapers",
                },
                "notes_file": "actual-feedback-notes.md",
                "capture_manifest": "capture-manifest.json",
                "queue_jsonl": "feedback-queue.jsonl",
            }
        ),
        encoding="utf-8",
    )
    outreach = tmp_path / "outreach.jsonl"
    outreach.write_text(
        json.dumps(
            {
                "reviewer_alias": "reviewer-001",
                "status": outreach_status,
                "invite_sent": outreach_status in {"sent", "responded", "scheduled", "completed"},
                "channel": "manual",
                "contacted_at": "2026-07-05",
                "follow_up_by": "2026-07-08",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest, outreach


def test_close_gate_passes_with_actual_manifest_notes_queue_and_completed_outreach(tmp_path) -> None:
    manifest, outreach = _write_actual_close_inputs(tmp_path)

    ok, errors, evidence = check_close_gate(root=tmp_path, manifest_path=manifest, outreach_ledger=outreach)

    assert ok is True
    assert errors == []
    assert evidence["session_mode"] == "actual_feedback"
    assert evidence["queue_records"] == 1
    assert evidence["outreach_counts"]["completed"] == 1


def test_close_gate_rejects_ready_to_schedule_manifest(tmp_path) -> None:
    manifest = tmp_path / "session_manifest.json"
    manifest.write_text(json.dumps({"actual_feedback_evidence": False}), encoding="utf-8")
    outreach = tmp_path / "outreach.jsonl"
    outreach.write_text("", encoding="utf-8")

    ok, errors, _evidence = check_close_gate(root=tmp_path, manifest_path=manifest, outreach_ledger=outreach)

    assert ok is False
    assert "session_manifest: mode must be actual_feedback, got ready_to_schedule" in errors


def test_close_gate_rejects_uncompleted_outreach(tmp_path) -> None:
    manifest, outreach = _write_actual_close_inputs(tmp_path, outreach_status="scheduled")

    ok, errors, _evidence = check_close_gate(root=tmp_path, manifest_path=manifest, outreach_ledger=outreach)

    assert ok is False
    assert "outreach: at least one completed reviewer session is required" in errors


def test_close_gate_rejects_empty_queue(tmp_path) -> None:
    manifest, outreach = _write_actual_close_inputs(tmp_path, queue_records=0)

    ok, errors, _evidence = check_close_gate(root=tmp_path, manifest_path=manifest, outreach_ledger=outreach)

    assert ok is False
    assert "queue_jsonl: at least one queue record is required" in errors
