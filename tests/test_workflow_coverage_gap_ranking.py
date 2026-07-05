from __future__ import annotations

from scripts.workflow_coverage_gap_ranking import build_workflow_coverage_gap_ranking, render_markdown


def test_workflow_coverage_gap_ranking_selects_actionable_candidate() -> None:
    result = build_workflow_coverage_gap_ranking()

    assert result["ok"]
    assert result["horizon"] == "workflow-coverage-expansion"
    assert result["completed_milestone"] == "WCE1"
    assert result["recommended_candidate"] == "1037_provisions"
    candidates = result["ranked_candidates"]
    assert [candidate["rank"] for candidate in candidates] == [1, 2, 3, 4, 5]
    assert {candidate["candidate_id"] for candidate in candidates} >= {
        "1113_fair_value",
        "1036_impairment",
        "1037_provisions",
        "1110_consolidation",
        "disclosure_closing_support",
    }
    assert candidates[0]["total_score"] >= candidates[1]["total_score"]
    assert all(candidate["service_line"] for candidate in candidates)
    assert all(candidate["output"] for candidate in candidates)
    assert all(candidate["limits"] for candidate in candidates)


def test_workflow_coverage_gap_ranking_report_is_public_safe() -> None:
    rendered = render_markdown(build_workflow_coverage_gap_ranking())

    assert "WCE1 Coverage Gap Ranking" in rendered
    assert "1037_provisions" in rendered
    assert "external accountant outreach" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
