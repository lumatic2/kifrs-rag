import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ifrs1109_scope_gate", ROOT / "scripts" / "ifrs1109_scope_gate.py"
)
ifrs1109_scope_gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ifrs1109_scope_gate)


def _report(*, scope_still_misses=False, rejected_changed=False):
    per_baseline = []
    per_target = []
    for item_id in ifrs1109_scope_gate.PRESERVED_ITEMS:
        per_baseline.append({"id": item_id, "miss": []})
        per_target.append({"id": item_id, "miss": []})
    for item_id in ifrs1109_scope_gate.RECOVERED_SCOPE_ITEMS:
        per_baseline.append({"id": item_id, "miss": [("1109", "2.1")]})
        per_target.append({"id": item_id, "miss": [("1109", "2.1")] if scope_still_misses else []})
    for item_id in ifrs1109_scope_gate.REJECTED_ITEMS:
        miss = [("R", item_id)]
        per_baseline.append({"id": item_id, "miss": miss})
        per_target.append({"id": item_id, "miss": [] if rejected_changed else miss})
    return {
        "k": 20,
        "retrievers": {
            "ifrs1115_subquery_hybrid": {
                "aggregate": {"recall@20": 0.8},
                "per_item": per_baseline,
            },
            "ifrs1109_scope_hybrid": {
                "aggregate": {"recall@20": 0.9},
                "per_item": per_target,
            },
        },
    }


def test_evaluate_gate_passes_when_scope_recovers_and_boundaries_hold():
    payload = ifrs1109_scope_gate.evaluate_gate(_report())

    assert payload["ok"] is True
    assert payload["failures"] == []


def test_evaluate_gate_fails_when_scope_item_still_misses():
    payload = ifrs1109_scope_gate.evaluate_gate(_report(scope_still_misses=True))

    assert payload["ok"] is False
    assert any("1109 scope subquery did not recover" in failure for failure in payload["failures"])


def test_evaluate_gate_fails_when_rejected_item_changes():
    payload = ifrs1109_scope_gate.evaluate_gate(_report(rejected_changed=True))

    assert payload["ok"] is False
    assert any("rejected item changed miss list" in failure for failure in payload["failures"])
