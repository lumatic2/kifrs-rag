from __future__ import annotations

from kifrs.feedback import (
    LocalPrivateParserAdapterScaffoldRequest,
    render_local_private_parser_adapter_scaffold_run,
    run_local_private_parser_adapter_scaffold,
    validate_local_private_parser_adapter_scaffold_request,
)
from scripts.client_private_local_parser_adapter_contract_check import default_adapter_contract
from scripts.client_private_local_parser_adapter_scaffold import (
    check_local_parser_adapter_scaffold,
    default_scaffold_request,
    render_report,
)
from scripts.client_private_upload_storage_policy_check import default_policy


def test_local_parser_adapter_scaffold_routes_structured_facts() -> None:
    result = check_local_parser_adapter_scaffold()

    assert result["ok"], result["errors"]
    assert result["scaffold_run"]["real_adapter_implemented"] is False
    route = result["scaffold_run"]["prototype_result"]["route"]
    assert route["route"] == "kifrs1116_review_pack"
    assert route["status"] == "candidate"


def test_local_parser_adapter_scaffold_rejects_raw_file_path() -> None:
    request = LocalPrivateParserAdapterScaffoldRequest(
        **{
            **default_scaffold_request().to_dict(),
            "raw_file_path": "C:/private/client.pdf",
        }
    )

    issues = validate_local_private_parser_adapter_scaffold_request(
        request,
        default_adapter_contract(),
        default_policy(),
    )

    assert any(issue.path == "raw_file_path" for issue in issues)


def test_local_parser_adapter_scaffold_rejects_ocr_flag() -> None:
    request = LocalPrivateParserAdapterScaffoldRequest(
        **{
            **default_scaffold_request().to_dict(),
            "ocr_enabled": True,
        }
    )
    run = run_local_private_parser_adapter_scaffold(
        "test-scaffold",
        default_adapter_contract(),
        default_policy(),
        request,
    )

    assert not run.ok
    assert any("ocr_enabled" in error for error in run.errors)


def test_local_parser_adapter_scaffold_requires_operator_ack() -> None:
    request = LocalPrivateParserAdapterScaffoldRequest(
        **{
            **default_scaffold_request().to_dict(),
            "operator_ack": "",
        }
    )

    issues = validate_local_private_parser_adapter_scaffold_request(
        request,
        default_adapter_contract(),
        default_policy(),
    )

    assert any(issue.path == "operator_ack" for issue in issues)


def test_render_local_parser_adapter_scaffold_run_states_boundary() -> None:
    run = run_local_private_parser_adapter_scaffold(
        "test-scaffold",
        default_adapter_contract(),
        default_policy(),
        default_scaffold_request(),
    )
    rendered = render_local_private_parser_adapter_scaffold_run(run)

    assert "accepts structured facts only" in rendered
    assert "refuses raw file paths" in rendered
    assert "not a real private-file parser" in rendered


def test_local_parser_adapter_scaffold_report_distinguishes_not_implemented() -> None:
    rendered = render_report(check_local_parser_adapter_scaffold())

    assert "LPAS1 Local Parser Adapter Scaffold" in rendered
    assert "Still Not Implemented" in rendered
    assert "real private document parsing" in rendered
    assert "not a real private-file parser" in rendered
