from __future__ import annotations

from scripts.opt_in_retriever_demo_validation import build_demo_validation, render_report


def test_opt_in_retriever_demo_validation_passes() -> None:
    payload = build_demo_validation()

    assert payload["ok"], payload["errors"]
    assert payload["target_retriever"] == "ifrs1109_classification_hybrid"
    assert payload["target_recall20"] == 1.0
    assert payload["target_buckets"]["absent"] == 0
    assert payload["default_promotion"] == "deferred"


def test_opt_in_retriever_demo_report_states_boundary() -> None:
    rendered = render_report(build_demo_validation())

    assert "ready for opt-in demo use" in rendered
    assert "Default retriever promotion remains deferred" in rendered
    assert "Keep the default retriever unchanged" in rendered
