from __future__ import annotations

from scripts.default_retriever_guard import check_default_retriever_guard, load_cached_promotion_decision, render_markdown


def test_default_retriever_guard_keeps_runtime_default_hybrid() -> None:
    result = check_default_retriever_guard()

    assert result["ok"], result["errors"]
    assert result["default_mode"] == "hybrid"
    assert result["target_retriever"] == "ifrs1109_classification_hybrid"
    assert result["target_retriever_opt_in_available"] is True
    assert result["target_retriever_exposed_in_mcp"] is False
    assert result["promotion_decision"] == "defer"
    assert result["promote_to_default"] is False


def test_default_retriever_guard_report_states_boundary() -> None:
    rendered = render_markdown(check_default_retriever_guard())

    assert "Default Retriever Guard" in rendered
    assert "runtime default remains `hybrid`" in rendered
    assert "opt-in evaluation/demo path" in rendered
    assert "does not change runtime defaults" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered


def test_cached_promotion_decision_reports_missing_file(tmp_path) -> None:
    result = load_cached_promotion_decision(tmp_path / "missing.md")

    assert result["decision"] == "unknown"
    assert result["promote_to_default"] is False
    assert result["errors"]
