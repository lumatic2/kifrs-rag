from __future__ import annotations

from scripts.product_weakness_horizon_candidates import build_candidates, render_markdown


def test_product_weakness_candidates_are_ordered_and_actionable() -> None:
    result = build_candidates()

    assert result["active_horizon"] == "operator-experience-hardening"
    candidates = result["candidates"]
    assert [candidate["order"] for candidate in candidates] == [1, 2, 3, 4, 5]
    assert [candidate["horizon_id"] for candidate in candidates] == [
        "real-local-parser-prototype",
        "source-body-ingestion-controlled-lane",
        "workflow-coverage-expansion",
        "runtime-retriever-promotion-gate",
        "operator-experience-hardening",
    ]
    assert candidates[0]["status"] == "closed"
    assert candidates[1]["status"] == "closed"
    assert candidates[2]["status"] == "closed"
    assert candidates[3]["status"] == "closed"
    assert candidates[4]["status"] == "active"
    assert all(candidate["plan"].startswith("docs/plans/") for candidate in candidates)
    assert all(candidate["first_milestone"] for candidate in candidates)


def test_product_weakness_candidates_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_candidates())

    assert "Product Weakness Horizon Candidates" in rendered
    assert "Recommended Queue" in rendered
    assert "real-local-parser-prototype" in rendered
    assert "runtime-retriever-promotion-gate" in rendered
    assert "real-accountant-session" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
