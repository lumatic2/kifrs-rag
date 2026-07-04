import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "source_routed_hybrid_gate", ROOT / "scripts" / "source_routed_hybrid_gate.py"
)
source_routed_hybrid_gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(source_routed_hybrid_gate)


def _report(*, accepted_routed_miss=None, rejected_changed=False):
    accepted_routed_miss = accepted_routed_miss or {}
    per_baseline = []
    per_routed = []
    for item_id in source_routed_hybrid_gate.ACCEPTED_ITEMS:
        per_baseline.append({"id": item_id, "miss": [("T", item_id)]})
        per_routed.append({"id": item_id, "miss": accepted_routed_miss.get(item_id, [])})
    for item_id in source_routed_hybrid_gate.REJECTED_ITEMS:
        miss = [("R", item_id)]
        per_baseline.append({"id": item_id, "miss": miss})
        per_routed.append({"id": item_id, "miss": [] if rejected_changed else miss})
    return {
        "k": 20,
        "retrievers": {
            "hybrid": {
                "aggregate": {"recall@20": 0.5},
                "per_item": per_baseline,
            },
            "source_routed_hybrid": {
                "aggregate": {"recall@20": 0.9},
                "per_item": per_routed,
            },
        },
    }


def test_evaluate_gate_passes_when_accepted_recover_and_rejected_unchanged():
    payload = source_routed_hybrid_gate.evaluate_gate(_report())

    assert payload["ok"] is True
    assert payload["failures"] == []


def test_evaluate_gate_fails_when_accepted_item_still_misses():
    payload = source_routed_hybrid_gate.evaluate_gate(
        _report(accepted_routed_miss={"Q004": [("1001", "69")]})
    )

    assert payload["ok"] is False
    assert "Q004 accepted route still misses [('1001', '69')]" in payload["failures"]


def test_evaluate_gate_fails_when_rejected_item_changes_miss_list():
    payload = source_routed_hybrid_gate.evaluate_gate(_report(rejected_changed=True))

    assert payload["ok"] is False
    assert any("rejected route changed miss list" in failure for failure in payload["failures"])
