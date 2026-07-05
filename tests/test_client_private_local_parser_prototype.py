from __future__ import annotations

import pytest

from kifrs.feedback import (
    LocalPrivateParserPrototypeInput,
    render_local_private_parser_prototype_result,
    run_local_private_parser_prototype,
    validate_local_private_parser_prototype_input,
)
from scripts.client_private_local_parser_prototype_spike import (
    check_local_parser_prototype,
    default_parser_input,
    render_report,
)
from scripts.client_private_upload_storage_policy_check import default_policy


def test_local_parser_prototype_routes_to_review_pack_candidate() -> None:
    result = check_local_parser_prototype()

    assert result["ok"], result["errors"]
    assert result["route"]["route"] == "kifrs1116_review_pack"
    assert result["route"]["status"] == "candidate"
    assert "source_locator" not in result["prototype_result"]["redacted_summary"]
    assert result["prototype_result"]["deletion_attestation"]["deletion_status"] == "deleted"


def test_local_parser_prototype_rejects_raw_file_presence() -> None:
    parser_input = LocalPrivateParserPrototypeInput(
        **{
            **default_parser_input().to_dict(),
            "raw_file_present": True,
        }
    )

    issues = validate_local_private_parser_prototype_input(parser_input, default_policy())

    assert any(issue.path == "raw_file_present" for issue in issues)


def test_local_parser_prototype_rejects_protected_extracted_field() -> None:
    parser_input = LocalPrivateParserPrototypeInput(
        **{
            **default_parser_input().to_dict(),
            "extracted_fields": {"raw_contract": "copied private body"},
        }
    )

    issues = validate_local_private_parser_prototype_input(parser_input, default_policy())

    assert any(issue.path == "extracted_fields.raw_contract" for issue in issues)


def test_local_parser_prototype_raises_on_invalid_input() -> None:
    parser_input = LocalPrivateParserPrototypeInput(
        **{
            **default_parser_input().to_dict(),
            "ocr_text_present": True,
        }
    )

    with pytest.raises(ValueError, match="ocr_text_present"):
        run_local_private_parser_prototype(parser_input, default_policy())


def test_render_local_parser_prototype_result_states_boundary() -> None:
    prototype = run_local_private_parser_prototype(default_parser_input(), default_policy())
    rendered = render_local_private_parser_prototype_result(prototype)

    assert "does not read files" in rendered
    assert "run OCR" in rendered
    assert "review-pack route candidate" in rendered


def test_local_parser_prototype_report_distinguishes_not_implemented() -> None:
    rendered = render_report(check_local_parser_prototype())

    assert "LPP1 Local Parser Prototype Spike" in rendered
    assert "Still Not Implemented" in rendered
    assert "real private document parsing" in rendered
    assert "parser-shaped structured input" in rendered
