from __future__ import annotations

from scripts.external_source_body_ingestion_decision_gate import (
    check_body_ingestion_decision_gate,
    render_report,
)


def test_body_ingestion_decision_gate_defers_when_policy_plan_and_authorization_are_missing(tmp_path) -> None:
    result = check_body_ingestion_decision_gate(
        body_policy=tmp_path / "missing-body-policy.md",
        implementation_plan=tmp_path / "missing-implementation-plan.md",
    )
    decision = result["decision"]

    assert result["ok"], result["errors"]
    assert decision["decision"] == "defer"
    assert decision["allowed_to_implement"] is False
    assert decision["source_manifest_ok"] is True
    assert decision["evidence_manifest_ok"] is True
    assert decision["live_landing_validation_ok"] is True
    assert decision["live_landing_report_present"] is True
    blockers = " ".join(decision["blockers"])
    assert "copyright/robots/storage policy" in blockers
    assert "implementation plan" in blockers
    assert "explicit user authorization" in blockers
    assert "body-ingestion policy plan" in result["next_leaf"]


def test_body_ingestion_decision_gate_default_has_policy_and_plan_but_still_requires_authorization() -> None:
    result = check_body_ingestion_decision_gate()
    decision = result["decision"]

    assert result["ok"], result["errors"]
    assert decision["decision"] == "defer"
    assert decision["allowed_to_implement"] is False
    assert decision["body_policy_present"] is True
    assert decision["implementation_plan_present"] is True
    assert decision["blockers"] == [
        "explicit user authorization is required before live body ingestion/chunking/embedding"
    ]
    assert "authorization gate" in result["next_leaf"]


def test_body_ingestion_decision_gate_can_proceed_when_all_stop_conditions_clear(tmp_path) -> None:
    body_policy = tmp_path / "body-policy.md"
    implementation_plan = tmp_path / "implementation-plan.md"
    body_policy.write_text("policy: local-only body handling approved for test\n", encoding="utf-8")
    implementation_plan.write_text("plan: parse/chunk/embed implementation approved for test\n", encoding="utf-8")

    result = check_body_ingestion_decision_gate(
        explicit_authorization=True,
        body_policy=body_policy,
        implementation_plan=implementation_plan,
    )
    decision = result["decision"]

    assert result["ok"], result["errors"]
    assert decision["decision"] == "proceed"
    assert decision["allowed_to_implement"] is True
    assert decision["blockers"] == []
    assert result["next_leaf"] == "external source body ingestion implementation"


def test_body_ingestion_report_states_no_body_pipeline_is_implemented() -> None:
    rendered = render_report(check_body_ingestion_decision_gate())

    assert "External Source Body-Ingestion Decision Gate" in rendered
    assert "explicit user authorization" in rendered
    assert "live body fetching or crawling" in rendered
    assert "source-specific chunking" in rendered
    assert "external body embeddings" in rendered
    assert "answer-time promotion of external body text" in rendered
