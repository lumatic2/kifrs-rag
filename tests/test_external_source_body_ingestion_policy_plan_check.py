from __future__ import annotations

from dataclasses import replace

from scripts.external_source_body_ingestion_policy_plan_check import (
    FORBIDDEN_PUBLIC_FIELDS,
    check_policy_plan,
    default_policy_plan,
    render_body_policy,
    render_implementation_plan,
    render_report,
    validate_policy_plan,
)


def test_default_external_source_body_policy_plan_passes() -> None:
    result = check_policy_plan()
    plan = result["policy_plan"]

    assert result["ok"], result["errors"]
    assert plan["body_fetching_allowed_by_this_plan"] is False
    assert plan["chunking_allowed_by_this_plan"] is False
    assert plan["embedding_allowed_by_this_plan"] is False
    assert plan["commit_allowed_by_this_plan"] is False
    assert set(FORBIDDEN_PUBLIC_FIELDS).issubset(set(plan["forbidden_public_fields"]))


def test_external_source_body_policy_plan_rejects_implementation_permission() -> None:
    bad_plan = replace(
        default_policy_plan(),
        body_fetching_allowed_by_this_plan=True,
        chunking_allowed_by_this_plan=True,
        embedding_allowed_by_this_plan=True,
        commit_allowed_by_this_plan=True,
    )

    errors = validate_policy_plan(bad_plan)

    assert any("body_fetching_allowed_by_this_plan" in error for error in errors)
    assert any("chunking_allowed_by_this_plan" in error for error in errors)
    assert any("embedding_allowed_by_this_plan" in error for error in errors)
    assert any("commit_allowed_by_this_plan" in error for error in errors)


def test_external_source_body_policy_plan_requires_source_review_and_authorization() -> None:
    bad_plan = replace(
        default_policy_plan(),
        required_source_checks=["record publisher and canonical locator"],
        required_operator_checks=["run metadata-only live validation"],
    )

    errors = validate_policy_plan(bad_plan)

    assert any("robots/terms/license" in error for error in errors)
    assert any("explicit authorization" in error for error in errors)


def test_external_source_body_policy_plan_reports_boundary() -> None:
    result = check_policy_plan()

    report = render_report(result)
    policy = render_body_policy(result)
    plan = render_implementation_plan(result)

    assert "does not fetch, cache, chunk, embed, or index" in report
    assert "does not authorize live body ingestion" in report
    assert "Body fetching allowed by this policy: False" in policy
    assert "The next implementation is not body ingestion itself" in plan
    assert "source-specific authorization gate" in plan
