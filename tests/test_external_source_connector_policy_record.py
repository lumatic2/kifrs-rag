from __future__ import annotations

from scripts.external_source_connector_policy_record import (
    FORBIDDEN_PUBLIC_FIELDS,
    build_connector_policy_record,
    check_connector_policy_record,
    render_report,
)


def test_connector_policy_record_is_metadata_only_for_kasb_fss() -> None:
    result = check_connector_policy_record()
    record = result["policy_record"]

    assert result["ok"], result["errors"]
    assert record["connector_id"] == "kasb-fss-interpretive-catalog"
    assert record["source_pack_item_ids"] == [
        "kasb-implementation-material-index",
        "fss-accounting-inquiry-index",
    ]
    assert record["source_class"] == "interpretive_accounting_material"
    assert record["citation_role"] == "supporting_interpretation_after_kifrs_primary_evidence"
    assert record["live_fetch_allowed"] is False
    assert record["body_cache_allowed"] is False
    assert record["live_chunking_allowed"] is False
    assert record["embedding_allowed"] is False
    assert record["answer_time_use_allowed"] is False
    assert result["source_pack_ok"] is True
    assert result["missing_source_pack_items"] == []


def test_connector_policy_record_keeps_forbidden_fields_out_of_allowed_public_fields() -> None:
    record = build_connector_policy_record()

    assert set(record.allowed_public_fields).isdisjoint(FORBIDDEN_PUBLIC_FIELDS)
    assert "locator" in record.allowed_public_fields
    assert "body" in record.forbidden_public_fields
    assert "embedding" in record.forbidden_public_fields


def test_connector_policy_report_names_next_leaf() -> None:
    markdown = render_report(check_connector_policy_record())

    assert "ESCP1 External Source Connector Policy Record" in markdown
    assert "kasb-fss-interpretive-catalog" in markdown
    assert "external source connector metadata dry-run gate" in markdown
    assert "live fetch allowed: False" in markdown
