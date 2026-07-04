from __future__ import annotations

import pytest

from kifrs.workflows.source_aware_rebuild import (
    assert_public_safe_report,
    build_default_rebuild_report,
    render_rebuild_report_markdown,
)


def test_default_rebuild_report_covers_all_public_review_pack_fixtures() -> None:
    report = build_default_rebuild_report()

    assert report.total_packs == 24
    assert {item.standard for item in report.summaries} == {"KIFRS1109", "KIFRS1115", "KIFRS1116"}
    assert report.automated_packs > report.human_review_packs


def test_default_rebuild_report_counts_external_evidence_roles() -> None:
    report = build_default_rebuild_report()

    assert report.aggregate_external_roles == {
        "fact_evidence": 24,
        "legal_boundary": 24,
        "supporting_interpretation": 24,
    }
    assert all(summary.fact_evidence_count == 1 for summary in report.summaries)


def test_rebuild_report_is_public_safe_data() -> None:
    report = build_default_rebuild_report()

    assert_public_safe_report(report.to_dict())

    with pytest.raises(ValueError, match="source payload fields"):
        assert_public_safe_report({"summaries": [{"source_body": "not allowed"}]})


def test_rebuild_report_markdown_renders_decision_boundary() -> None:
    report = build_default_rebuild_report()
    rendered = render_rebuild_report_markdown(report)

    assert "# Source-Aware Workflow Rebuild Report" in rendered
    assert "KIFRS1109" in rendered
    assert "KIFRS1115" in rendered
    assert "KIFRS1116" in rendered
    assert "Human-review items are counted, not removed." in rendered
    assert "source_body" not in rendered
