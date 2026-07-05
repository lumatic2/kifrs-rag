from __future__ import annotations

from scripts.workflow_depth_minimal_adapter import build_adapter_report, render_markdown, run_adapter


def test_workflow_depth_minimal_adapter_outputs_decision_prep_metadata() -> None:
    result = build_adapter_report()

    assert result["ok"] is True
    assert result["horizon"] == "workflow-coverage-depth-expansion"
    assert result["completed_milestone"] == "WCD3"
    assert result["adapter_output"]["workflow_id"] == "audit_disclosure_tie_out"
    assert result["adapter_output"]["prepared_disclosure_tie_out_status"] == "partial"
    assert result["adapter_output"]["final_audit_conclusion"] is None
    assert "audit_sufficiency" in result["adapter_output"]["human_review_required_items"]
    assert result["next_leaf"] == "WCD4_coverage_depth_metric_update"


def test_workflow_depth_minimal_adapter_has_failure_relevant_flags() -> None:
    output = run_adapter(
        {
            "workflow_id": "audit_disclosure_tie_out",
            "review_pack_refs": ["report-a", "report-b"],
        }
    )

    assert "lease_expense_split_label" in output["missing_or_ambiguous_evidence_flags"]
    assert "significant_judgement_label" in output["missing_or_ambiguous_evidence_flags"]


def test_workflow_depth_minimal_adapter_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_adapter_report())

    assert "WCD3 Minimal Adapter Expansion" in rendered
    assert "final audit conclusion: None" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
