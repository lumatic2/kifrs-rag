from __future__ import annotations

from scripts.external_source_connector_post_close_demo_packet_note import (
    NOTE_PATH,
    check_post_close_demo_packet_note,
    render_note,
    render_report,
)


def test_post_close_demo_packet_note_links_reviewer_entrypoints() -> None:
    result = check_post_close_demo_packet_note()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["boundary"]["metadata_only"] is True
    assert result["boundary"]["supporting_interpretation_only"] is True
    assert result["boundary"]["external_text_pipeline_enabled"] is False
    assert all(link["linked"] for link in result["entrypoint_links"].values())


def test_post_close_demo_packet_note_names_boundary_plainly() -> None:
    result = check_post_close_demo_packet_note()
    markdown = NOTE_PATH.read_text(encoding="utf-8")

    assert "metadata-only" in markdown
    assert "supporting interpretation" in markdown
    assert "K-IFRS paragraph DB remains the primary accounting evidence source" in markdown
    assert "does not fetch/cache/chunk/embed/index/answer from external source body text" in markdown
    assert "2026-07-05-eslsc1-external-source-connector-lane-close-gate.md" in markdown
    assert "2026-07-05-esls1-external-source-connector-lane-summary.md" in markdown

    rendered_note = render_note(result)
    assert "source-body RAG" in rendered_note
    assert "Machine Result" in rendered_note


def test_post_close_demo_packet_note_gate_report_is_public_safe() -> None:
    markdown = render_report(check_post_close_demo_packet_note())

    assert "ESPDN1 External Source Connector Post-Close Demo Packet Note Gate" in markdown
    assert "source_body" not in markdown
    assert "api_key" not in markdown
    assert "token" not in markdown
