from __future__ import annotations

import json

import pytest

from scripts.real_accountant_capture import capture_actual_notes, parse_actual_notes


def _actual_notes() -> str:
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

- lease term approval evidence

## Review Question Additions

- Ask whether approval memo evidence exists.

## Safe Correction Candidates

### Candidate 1

- Case id: anon-lease-poc-001
- Issue: Lease term evidence question should be explicit
- Severity: medium
- Suggested fix: Add a required reviewer question for lease term evidence.
- Missing evidence: lease term approval evidence
- Disposition: eval_seed_candidate
- Affected outputs: human_review_questions, review_pack

## Boundary Confirmation

- [x] No raw contract copied
- [x] No customer/client/company identifier copied
- [x] No private filing body copied
- [x] No K-IFRS source text copied
- [x] Notes are safe to convert into queue candidates
"""


def test_parse_actual_notes_builds_feedback_session_notes(tmp_path) -> None:
    path = tmp_path / "actual-feedback-notes.md"
    path.write_text(_actual_notes(), encoding="utf-8")

    notes = parse_actual_notes(path)

    assert notes.source == "field_session"
    assert notes.reviewer_role == "CPA reviewer"
    assert notes.scores["workflow_fit"] == 4
    assert notes.corrections[0].case_id == "anon-lease-poc-001"


def test_capture_actual_notes_writes_manifest_and_queue(tmp_path) -> None:
    path = tmp_path / "actual-feedback-notes.md"
    out = tmp_path / "capture"
    path.write_text(_actual_notes(), encoding="utf-8")

    paths = capture_actual_notes(path, out, root=tmp_path)

    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    assert manifest["actual_feedback_evidence"] is True
    assert manifest["queue_records"] == 1
    assert paths["queue_jsonl"].read_text(encoding="utf-8").strip()
    assert "Queue records generated: 1" in paths["capture_report"].read_text(encoding="utf-8")


def test_capture_actual_notes_rejects_unchecked_scaffold(tmp_path) -> None:
    path = tmp_path / "actual-feedback-notes.md"
    path.write_text(_actual_notes().replace("- [x] No raw contract copied", "- [ ] No raw contract copied"), encoding="utf-8")

    with pytest.raises(ValueError, match="boundary checkbox not confirmed"):
        capture_actual_notes(path, tmp_path / "capture", root=tmp_path)
