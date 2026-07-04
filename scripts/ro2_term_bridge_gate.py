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
DEFAULT_ITEMS = ("Q039", "Q048")
DEFAULT_RETRIEVER = "hybrid"
DEFAULT_K = 20
REMEDIATION = "python scripts\\seed_user_notes.py --apply"


def build_report(
    *,
    goldset: Path = DEFAULT_GOLDSET,
    item_ids: tuple[str, ...] = DEFAULT_ITEMS,
    retriever: str = DEFAULT_RETRIEVER,
    k: int = DEFAULT_K,
) -> dict[str, Any]:
    wanted = set(item_ids)
    items = [item for item in _load_goldset(goldset) if item.id in wanted]
    missing = sorted(wanted - {item.id for item in items})
    if missing:
        raise ValueError(f"goldset missing item ids: {', '.join(missing)}")
    report = evaluate(items, [retriever], k)
    return evaluate_gate(report, retriever=retriever, min_recall_at_k=1.0)


def evaluate_gate(
    report: dict[str, Any],
    *,
    retriever: str = DEFAULT_RETRIEVER,
    min_recall_at_k: float = 1.0,
) -> dict[str, Any]:
    data = report["retrievers"][retriever]
    metric_name = f"recall@{report['k']}"
    recall_at_k = data["aggregate"][metric_name]
    failures: list[str] = []
    if recall_at_k < min_recall_at_k:
        failures.append(f"{metric_name} {recall_at_k:.3f} < {min_recall_at_k:.3f}")
    for item in data["per_item"]:
        if item.get("miss"):
            failures.append(f"{item['id']} still misses {item['miss']}")
    return {
        "ok": not failures,
        "retriever": retriever,
        "k": report["k"],
        "metric": metric_name,
        "min_recall_at_k": min_recall_at_k,
        "recall_at_k": recall_at_k,
        "aggregate": data["aggregate"],
        "per_item": [
            {
                "id": item["id"],
                "hit": item["hit"],
                "miss": item["miss"],
                "gold_ranks": item["gold_ranks"],
            }
            for item in data["per_item"]
        ],
        "failures": failures,
        "remediation": REMEDIATION,
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        f"ok: {payload['ok']}",
        f"retriever: {payload['retriever']}",
        f"k: {payload['k']}",
        f"{payload['metric']}: {payload['recall_at_k']:.3f}",
        "aggregate:",
    ]
    for key, value in payload["aggregate"].items():
        lines.append(f"  {key}: {value:.3f}")
    lines.append("per_item:")
    for item in payload["per_item"]:
        lines.append(f"  {item['id']}: miss={item['miss']} gold_ranks={item['gold_ranks']}")
    if payload["failures"]:
        lines.append("failures:")
        lines.extend(f"  - {failure}" for failure in payload["failures"])
        lines.append(f"remediation: {payload['remediation']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="RO2 reviewed term bridge regression gate.")
    parser.add_argument("--goldset", type=Path, default=DEFAULT_GOLDSET)
    parser.add_argument("--only", nargs="+", default=list(DEFAULT_ITEMS))
    parser.add_argument("--retriever", default=DEFAULT_RETRIEVER)
    parser.add_argument("--k", type=int, default=DEFAULT_K)
    parser.add_argument("--format", choices=["json", "text"], default="text")
    args = parser.parse_args()

    payload = build_report(
        goldset=args.goldset,
        item_ids=tuple(args.only),
        retriever=args.retriever,
        k=args.k,
    )
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(payload))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
