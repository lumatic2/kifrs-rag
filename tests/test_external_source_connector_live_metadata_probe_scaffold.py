from __future__ import annotations

from scripts.external_source_connector_live_metadata_decision_gate import ALLOWED_LIVE_METADATA_FIELDS
from scripts.external_source_connector_live_metadata_probe_scaffold import (
    _find_forbidden_fields,
    _find_extra_fields,
    render_report,
    run_live_metadata_probe_scaffold,
)


def test_live_metadata_probe_scaffold_defaults_to_no_network() -> None:
    result = run_live_metadata_probe_scaffold(checked_at="2026-07-05T12:30:00+09:00")

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["allow_network"] is False
    assert result["record_count"] == 2
    assert result["body_text_stored"] is False
    assert result["body_cache_created"] is False
    assert result["chunks_created"] is False
    assert result["embeddings_created"] is False
    assert result["index_created"] is False
    assert result["answer_time_body_use_enabled"] is False
    assert all(record["network_checked"] is False for record in result["probe_records"])
    assert all(record["checked_at"] == "2026-07-05T12:30:00+09:00" for record in result["probe_records"])
    assert all(set(record) == set(ALLOWED_LIVE_METADATA_FIELDS) for record in result["probe_records"])


def test_live_metadata_probe_scaffold_uses_injected_fetcher_without_storing_body() -> None:
    called: list[str] = []

    def fake_fetcher(url: str, timeout: float) -> dict[str, object]:
        called.append(url)
        return {
            "ok": True,
            "status_code": 200,
            "final_url": f"{url.rstrip('/')}/final",
            "content_type": "text/html; charset=utf-8",
            "error": "",
        }

    result = run_live_metadata_probe_scaffold(
        allow_network=True,
        checked_at="2026-07-05T12:31:00+09:00",
        fetcher=fake_fetcher,
    )

    assert result["ok"], result["errors"]
    assert len(called) == 2
    assert all(record["network_checked"] is True for record in result["probe_records"])
    assert all(record["status_code"] == 200 for record in result["probe_records"])
    assert all(record["body_text_stored"] is False for record in result["probe_records"])
    assert not _find_forbidden_fields(result["probe_records"])


def test_live_metadata_probe_scaffold_reports_failed_probe() -> None:
    def fake_fetcher(url: str, timeout: float) -> dict[str, object]:
        return {
            "ok": False,
            "status_code": 503,
            "final_url": url,
            "content_type": "",
            "error": "service_unavailable",
        }

    result = run_live_metadata_probe_scaffold(allow_network=True, fetcher=fake_fetcher)

    assert not result["ok"]
    assert any("live metadata probe failed" in error for error in result["errors"])
    assert all(record["body_text_stored"] is False for record in result["probe_records"])


def test_live_metadata_probe_scaffold_field_guards_detect_regressions() -> None:
    result = run_live_metadata_probe_scaffold()
    records = result["probe_records"]
    records[0]["body"] = "copied body"
    records[1]["unexpected"] = "not allowed"

    assert "$[0].body" in _find_forbidden_fields(records)
    assert _find_extra_fields(records) == ["body", "unexpected"]


def test_live_metadata_probe_report_names_next_leaf_and_boundary() -> None:
    markdown = render_report(run_live_metadata_probe_scaffold())

    assert "ESLP1 External Source Connector Live-Metadata Probe Scaffold" in markdown
    assert "live-metadata probe scaffold" in markdown
    assert "body text stored: False" in markdown
    assert "external source connector live-metadata close gate" in markdown
