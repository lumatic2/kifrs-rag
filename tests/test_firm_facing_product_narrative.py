from __future__ import annotations

from scripts.firm_facing_product_narrative import build_narrative_check, render_markdown


def test_product_narrative_readme_surface_is_present() -> None:
    check = build_narrative_check()

    assert check["ok"] is True
    assert check["milestone"] == "FPS4"
    assert check["missing_phrases"] == []
    assert check["forbidden_hits"] == []


def test_product_narrative_report_explains_capability_and_limits() -> None:
    rendered = render_markdown(build_narrative_check())

    assert "firm-facing demo command" in rendered
    assert "decision-support only" in rendered
    assert "private client payloads are not published" in rendered
