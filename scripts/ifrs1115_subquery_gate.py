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
BASELINE_RETRIEVER = "source_routed_hybrid"
TARGET_RETRIEVER = "ifrs1115_subquery_hybrid"
ACCEPTED_SOURCE_ROUTE_ITEMS = ("Q004", "Q013", "Q025", "Q026", "Q041")
RECOVERED_1115_ITEMS = ("Q001", "Q006")
SEEDED_ITEMS = ("Q029",)
REJECTED_ITEMS = ("Q008", "Q040")
DEFAULT_K = 20


def build_report(*, goldset: Path = DEFAULT_GOLDSET, k: int = DEFAULT_K) -> dict[str, Any]:
    wanted = set(ACCEPTED_SOURCE_ROUTE_ITEMS + RECOVERED_1115_ITEMS + SEEDED_ITEMS + REJECTED_ITEMS)
    items = [item for item in _load_goldset(goldset) if item.id in wanted]
    missing = sorted(wanted - {item.id for item in items})
    if missing:
        raise ValueError(f"goldset missing item ids: {', '.join(missing)}")
    report = evaluate(items, [BASELINE_RETRIEVER, TARGET_RETRIEVER], k)
    return evaluate_gate(report)


def evaluate_gate(report: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    baseline_items = _items_by_id(report, BASELINE_RETRIEVER)
    target_items = _items_by_id(report, TARGET_RETRIEVER)

    accepted_source_route = _group_rows(ACCEPTED_SOURCE_ROUTE_ITEMS, baseline_items, target_items)
    recovered_1115 = _group_rows(RECOVERED_1115_ITEMS, baseline_items, target_items)
    seeded = _group_rows(SEEDED_ITEMS, baseline_items, target_items)
    rejected = _group_rows(REJECTED_ITEMS, baseline_items, target_items)

    for item_id, row in accepted_source_route.items():
        if row["target_miss"]:
            failures.append(f"{item_id} accepted source route regressed: {row['target_miss']}")
    for item_id, row in recovered_1115.items():
        if row["baseline_miss"] and not row["target_miss"]:
            continue
        failures.append(
            f"{item_id} 1115 subquery did not recover expected miss: "
            f"baseline={row['baseline_miss']}, target={row['target_miss']}"
        )
    for item_id, row in seeded.items():
        if row["baseline_miss"] or row["target_miss"]:
            failures.append(
                f"{item_id} reviewed seed should remain recovered: "
                f"baseline={row['baseline_miss']}, target={row['target_miss']}"
            )
    for item_id, row in rejected.items():
        if row["target_miss"] != row["baseline_miss"]:
            failures.append(
                f"{item_id} rejected item changed miss list: "
                f"baseline={row['baseline_miss']}, target={row['target_miss']}"
            )

    baseline_recall20 = report["retrievers"][BASELINE_RETRIEVER]["aggregate"]["recall@20"]
    target_recall20 = report["retrievers"][TARGET_RETRIEVER]["aggregate"]["recall@20"]
    if target_recall20 < baseline_recall20:
        failures.append(f"target recall@20 regressed: {target_recall20:.3f} < {baseline_recall20:.3f}")

    return {
        "ok": not failures,
        "k": report["k"],
        "baseline_recall20": baseline_recall20,
        "target_recall20": target_recall20,
        "accepted_source_route": accepted_source_route,
        "recovered_1115": recovered_1115,
        "seeded": seeded,
        "rejected": rejected,
        "failures": failures,
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        f"ok: {payload['ok']}",
        f"k: {payload['k']}",
        f"baseline_recall@20: {payload['baseline_recall20']:.3f}",
        f"ifrs1115_subquery_recall@20: {payload['target_recall20']:.3f}",
    ]
    for label in ("accepted_source_route", "recovered_1115", "seeded", "rejected"):
        lines.append(f"{label}:")
        for item_id, row in payload[label].items():
            lines.append(f"  {item_id}: baseline_miss={row['baseline_miss']} target_miss={row['target_miss']}")
    if payload["failures"]:
        lines.append("failures:")
        lines.extend(f"  - {failure}" for failure in payload["failures"])
    return "\n".join(lines)


def _group_rows(
    item_ids: tuple[str, ...],
    baseline_items: dict[str, dict[str, Any]],
    target_items: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    return {
        item_id: {
            "baseline_miss": baseline_items[item_id]["miss"],
            "target_miss": target_items[item_id]["miss"],
        }
        for item_id in item_ids
    }


def _items_by_id(report: dict[str, Any], retriever: str) -> dict[str, dict[str, Any]]:
    return {
        row["id"]: row
        for row in report["retrievers"][retriever]["per_item"]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate opt-in IFRS 1115 subquery retriever.")
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
