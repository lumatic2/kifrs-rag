from __future__ import annotations

from scripts.client_private_redaction_gate_check import check_client_private_redaction_gate


def test_client_private_redaction_gate_check_passes() -> None:
    result = check_client_private_redaction_gate()

    assert result["ok"], result["errors"]
    assert "source_locator" not in result["summary_keys"]
    assert "notes" not in result["summary_keys"]
    assert result["rejected_unreviewed"] is True
    assert result["report_exists"] is True
