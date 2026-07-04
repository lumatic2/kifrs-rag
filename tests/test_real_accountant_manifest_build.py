from __future__ import annotations

import json

import pytest

from scripts.real_accountant_manifest_build import build_actual_manifest


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


def _write_actual_inputs(tmp_path):
    notes = tmp_path / "actual-feedback-notes.md"
    notes.write_text(_safe_notes(), encoding="utf-8")
    capture = tmp_path / "capture-manifest.json"
    capture.write_text(json.dumps({"actual_feedback_evidence": True}), encoding="utf-8")
    queue = tmp_path / "feedback-queue.jsonl"
    queue.write_text(json.dumps(_queue_record(), ensure_ascii=False) + "\n", encoding="utf-8")
    return notes, capture, queue


def test_build_actual_manifest_writes_valid_session_manifest(tmp_path) -> None:
    notes, capture, queue = _write_actual_inputs(tmp_path)
    out = tmp_path / "session_manifest.json"

    manifest = build_actual_manifest(
        root=tmp_path,
        out=out,
        notes=notes,
        capture_manifest=capture,
        queue_jsonl=queue,
        reviewer_role="CPA reviewer",
        reviewer_service_line="F-ACC",
        reviewer_experience_context="reviewed accounting advisory workpapers",
    )

    assert manifest["actual_feedback_evidence"] is True
    assert manifest["queue_records"] == 1
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["status"] == "actual_feedback"
    assert written["notes_file"] == "actual-feedback-notes.md"


def test_build_actual_manifest_rejects_non_actual_capture_manifest(tmp_path) -> None:
    notes, capture, queue = _write_actual_inputs(tmp_path)
    capture.write_text(json.dumps({"actual_feedback_evidence": False}), encoding="utf-8")

    with pytest.raises(ValueError, match="actual_feedback_evidence must be true"):
        build_actual_manifest(
            root=tmp_path,
            out=tmp_path / "session_manifest.json",
            notes=notes,
            capture_manifest=capture,
            queue_jsonl=queue,
            reviewer_role="CPA reviewer",
            reviewer_service_line="F-ACC",
            reviewer_experience_context="reviewed accounting advisory workpapers",
        )


def test_build_actual_manifest_rejects_empty_queue_by_default(tmp_path) -> None:
    notes, capture, queue = _write_actual_inputs(tmp_path)
    queue.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="at least one queue record"):
        build_actual_manifest(
            root=tmp_path,
            out=tmp_path / "session_manifest.json",
            notes=notes,
            capture_manifest=capture,
            queue_jsonl=queue,
            reviewer_role="CPA reviewer",
            reviewer_service_line="F-ACC",
            reviewer_experience_context="reviewed accounting advisory workpapers",
        )


def test_build_actual_manifest_rejects_unchecked_notes(tmp_path) -> None:
    notes, capture, queue = _write_actual_inputs(tmp_path)
    notes.write_text(_safe_notes().replace("- [x] No raw contract copied", "- [ ] No raw contract copied"), encoding="utf-8")

    with pytest.raises(ValueError, match="boundary checkbox not confirmed"):
        build_actual_manifest(
            root=tmp_path,
            out=tmp_path / "session_manifest.json",
            notes=notes,
            capture_manifest=capture,
            queue_jsonl=queue,
            reviewer_role="CPA reviewer",
            reviewer_service_line="F-ACC",
            reviewer_experience_context="reviewed accounting advisory workpapers",
        )
