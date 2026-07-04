import importlib.util
import sys
from pathlib import Path

from kifrs.eval.models import Citation, GoldItem


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "source_routing_candidate_eval", ROOT / "scripts" / "source_routing_candidate_eval.py"
)
source_routing_candidate_eval = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = source_routing_candidate_eval
SPEC.loader.exec_module(source_routing_candidate_eval)


def _item():
    return GoldItem(
        id="QX",
        source="test",
        source_ref="test",
        question="classification question",
        must_cite=[Citation("1001", "69"), Citation("1001", "72")],
    )


def test_evaluate_candidates_accepts_fused_route_when_target_recovers_and_existing_hit_remains():
    candidate = source_routing_candidate_eval.SourceRouteCandidate(
        "QX", "1001-69", "1001", "test route"
    )

    def search_fn(query, standard, limit):
        if standard == "1001":
            return [
                {"standard": "1001", "no": "69"},
                {"standard": "1001", "no": "72"},
            ]
        return [
            {"standard": "1001", "no": "72"},
            {"standard": "9999", "no": "1"},
        ]

    report = source_routing_candidate_eval.evaluate_candidates(
        [_item()],
        (candidate,),
        search_fn=search_fn,
        limit=20,
        gate_k=20,
    )

    row = report["rows"][0]
    assert row["candidate"] is True
    assert row["target_improved"] is True
    assert row["preserves_existing_hits"] is True


def test_preserves_existing_hits_rejects_lost_required_hit():
    assert (
        source_routing_candidate_eval._preserves_existing_hits(
            {"1001-69": None, "1001-72": 2},
            {"1001-69": 3, "1001-72": None},
            gate_k=20,
        )
        is False
    )


def test_render_markdown_shows_decision_table():
    text = source_routing_candidate_eval.render_markdown(
        {
            "limit": 20,
            "gate_k": 20,
            "rows": [
                {
                    "item_id": "QX",
                    "route_standard": "1001",
                    "target_citation": "1001-69",
                    "target_rank_before": None,
                    "target_rank_routed": 1,
                    "target_rank_fused": 3,
                    "candidate": True,
                    "base_ranks": {"1001-69": None},
                    "routed_ranks": {"1001-69": 1},
                    "fused_ranks": {"1001-69": 3},
                    "target_improved": True,
                    "preserves_existing_hits": True,
                    "rationale": "test",
                }
            ],
        }
    )

    assert "# Source Routing Candidate Evaluation" in text
    assert "| QX | `1001` | `1001-69` | absent | 1 | 3 | candidate |" in text
