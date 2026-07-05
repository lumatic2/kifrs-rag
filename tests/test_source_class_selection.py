from __future__ import annotations

from scripts.source_class_selection import build_source_class_selection, render_markdown


def test_source_class_selection_picks_interpretive_body_lane() -> None:
    selection = build_source_class_selection()

    assert selection["ok"] is True
    assert selection["selected_source_class"] == "interpretive_accounting_material"
    assert selection["selected_source_ids"] == ["kasb-interpretation-material", "fss-accounting-inquiry"]
    assert selection["authorization_status"] == "not_authorized_for_body"
    assert selection["implementation_mode"] == "synthetic_body_only"
    assert selection["completed_milestone"] == "SBI1"
    assert selection["next_leaf"] == "SBI2_source_policy_record"


def test_source_class_selection_defines_allowed_and_forbidden_fields() -> None:
    selection = build_source_class_selection()

    assert "synthetic_body" in selection["allowed_fields"]
    assert "citation_role" in selection["allowed_fields"]
    assert "copied external document text" in selection["forbidden_fields"]
    assert "embedding dump" in selection["forbidden_fields"]
    assert "API secret" in selection["forbidden_fields"]


def test_source_class_selection_compares_multiple_candidates() -> None:
    selection = build_source_class_selection()
    candidate_classes = {candidate["source_class"] for candidate in selection["candidates"]}

    assert {
        "interpretive_accounting_material",
        "law_regulation",
        "filing_data",
        "client_private",
    }.issubset(candidate_classes)
    assert selection["missing_source_ids"] == []


def test_source_class_selection_report_is_public_safe() -> None:
    rendered = render_markdown(build_source_class_selection())

    assert "SBI1 Source Class Selection" in rendered
    assert "synthetic-body-only" in rendered
    assert "K-IFRS paragraph evidence remains primary" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
