from __future__ import annotations

from scripts.private_parser_fixture_adapter_contract import build_fixture_adapter_contract, render_markdown


def test_private_parser_fixture_adapter_contract_defines_file_classes_and_schema() -> None:
    contract = build_fixture_adapter_contract()

    assert contract["ok"] is True
    assert contract["horizon"] == "private-parser-realism-hardening"
    assert contract["completed_milestone"] == "PPR2"
    assert contract["next_leaf"] == "PPR3_deletion_and_retention_rehearsal"
    assert len(contract["file_classes"]) >= 3
    assert "needs_human_review" in contract["output_schema"]
    assert "raw_payload" not in contract["output_schema"]
    assert all(item["exists"] for item in contract["evidence"])
    assert {state["state"] for state in contract["failure_states"]} >= {
        "unsupported_file_type",
        "parse_confidence_low",
        "redaction_required",
        "authorization_missing",
    }


def test_private_parser_fixture_adapter_contract_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_fixture_adapter_contract())

    assert "PPR2 Realistic Local Fixture Adapter Contract" in rendered
    assert "structured facts" in rendered
    assert "authorization_missing" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
