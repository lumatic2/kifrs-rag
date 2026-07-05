from __future__ import annotations

from scripts.workflow_sample_contract_pack import build_contract_pack, render_markdown


def test_workflow_sample_contract_pack_defines_adapter_ready_contract() -> None:
    result = build_contract_pack()

    assert result["ok"] is True
    assert result["horizon"] == "workflow-coverage-depth-expansion"
    assert result["completed_milestone"] == "WCD2"
    assert result["workflow"]["workflow_id"] == "audit_disclosure_tie_out"
    assert result["workflow"]["status"] == "selected_for_minimal_adapter"
    assert len(result["input_facts"]) >= 5
    assert len(result["authority_needs"]) >= 4
    assert "human_review_required_items" in result["output_surface"]
    assert any("may not" in item for item in result["review_boundary"])
    assert result["next_leaf"] == "WCD3_minimal_adapter_expansion"


def test_workflow_sample_contract_pack_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_contract_pack())

    assert "WCD2 Workflow Sample Contract Pack" in rendered
    assert "audit_disclosure_tie_out" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
    assert "external accountant feedback" not in rendered.lower()
