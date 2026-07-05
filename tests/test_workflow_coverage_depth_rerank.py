from __future__ import annotations

from scripts.workflow_coverage_depth_rerank import build_rerank, render_markdown


def test_workflow_coverage_depth_rerank_selects_public_safe_broader_workflow() -> None:
    result = build_rerank()

    assert result["ok"] is True
    assert result["horizon"] == "workflow-coverage-depth-expansion"
    assert result["completed_milestone"] == "WCD1"
    assert result["recommended_workflow"]["workflow_id"] == "audit_disclosure_tie_out"
    assert result["ranked_gaps"][0]["recommended_next"] is True
    assert result["ranked_gaps"][0]["public_safety"] >= 4
    assert result["ranked_gaps"][0]["evidence_availability"] >= 4
    assert len({gap["service_line"] for gap in result["ranked_gaps"]}) >= 4
    assert result["checks"]["no_external_dependency_required"] is True
    assert result["next_leaf"] == "WCD2_workflow_sample_contract_pack"


def test_workflow_coverage_depth_rerank_markdown_avoids_parked_work() -> None:
    rendered = render_markdown(build_rerank())

    assert "WCD1 Service-Line Coverage Rerank" in rendered
    assert "audit_disclosure_tie_out" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
    assert "external accountant feedback" not in rendered.lower()
