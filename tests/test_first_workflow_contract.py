from __future__ import annotations

from scripts.first_workflow_contract import build_first_workflow_contract, render_markdown


def test_first_workflow_contract_matches_wce1_recommendation() -> None:
    result = build_first_workflow_contract()
    contract = result["contract"]

    assert result["ok"], result["errors"]
    assert result["horizon"] == "workflow-coverage-expansion"
    assert result["completed_milestone"] == "WCE2"
    assert result["selected_candidate"] == "1037_provisions"
    assert contract["workflow_id"] == "1037_provisions"
    assert contract["standard_scope"] == ["KIFRS1037"]
    assert {item["name"] for item in contract["inputs"]} >= {
        "obligating_event",
        "obligation_type",
        "outflow_probability",
    }
    assert "recognition_assessment" in contract["outputs"]
    assert "human_review_checklist" in contract["outputs"]
    assert any(role["role"] == "primary_kifrs" for role in contract["evidence_roles"])
    assert "final recognition conclusion" in contract["human_review_boundary"]
    assert contract["next_adapter"] == "minimal_workflow_review_pack_adapter"


def test_first_workflow_contract_report_is_public_safe() -> None:
    rendered = render_markdown(build_first_workflow_contract())

    assert "WCE2 First Workflow Candidate Contract" in rendered
    assert "1037_provisions" in rendered
    assert "final conclusion and estimate judgment stay with the accountant" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
