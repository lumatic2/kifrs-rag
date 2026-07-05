from __future__ import annotations

from scripts.external_source_connector_body_fixture_contract import build_fixture_contract, render_markdown


def test_external_source_connector_body_fixture_contract_defines_safe_schema() -> None:
    result = build_fixture_contract()

    assert result["ok"] is True
    assert result["horizon"] == "external-source-body-connector-expansion"
    assert result["completed_milestone"] == "ESB2"
    assert result["selected_source_class"] == "interpretive_accounting_material"
    assert result["sample_fixture"]["policy_status"] == "synthetic_dry_run_only"
    assert result["chunk_output_schema"]["contains_copied_body_payload"] is False
    assert result["checks"]["fixture_has_no_copied_payload"] is True
    assert result["checks"]["chunk_contract_blocks_copied_payload"] is True
    assert result["next_leaf"] == "ESB3_chunking_and_retrieval_dry_run"


def test_external_source_connector_body_fixture_contract_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_fixture_contract())

    assert "ESB2 Synthetic Source-Body Fixture Contract" in rendered
    assert "synthetic fixture contract" in rendered
    assert "author_written_placeholder_label_only" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "password" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
