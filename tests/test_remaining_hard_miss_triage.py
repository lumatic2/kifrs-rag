import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "remaining_hard_miss_triage", ROOT / "scripts" / "remaining_hard_miss_triage.py"
)
remaining_hard_miss_triage = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = remaining_hard_miss_triage
SPEC.loader.exec_module(remaining_hard_miss_triage)


def test_render_markdown_includes_public_safe_triage_rows():
    text = remaining_hard_miss_triage.render_markdown(
        {
            "retriever": "source_routed_hybrid",
            "k": 20,
            "candidate_limit": 50,
            "rows": [
                {
                    "item_id": "Q001",
                    "miss": [("1115", "27")],
                    "hit": [("1115", "22")],
                    "gold_ranks": {"1115-22": 20, "1115-27": None},
                    "candidate_id": "q001-distinct-performance-obligation",
                    "candidate_rank_after": 28,
                    "candidate_decision": "reject",
                    "classification": "near_miss_candidate_pool",
                    "finding": "test finding",
                    "next_action": "test next action",
                }
            ],
        }
    )

    assert "# Remaining Hard Miss Triage" in text
    assert "| Q001 | `1115-27` | `1115-22` | 28 | reject | `near_miss_candidate_pool` |" in text
    assert "test next action" in text


def test_build_report_raises_on_missing_item(monkeypatch):
    monkeypatch.setattr(remaining_hard_miss_triage, "_load_goldset", lambda goldset: [])

    try:
        remaining_hard_miss_triage.build_report(item_ids=("Q999",))
    except ValueError as exc:
        assert "goldset missing item ids: Q999" in str(exc)
    else:
        raise AssertionError("expected ValueError")
