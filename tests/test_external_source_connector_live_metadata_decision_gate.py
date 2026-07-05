from __future__ import annotations

from scripts.external_source_connector_live_metadata_decision_gate import (
    ALLOWED_LIVE_METADATA_FIELDS,
    FORBIDDEN_LIVE_METADATA_FIELDS,
    check_live_metadata_decision_gate,
    render_report,
)


def test_live_metadata_decision_allows_metadata_probe_only() -> None:
    result = check_live_metadata_decision_gate()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["decision"] == "allow_live_metadata_probe_scaffold"
    assert result["live_metadata_probe_allowed"] is True
    assert result["live_network_probe_allowed"] is True
    assert result["live_body_fetch_allowed"] is False
    assert result["body_cache_allowed"] is False
    assert result["chunking_allowed"] is False
    assert result["embedding_allowed"] is False
    assert result["indexing_allowed"] is False
    assert result["answer_time_body_use_allowed"] is False
    assert result["metadata_close_gate"]["ok"] is True
    assert result["live_contract"]["ok"] is True
    assert result["live_contract"]["network_checked_by_this_gate"] is False
    assert result["live_contract"]["body_text_stored"] is False


def test_live_metadata_decision_targets_kasb_and_fss_only() -> None:
    result = check_live_metadata_decision_gate()
    item_ids = {target["item_id"] for target in result["live_contract"]["connector_targets"]}

    assert item_ids == {
        "kasb-implementation-material-index",
        "fss-accounting-inquiry-index",
    }
    assert all(target["allowed_use"] == "supporting_interpretation" for target in result["live_contract"]["connector_targets"])
    assert all(target["body_text_stored"] is False for target in result["live_contract"]["connector_targets"])


def test_live_metadata_allowed_fields_exclude_body_and_secret_fields() -> None:
    assert set(ALLOWED_LIVE_METADATA_FIELDS).isdisjoint(FORBIDDEN_LIVE_METADATA_FIELDS)
    assert "final_url" in ALLOWED_LIVE_METADATA_FIELDS
    assert "content_type" in ALLOWED_LIVE_METADATA_FIELDS
    assert "body" in FORBIDDEN_LIVE_METADATA_FIELDS
    assert "raw_html" in FORBIDDEN_LIVE_METADATA_FIELDS
    assert "token" in FORBIDDEN_LIVE_METADATA_FIELDS


def test_live_metadata_decision_report_explains_next_leaf_and_boundary() -> None:
    markdown = render_report(check_live_metadata_decision_gate())

    assert "ESLM1 External Source Connector Live-Metadata Decision Gate" in markdown
    assert "live-metadata probe scaffold" in markdown
    assert "performs no live network request itself" in markdown
    assert "source body fetch" in markdown
    assert "external source connector live-metadata probe scaffold" in markdown
