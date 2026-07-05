from __future__ import annotations

from scripts.client_private_local_parser_close_gate import (
    render_close_report,
    run_local_parser_close_gate,
)


def test_local_parser_close_gate_passes_without_quality_preflight() -> None:
    result = run_local_parser_close_gate()

    assert result["ok"], result["errors"]
    assert result["checks"]["local_only_close_gate"]["ok"] is True
    assert result["checks"]["upload_storage_policy"]["ok"] is True
    assert result["checks"]["parser_dry_run_fixture"]["ok"] is True
    assert result["checks"]["deletion_attestation"]["ok"] is True
    assert "synthetic parser dry-run output contract" in result["closed_scope"]


def test_local_parser_close_gate_report_states_boundary() -> None:
    rendered = render_close_report(run_local_parser_close_gate())

    assert "CPL1 Client-Private Local Parser Close Gate" in rendered
    assert "contract level" in rendered
    assert "real private document parser" in rendered
    assert "real file deletion automation" in rendered
    assert "source bodies or identifiers" in rendered
