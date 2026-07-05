from __future__ import annotations

from scripts.accounting_intelligence_gap_audit import build_gap_audit, render_markdown


def test_gap_audit_covers_current_expansion_evidence() -> None:
    audit = build_gap_audit()

    assert audit.ok, audit.errors
    assert audit.missing_reports == []
    assert audit.missing_demo_outputs == []
    assert audit.source_manifest_ok is True
    assert audit.evidence_manifest_ok is True
    assert audit.total_review_packs == 24
    assert audit.automated_packs >= 20
    assert audit.human_review_packs <= 4
    joined_gaps = " ".join(audit.remaining_gaps)
    assert "actual accountant session" in joined_gaps
    assert "decision queue, reviewer invite action packet, readiness index, external-action boundary, invite, response handling, after-send action matrix, scheduled-session, RS3 notes-quality/capture-readiness/post-session final gate, operator execution brief, pre-send final gate, and close-state matrix are ready" in joined_gaps
    assert "reviewer invite has not been sent" in joined_gaps
    assert "local parser real-adapter implementation plan is present" in joined_gaps
    assert "explicit authorization" in joined_gaps
    assert "parser/deletion automation" in joined_gaps
    assert "external source connector metadata-only lane is closed" in joined_gaps
    assert "authorization record scaffold is present" in joined_gaps
    assert "demo-noted" in joined_gaps
    assert "source-body connector is still not implemented" in joined_gaps
    assert "opt-in retriever promotion decision gate is present" in joined_gaps
    assert "default retriever change remains deferred" in joined_gaps


def test_gap_audit_markdown_is_public_safe_summary() -> None:
    markdown = render_markdown(build_gap_audit())

    assert "source_body" not in markdown
    assert "api_key" not in markdown
    assert "token" not in markdown
    assert "Accounting Intelligence Gap Audit" in markdown
    assert "Automation rate" in markdown
