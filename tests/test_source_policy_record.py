from __future__ import annotations

from scripts.source_policy_record import (
    SourcePolicyRecord,
    build_source_policy_record,
    default_source_policy_record,
    render_markdown,
    validate_source_policy_record,
)


def test_source_policy_record_validates_selected_lane() -> None:
    result = build_source_policy_record()

    assert result["ok"], result["errors"]
    assert result["completed_milestone"] == "SBI2"
    assert result["next_leaf"] == "SBI3_synthetic_parser_chunker"
    policy = result["policy"]
    assert policy["source_class"] == "interpretive_accounting_material"
    assert policy["storage_mode"] == "synthetic_body_only"
    assert policy["citation_role"] == "supporting_interpretation"
    assert policy["authority_level"] == "interpretive"


def test_source_policy_record_rejects_primary_override() -> None:
    policy = SourcePolicyRecord(
        **{
            **default_source_policy_record().to_dict(),
            "primary_evidence_override_allowed": True,
        }
    )

    errors = validate_source_policy_record(policy)

    assert any("primary_evidence_override_allowed" in error for error in errors)


def test_source_policy_record_rejects_live_fetch_and_embedding() -> None:
    policy = SourcePolicyRecord(
        **{
            **default_source_policy_record().to_dict(),
            "live_fetch_allowed": True,
            "embedding_allowed": True,
        }
    )

    errors = validate_source_policy_record(policy)

    assert any("live_fetch_allowed" in error for error in errors)
    assert any("embedding_allowed" in error for error in errors)


def test_source_policy_record_requires_forbidden_fields() -> None:
    policy = SourcePolicyRecord(
        **{
            **default_source_policy_record().to_dict(),
            "forbidden_fields": [],
        }
    )

    errors = validate_source_policy_record(policy)

    assert any("copied external document text" in error for error in errors)
    assert any("embedding dump" in error for error in errors)


def test_source_policy_record_report_is_public_safe() -> None:
    rendered = render_markdown(build_source_policy_record())

    assert "SBI2 Source Body Policy Record" in rendered
    assert "synthetic-body-only" in rendered
    assert "supporting-interpretation evidence" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
