from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from kifrs.eval.retrieval import _load_goldset, evaluate
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.eval.retrieval import _load_goldset, evaluate


DEFAULT_GOLDSET = Path("data/eval/goldset.json")
ACCEPTED_ITEMS = ("Q004", "Q013", "Q025", "Q026", "Q041")
SEEDED_ITEMS = ("Q029",)
REJECTED_ITEMS = ("Q001", "Q006", "Q008", "Q040")
ROUTED_RETRIEVER = "source_routed_hybrid"
BASELINE_RETRIEVER = "hybrid"
DEFAULT_K = 20


def build_report(*, goldset: Path = DEFAULT_GOLDSET, k: int = DEFAULT_K) -> dict[str, Any]:
    wanted = set(ACCEPTED_ITEMS + SEEDED_ITEMS + REJECTED_ITEMS)
    items = [item for item in _load_goldset(goldset) if item.id in wanted]
    missing = sorted(wanted - {item.id for item in items})
    if missing:
        raise ValueError(f"goldset missing item ids: {', '.join(missing)}")
    report = evaluate(items, [BASELINE_RETRIEVER, ROUTED_RETRIEVER], k)
    return evaluate_gate(report)


def evaluate_gate(report: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    baseline_items = _items_by_id(report, BASELINE_RETRIEVER)
    routed_items = _items_by_id(report, ROUTED_RETRIEVER)
    accepted: dict[str, dict[str, Any]] = {}
    seeded: dict[str, dict[str, Any]] = {}
    rejected: dict[str, dict[str, Any]] = {}

    for item_id in ACCEPTED_ITEMS:
        baseline_miss = baseline_items[item_id]["miss"]
        routed_miss = routed_items[item_id]["miss"]
        accepted[item_id] = {"baseline_miss": baseline_miss, "routed_miss": routed_miss}
        if routed_miss:
            failures.append(f"{item_id} accepted route still misses {routed_miss}")

    for item_id in SEEDED_ITEMS:
        baseline_miss = baseline_items[item_id]["miss"]
        routed_miss = routed_items[item_id]["miss"]
        seeded[item_id] = {"baseline_miss": baseline_miss, "routed_miss": routed_miss}
        if baseline_miss or routed_miss:
            failures.append(
                f"{item_id} reviewed seed should recover both retrievers: "
                f"baseline={baseline_miss}, routed={routed_miss}"
            )

    for item_id in REJECTED_ITEMS:
        baseline_miss = baseline_items[item_id]["miss"]
        routed_miss = routed_items[item_id]["miss"]
        rejected[item_id] = {"baseline_miss": baseline_miss, "routed_miss": routed_miss}
        if routed_miss != baseline_miss:
            failures.append(
                f"{item_id} rejected route changed miss list: baseline={baseline_miss}, routed={routed_miss}"
            )

    routed_recall20 = report["retrievers"][ROUTED_RETRIEVER]["aggregate"]["recall@20"]
    baseline_recall20 = report["retrievers"][BASELINE_RETRIEVER]["aggregate"]["recall@20"]
    if routed_recall20 < baseline_recall20:
        failures.append(f"routed recall@20 regressed: {routed_recall20:.3f} < {baseline_recall20:.3f}")

    return {
        "ok": not failures,
        "k": report["k"],
        "baseline_recall20": baseline_recall20,
        "routed_recall20": routed_recall20,
        "accepted": accepted,
        "seeded": seeded,
        "rejected": rejected,
        "failures": failures,
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        f"ok: {payload['ok']}",
        f"k: {payload['k']}",
        f"baseline_recall@20: {payload['baseline_recall20']:.3f}",
        f"source_routed_recall@20: {payload['routed_recall20']:.3f}",
        "accepted:",
    ]
    for item_id, row in payload["accepted"].items():
        lines.append(f"  {item_id}: baseline_miss={row['baseline_miss']} routed_miss={row['routed_miss']}")
    lines.append("seeded:")
    for item_id, row in payload["seeded"].items():
        lines.append(f"  {item_id}: baseline_miss={row['baseline_miss']} routed_miss={row['routed_miss']}")
    lines.append("rejected:")
    for item_id, row in payload["rejected"].items():
        lines.append(f"  {item_id}: baseline_miss={row['baseline_miss']} routed_miss={row['routed_miss']}")
    if payload["failures"]:
        lines.append("failures:")
        lines.extend(f"  - {failure}" for failure in payload["failures"])
    return "\n".join(lines)


def _items_by_id(report: dict[str, Any], retriever: str) -> dict[str, dict[str, Any]]:
    return {
        row["id"]: row
        for row in report["retrievers"][retriever]["per_item"]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate accepted-cluster source_routed_hybrid retrieval.")
    parser.add_argument("--goldset", type=Path, default=DEFAULT_GOLDSET)
    parser.add_argument("--k", type=int, default=DEFAULT_K)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    payload = build_report(goldset=args.goldset, k=args.k)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(payload))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
