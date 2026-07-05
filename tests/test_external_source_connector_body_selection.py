from __future__ import annotations

from scripts.external_source_connector_body_selection import build_selection, render_markdown


def test_external_source_connector_body_selection_picks_safe_first_lane() -> None:
    result = build_selection()

    assert result["ok"] is True
    assert result["horizon"] == "external-source-body-connector-expansion"
    assert result["completed_milestone"] == "ESB1"
    assert result["selected_source_class"]["source_class"] == "interpretive_accounting_material"
    assert result["selected_source_class"]["implementation_status"] == "selected_for_ESB2"
    assert result["policy"]["live_fetching_allowed_by_ESB1"] is False
    assert result["policy"]["body_chunking_allowed_by_ESB1"] is False
    assert result["policy"]["embedding_allowed_by_ESB1"] is False
    assert result["checks"]["authorization_boundary_explicit"] is True
    assert result["checks"]["allowed_public_fields_do_not_include_blocked_fields"] is True
    assert result["next_leaf"] == "ESB2_synthetic_connector_body_fixture_contract"


def test_external_source_connector_body_selection_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_selection())

    assert "ESB1 Source-Body Connector Selection And Policy Gate" in rendered
    assert "interpretive_accounting_material" in rendered
    assert "live fetching: False" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "password" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
