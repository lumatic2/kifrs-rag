from __future__ import annotations

from scripts.e2e_demo_packet_builder import build_demo_packet, render_markdown, render_packet_index


def test_e2e_demo_packet_builder_creates_ordered_navigation_surface() -> None:
    packet = build_demo_packet()

    assert packet["ok"] is True
    assert packet["horizon"] == "end-to-end-demo-scenario"
    assert packet["completed_milestone"] == "E2E3"
    assert packet["packet_path"] == "docs/reports/end-to-end-demo/INDEX.md"
    assert packet["next_leaf"] == "E2E4_demo_smoke_and_navigation_gate"
    assert [item["section"] for item in packet["items"]][:3] == ["start", "storyboard", "contract"]
    assert all(item["report_exists"] for item in packet["items"])
    assert all(item["recovery"] for item in packet["items"])


def test_e2e_demo_packet_index_is_public_safe_and_actionable() -> None:
    packet = build_demo_packet()
    index = render_packet_index(packet)
    report = render_markdown(packet)

    assert "End-to-End Demo Packet" in index
    assert "Demo Run Order" in index
    assert "python scripts\\e2e_demo_asset_inventory.py --format text --write" in index
    assert "not final accounting judgment" in index
    assert "release readiness" in index
    assert "E2E3 Demo Packet Builder" in report
    assert "api_key" not in index
    assert "token" not in index
    assert "kifrs.db" not in index
