from __future__ import annotations

from scripts.e2e_scenario_contract import build_scenario_contract, render_markdown


def test_e2e_scenario_contract_defines_required_stage_boundaries() -> None:
    contract = build_scenario_contract()

    assert contract["ok"] is True
    assert contract["horizon"] == "end-to-end-demo-scenario"
    assert contract["completed_milestone"] == "E2E2"
    assert contract["next_leaf"] == "E2E3_demo_packet_builder"
    assert contract["contract"]["scenario_id"] == "public_safe_firm_demo_v1"
    for stage in contract["stages"]:
        assert stage["input_signal"]
        assert stage["evidence_exists"] is True
        assert stage["output"]
        assert stage["review_checkpoint"]
        assert stage["operator_command"].startswith("python scripts\\")
        assert stage["failure_boundary"]


def test_e2e_scenario_contract_markdown_is_public_safe_and_demo_scoped() -> None:
    rendered = render_markdown(build_scenario_contract())

    assert "E2E2 Scenario Contract" in rendered
    assert "It does not replace final accounting judgment." in rendered
    assert "It does not prove production deployment readiness." in rendered
    assert "It does not expose protected local data." in rendered
    assert "python scripts\\runtime_retriever_promotion_close_gate.py --format text" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
