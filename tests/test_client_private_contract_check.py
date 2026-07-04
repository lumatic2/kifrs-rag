from __future__ import annotations

from scripts.client_private_contract_check import check_client_private_contract


def test_client_private_contract_check_passes() -> None:
    result = check_client_private_contract()

    assert result["ok"], result["errors"]
    assert result["good_issue_count"] == 0
    assert "structured_facts.raw_contract" in result["bad_issue_paths"]
    assert result["report_exists"] is True
