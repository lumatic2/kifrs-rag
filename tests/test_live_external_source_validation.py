from __future__ import annotations

from scripts.live_external_source_validation import (
    collect_live_probe_targets,
    render_report,
    validate_live_external_sources,
)


def test_collect_live_probe_targets_includes_public_external_surfaces() -> None:
    targets = collect_live_probe_targets()
    item_ids = {target.item_id for target in targets}

    assert "kasb-implementation-material-index" in item_ids
    assert "fss-accounting-inquiry-index" in item_ids
    assert "opendart-structured-financials-seed" in item_ids


def test_validate_live_external_sources_uses_fetcher_without_storing_body() -> None:
    called: list[str] = []

    def fake_fetcher(url: str, timeout: float) -> dict[str, object]:
        called.append(url)
        return {
            "ok": True,
            "status_code": 200,
            "final_url": url,
            "content_type": "text/html",
            "error": "",
        }

    result = validate_live_external_sources(allow_network=True, fetcher=fake_fetcher)

    assert result["ok"], result["errors"]
    assert result["network_checked"] is True
    assert result["body_text_stored"] is False
    assert len(called) == result["target_count"]
    assert all(check["body_text_stored"] is False for check in result["checks"])


def test_live_external_source_report_keeps_boundary_explicit() -> None:
    result = validate_live_external_sources()
    rendered = render_report(result)

    assert "stores no source body text" in rendered
    assert "does not promote external sources above K-IFRS primary evidence" in rendered
    assert "does not implement body ingestion" in rendered
