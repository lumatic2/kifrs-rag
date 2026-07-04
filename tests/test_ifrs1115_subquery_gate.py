import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ifrs1115_subquery_gate", ROOT / "scripts" / "ifrs1115_subquery_gate.py"
)
ifrs1115_subquery_gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ifrs1115_subquery_gate)


def _report(*, recovered_target_miss=False, rejected_changed=False):
    per_baseline = []
    per_target = []
    for item_id in ifrs1115_subquery_gate.ACCEPTED_SOURCE_ROUTE_ITEMS:
        per_baseline.append({"id": item_id, "miss": []})
        per_target.append({"id": item_id, "miss": []})
    for item_id in ifrs1115_subquery_gate.RECOVERED_1115_ITEMS:
        per_baseline.append({"id": item_id, "miss": [("1115", item_id)]})
        per_target.append({"id": item_id, "miss": [("1115", item_id)] if recovered_target_miss else []})
    for item_id in ifrs1115_subquery_gate.SEEDED_ITEMS:
        per_baseline.append({"id": item_id, "miss": []})
        per_target.append({"id": item_id, "miss": []})
    for item_id in ifrs1115_subquery_gate.REJECTED_ITEMS:
        miss = [("R", item_id)]
        per_baseline.append({"id": item_id, "miss": miss})
        per_target.append({"id": item_id, "miss": [] if rejected_changed else miss})
    return {
        "k": 20,
        "retrievers": {
            "source_routed_hybrid": {
                "aggregate": {"recall@20": 0.8},
                "per_item": per_baseline,
            },
            "ifrs1115_subquery_hybrid": {
                "aggregate": {"recall@20": 0.9},
                "per_item": per_target,
            },
        },
    }


def test_evaluate_gate_passes_when_1115_items_recover_and_boundaries_hold():
    payload = ifrs1115_subquery_gate.evaluate_gate(_report())

    assert payload["ok"] is True
    assert payload["failures"] == []


def test_evaluate_gate_fails_when_1115_item_still_misses():
    payload = ifrs1115_subquery_gate.evaluate_gate(_report(recovered_target_miss=True))

    assert payload["ok"] is False
    assert any("1115 subquery did not recover" in failure for failure in payload["failures"])


def test_evaluate_gate_fails_when_rejected_item_changes():
    payload = ifrs1115_subquery_gate.evaluate_gate(_report(rejected_changed=True))

    assert payload["ok"] is False
    assert any("rejected item changed miss list" in failure for failure in payload["failures"])
