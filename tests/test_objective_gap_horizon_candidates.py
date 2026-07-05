from __future__ import annotations

from scripts.objective_gap_horizon_candidates import build_candidates, render_markdown


def test_objective_gap_horizons_are_ordered_and_exclude_parked_work() -> None:
    result = build_candidates()

    assert result["active_horizon"] == "private-parser-realism-hardening"
    assert [candidate["order"] for candidate in result["candidates"]] == [1, 2, 3, 4, 5]
    assert [candidate["horizon_id"] for candidate in result["candidates"]] == [
        "rag-quality-fresh-validation",
        "private-parser-realism-hardening",
        "external-source-body-connector-expansion",
        "workflow-coverage-depth-expansion",
        "demo-rehearsal-quality-loop",
    ]
    assert result["candidates"][0]["status"] == "closed"
    assert result["candidates"][1]["status"] == "active"
    assert all(candidate["evidence_target"].startswith("docs/reports/") for candidate in result["candidates"])
    excluded = " ".join(result["excluded_from_plan"])
    assert "external accountant feedback" in excluded
    assert "packaging" in excluded


def test_objective_gap_horizon_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_candidates())

    assert "Objective Gap Horizon Candidates" in rendered
    assert "Recommended Horizon Queue" in rendered
    assert "rag-quality-fresh-validation" in rendered
    assert "private-parser-realism-hardening" in rendered
    assert "demo-rehearsal-quality-loop" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
