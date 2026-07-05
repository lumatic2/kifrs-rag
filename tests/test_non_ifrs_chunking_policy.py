from __future__ import annotations

import json

from scripts.validate_non_ifrs_chunking_policy import DEFAULT_POLICY_PATH, render_markdown, validate_policy


def test_non_ifrs_chunking_policy_covers_all_record_types() -> None:
    result = validate_policy()

    assert result["ok"], result["errors"]
    assert result["total_lanes"] == 4
    assert set(result["lanes"]) == {
        "document_metadata",
        "law_locator",
        "structured_fact",
        "client_private_fact",
    }
    assert result["lanes"]["law_locator"]["vector_scope"] == "none_for_public_fixture"
    assert result["lanes"]["structured_fact"]["index_strategy"] == "structured_lookup"
    assert result["lanes"]["client_private_fact"]["runtime_lookup"] == "local_private_namespace"


def test_non_ifrs_chunking_policy_rejects_vector_scope_for_law_locator(tmp_path) -> None:
    payload = json.loads(DEFAULT_POLICY_PATH.read_text(encoding="utf-8"))
    payload["lanes"]["law_locator"]["vector_scope"] = "author_written_metadata_only"
    bad_path = tmp_path / "bad_policy.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    result = validate_policy(bad_path)

    assert not result["ok"]
    assert any("law_locator" in error and "none_for_public_fixture" in error for error in result["errors"])


def test_nis4_report_is_actionable() -> None:
    rendered = render_markdown(validate_policy())

    assert "NIS4 Chunking and Embedding Policy" in rendered
    assert "document_metadata" in rendered
    assert "structured_fact" in rendered
    assert "NIS5_dataization_gate_and_runtime_handoff" in rendered
