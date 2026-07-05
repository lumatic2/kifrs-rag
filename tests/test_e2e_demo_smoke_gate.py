from __future__ import annotations

from scripts.e2e_demo_packet_builder import build_demo_packet
from scripts.e2e_demo_smoke_gate import build_demo_smoke_gate, render_markdown


def test_e2e_demo_smoke_gate_verifies_packet_navigation() -> None:
    smoke = build_demo_smoke_gate()

    assert smoke["ok"] is True
    assert smoke["horizon"] == "end-to-end-demo-scenario"
    assert smoke["completed_milestone"] == "E2E4"
    assert smoke["next_leaf"] == "E2E5_horizon_close_gate"
    assert smoke["checks"]["packet_index_exists"] is True
    assert smoke["checks"]["all_packet_reports_exist"] is True
    assert smoke["checks"]["packet_surface_public_safe"] is True
    assert smoke["missing_reports"] == []


def test_e2e_demo_smoke_gate_reports_missing_report_failure_path() -> None:
    packet = build_demo_packet()
    broken_items = [dict(item) for item in packet["items"]]
    broken_items[0]["report"] = "docs/reports/missing-demo-report.md"

    smoke = build_demo_smoke_gate(items=broken_items)

    assert smoke["ok"] is False
    assert "docs/reports/missing-demo-report.md" in smoke["missing_reports"]
    assert "Rerun the matching packet command" in smoke["failure_path"]
    assert "all_packet_reports_exist" in smoke["errors"]


def test_e2e_demo_smoke_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_demo_smoke_gate())

    assert "E2E4 Demo Smoke And Navigation Gate" in rendered
    assert "Missing Reports" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
