from __future__ import annotations

from scripts.real_accountant_readiness_index import build_readiness_index, render_markdown


def test_readiness_index_summarizes_internal_ready_and_external_open_items() -> None:
    index = build_readiness_index()

    assert index["ok"], index["errors"]
    assert index["session_mode"] == "ready_to_schedule"
    assert index["close_ready"] is False
    assert index["ready_item_count"] == index["total_item_count"]
    assert index["total_item_count"] >= 10
    assert "Send the reviewer invite" in index["external_open_items"][0]
    assert index["operator_start"].endswith("2026-07-05-operator-execution-brief.md")


def test_readiness_index_report_is_one_page_public_safe_status() -> None:
    report = render_markdown(build_readiness_index())

    assert "Real Accountant Session Readiness Index" in report
    assert "Internal readiness is complete" in report
    assert "External Open Items" in report
    assert "source_body" not in report
    assert "api_key" not in report
    assert "token" not in report
