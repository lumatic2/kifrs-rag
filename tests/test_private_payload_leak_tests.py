from __future__ import annotations

from pathlib import Path

from scripts.private_payload_leak_tests import (
    render_report,
    scan_public_parser_artifacts,
    scan_text_for_private_payloads,
)


def test_private_payload_leak_gate_passes_current_parser_reports() -> None:
    result = scan_public_parser_artifacts()

    assert result["ok"], result["leaks"]
    assert result["leak_count"] == 0
    assert result["missing_artifacts"] == []
    assert result["completed_milestone"] == "RLP4"
    assert result["next_leaf"] == "RLP5_local_parser_prototype_close_gate"


def test_private_payload_leak_detector_finds_identifier_like_values() -> None:
    leaks = scan_text_for_private_payloads("business number 123-45-67890", "memory")

    assert any(leak.leak_type == "identifier_like" for leak in leaks)


def test_private_payload_leak_detector_finds_body_and_ocr_markers() -> None:
    text = "PRIVATE_PAYLOAD: copied terms\nOCR PAYLOAD: scanned words"
    leaks = scan_text_for_private_payloads(text, "memory")

    leak_types = {leak.leak_type for leak in leaks}
    assert "body_payload_marker" in leak_types
    assert "ocr_payload_marker" in leak_types


def test_private_payload_leak_detector_finds_embedding_like_vectors() -> None:
    leaks = scan_text_for_private_payloads("embedding [0.123, -0.234, 0.345, 0.456]", "memory")

    assert any(leak.leak_type == "embedding_vector_like" for leak in leaks)


def test_private_payload_leak_gate_fails_temp_bad_artifact(tmp_path: Path) -> None:
    bad = tmp_path / "bad-report.md"
    bad.write_text("PRIVATE_PAYLOAD: copied private clause", encoding="utf-8")

    result = scan_public_parser_artifacts([bad])

    assert not result["ok"]
    assert result["leak_count"] == 1


def test_private_payload_leak_report_is_public_safe() -> None:
    rendered = render_report(scan_public_parser_artifacts())

    assert "RLP4 Private Payload Leak Tests" in rendered
    assert "leak-test gate" in rendered
    assert "private absolute file paths" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
