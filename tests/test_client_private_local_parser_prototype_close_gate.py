from __future__ import annotations

from scripts.client_private_local_parser_prototype_close_gate import (
    render_close_report,
    run_local_parser_prototype_close_gate,
)


def test_local_parser_prototype_close_gate_passes_without_quality_preflight() -> None:
    result = run_local_parser_prototype_close_gate()

    assert result["ok"], result["errors"]
    assert result["checks"]["parser_readiness"]["ok"] is True
    assert result["checks"]["parser_prototype"]["ok"] is True
    assert result["checks"]["parser_prototype"]["route"]["route"] == "kifrs1116_review_pack"
    assert result["checks"]["parser_prototype"]["route"]["status"] == "candidate"
    assert "synthetic local parser prototype" in result["closed_scope"]


def test_local_parser_prototype_close_report_states_boundary() -> None:
    rendered = render_close_report(run_local_parser_prototype_close_gate())

    assert "LPC1 Local Parser Prototype Close Gate" in rendered
    assert "KIFRS1116 review-pack candidate" in rendered
    assert "real private document parser adapter" in rendered
    assert "Real private-file handling remains blocked" in rendered
