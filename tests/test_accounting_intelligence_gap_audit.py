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
    assert "local parser real-adapter decision gate is present and deferred" in joined_gaps
    assert "parser/deletion automation" in joined_gaps
    assert "external source connector-specific policy record is present" in joined_gaps
    assert "connector metadata dry-run is not implemented" in joined_gaps
    assert "opt-in retriever demo validation is complete" in joined_gaps


def test_gap_audit_markdown_is_public_safe_summary() -> None:
    markdown = render_markdown(build_gap_audit())

    assert "source_body" not in markdown
    assert "api_key" not in markdown
    assert "token" not in markdown
    assert "Accounting Intelligence Gap Audit" in markdown
    assert "Automation rate" in markdown
