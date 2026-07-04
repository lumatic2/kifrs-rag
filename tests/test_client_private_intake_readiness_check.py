from __future__ import annotations

from scripts.client_private_intake_readiness_check import check_client_private_intake_readiness


def test_client_private_intake_readiness_report_is_complete() -> None:
    result = check_client_private_intake_readiness()

    assert result["ok"], result["errors"]
    assert result["missing_artifacts"] == []
    assert result["missing_report_terms"] == []
    assert result["missing_next_steps"] == []


def test_client_private_intake_readiness_detects_missing_required_terms(tmp_path) -> None:
    report = tmp_path / "readiness.md"
    report.write_text(
        """
# Client Private Intake Readiness

client_private
local_private_case_facts
no_store_handoff
redaction_status
allowed_output_level
raw_contract
customer identifier
reviewer checks original documents outside this repo
do not implement upload
CP1 CP2 CP3 CP4
""",
        encoding="utf-8",
    )

    result = check_client_private_intake_readiness(report)

    assert not result["ok"]
    assert result["missing_report_terms"] == [
        "LocalPrivateCaseIntake",
        "Status: complete",
        "do not parse private source body",
    ]
