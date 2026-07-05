from __future__ import annotations

from scripts.rag_reliability_repair_policy_candidate import build_policy_candidate, render_markdown


def test_rr4_repair_policy_keeps_runtime_default_unchanged() -> None:
    policy = build_policy_candidate()

    assert policy["ok"], policy["errors"]
    assert policy["milestone"] == "RR4"
    assert policy["guard_snapshot"]["default_mode"] == "hybrid"
    assert policy["guard_snapshot"]["target_retriever_exposed_in_mcp"] is False
    assert policy["guard_snapshot"]["promote_to_default"] is False
    accepted_ids = {item["id"] for item in policy["accepted_policies"]}
    deferred_ids = {item["id"] for item in policy["deferred_policies"]}
    assert "keep_target_opt_in_eval_path" in accepted_ids
    assert "default_promotion" in deferred_ids
    assert "mcp_mode_exposure" in deferred_ids


def test_rr4_repair_policy_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_policy_candidate())

    assert "RR4 Repair Policy Candidate" in rendered
    assert "Accepted Policies" in rendered
    assert "Deferred Policies" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
