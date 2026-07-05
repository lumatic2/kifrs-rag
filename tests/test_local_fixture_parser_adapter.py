from __future__ import annotations

from kifrs.feedback import (
    LocalFixtureParserAdapterInput,
    render_local_fixture_parser_adapter_result,
    run_local_fixture_parser_adapter,
    validate_local_fixture_parser_adapter_input,
)
from scripts.client_private_local_parser_adapter_contract_check import default_adapter_contract
from scripts.client_private_upload_storage_policy_check import default_policy
from scripts.local_fixture_parser_adapter import (
    check_local_fixture_parser_adapter,
    default_fixture_adapter_input,
    render_report,
)


def test_local_fixture_parser_adapter_emits_structured_facts_and_questions() -> None:
    result = check_local_fixture_parser_adapter()

    assert result["ok"], result["errors"]
    assert result["route"]["route"] == "kifrs1116_review_pack"
    assert result["route"]["status"] == "candidate"
    assert result["structured_fact_keys"] == ["lease_term", "party", "payment_schedule"]
    assert "ignored_note" not in result["adapter_result"]["structured_facts"]
    assert len(result["review_questions"]) >= 5
    assert any("original local document" in question for question in result["review_questions"])


def test_local_fixture_parser_adapter_rejects_raw_fixture_text() -> None:
    adapter_input = LocalFixtureParserAdapterInput(
        **{
            **default_fixture_adapter_input().to_dict(),
            "raw_fixture_text_present": True,
        }
    )

    issues = validate_local_fixture_parser_adapter_input(
        adapter_input,
        default_adapter_contract(),
        default_policy(),
    )

    assert any(issue.path == "raw_fixture_text_present" for issue in issues)


def test_local_fixture_parser_adapter_requires_fixture_stub() -> None:
    adapter_input = LocalFixtureParserAdapterInput(
        **{
            **default_fixture_adapter_input().to_dict(),
            "source_stub": "local-private://dry-run/not-a-fixture",
        }
    )

    result = run_local_fixture_parser_adapter(
        adapter_input,
        default_adapter_contract(),
        default_policy(),
    )

    assert not result.ok
    assert any("source_stub" in error for error in result.errors)


def test_local_fixture_parser_adapter_renderer_states_boundary() -> None:
    result = run_local_fixture_parser_adapter(
        default_fixture_adapter_input(),
        default_adapter_contract(),
        default_policy(),
    )
    rendered = render_local_fixture_parser_adapter_result(result)

    assert "fixture-shaped structured facts only" in rendered
    assert "does not copy raw text" in rendered
    assert "Review Questions" in rendered


def test_local_fixture_parser_adapter_report_is_public_safe() -> None:
    rendered = render_report(check_local_fixture_parser_adapter())

    assert "RLP2 Local Fixture Parser Adapter" in rendered
    assert "structured facts plus human review questions" in rendered
    assert "real private-file parser" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
