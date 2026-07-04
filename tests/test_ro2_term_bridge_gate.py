import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ro2_term_bridge_gate", ROOT / "scripts" / "ro2_term_bridge_gate.py"
)
ro2_term_bridge_gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ro2_term_bridge_gate)


def _report(*, recall20=1.0, misses=None):
    misses = misses or {"Q039": [], "Q048": []}
    return {
        "k": 20,
        "retrievers": {
            "hybrid": {
                "aggregate": {
                    "recall@1": 0.0,
                    "recall@3": 0.0,
                    "recall@5": 0.25,
                    "recall@10": 0.25,
                    "recall@20": recall20,
                    "mrr": 0.161,
                    "ndcg@10": 0.132,
                },
                "per_item": [
                    {
                        "id": "Q039",
                        "hit": [("1037", "14"), ("1116", "24")],
                        "miss": misses["Q039"],
                        "gold_ranks": {"1037-14": 16, "1116-24": 2},
                    },
                    {
                        "id": "Q048",
                        "hit": [("1036", "18"), ("1036", "59")],
                        "miss": misses["Q048"],
                        "gold_ranks": {"1036-18": 17, "1036-59": 4},
                    },
                ],
            }
        },
    }


def test_evaluate_gate_passes_when_focused_recall_is_repaired():
    payload = ro2_term_bridge_gate.evaluate_gate(_report())

    assert payload["ok"] is True
    assert payload["recall_at_k"] == 1.0
    assert payload["failures"] == []


def test_evaluate_gate_fails_when_recall20_regresses():
    payload = ro2_term_bridge_gate.evaluate_gate(_report(recall20=0.5))

    assert payload["ok"] is False
    assert "recall@20 0.500 < 1.000" in payload["failures"]


def test_evaluate_gate_fails_when_any_item_still_misses_required_citation():
    payload = ro2_term_bridge_gate.evaluate_gate(
        _report(misses={"Q039": [("1037", "14")], "Q048": []})
    )

    assert payload["ok"] is False
    assert "Q039 still misses [('1037', '14')]" in payload["failures"]


def test_render_text_includes_seed_remediation_on_failure():
    payload = ro2_term_bridge_gate.evaluate_gate(_report(recall20=0.5))
    text = ro2_term_bridge_gate.render_text(payload)

    assert "ok: False" in text
    assert "python scripts\\seed_user_notes.py --apply" in text
