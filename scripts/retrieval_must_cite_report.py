from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from kifrs.eval.retrieval import (
        _load_goldset,
        evaluate,
        must_cite_rank_rows,
        must_cite_rank_summary,
    )
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.eval.retrieval import (
        _load_goldset,
        evaluate,
        must_cite_rank_rows,
        must_cite_rank_summary,
    )


DEFAULT_GOLDSET = Path("data/eval/goldset.json")


def build_report(
    *,
    goldset: Path = DEFAULT_GOLDSET,
    retrievers: list[str] | None = None,
    k: int = 20,
    only: list[str] | None = None,
) -> dict[str, Any]:
    items = _load_goldset(goldset)
    if only:
        wanted = set(only)
        items = [item for item in items if item.id in wanted]
        missing = sorted(wanted - {item.id for item in items})
        if missing:
            raise ValueError(f"goldset missing item ids: {', '.join(missing)}")
    report = evaluate(items, retrievers or ["hybrid"], k)
    return {
        "k": k,
        "n_items": len(items),
        "summary": must_cite_rank_summary(report),
        "rows": must_cite_rank_rows(report),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Must-Cite Retrieval Rank Report",
        "",
        f"> Items: {payload['n_items']}",
        f"> K: {payload['k']}",
        "",
        "## Summary",
        "",
        "| Retriever | hit@5 | hit@10 | hit@20 | beyond@20 | absent |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for retriever, counts in payload["summary"].items():
        lines.append(
            "| {retriever} | {hit5} | {hit10} | {hit20} | {beyond20} | {absent} |".format(
                retriever=retriever,
                hit5=counts["hit@5"],
                hit10=counts["hit@10"],
                hit20=counts["hit@20"],
                beyond20=counts["beyond@20"],
                absent=counts["absent"],
            )
        )
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Retriever | Item | Citation | Rank | Bucket |",
            "|---|---|---|---:|---|",
        ]
    )
    for row in payload["rows"]:
        rank = "absent" if row["rank"] is None else str(row["rank"])
        lines.append(
            f"| {row['retriever']} | {row['item_id']} | `{row['citation']}` | {rank} | {row['bucket']} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render citation-level K-IFRS retrieval rank report.")
    parser.add_argument("--goldset", type=Path, default=DEFAULT_GOLDSET)
    parser.add_argument("--retrievers", nargs="+", default=["hybrid"])
    parser.add_argument("--only", nargs="+")
    parser.add_argument("--k", type=int, default=20)
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    payload = build_report(
        goldset=args.goldset,
        retrievers=args.retrievers,
        k=args.k,
        only=args.only,
    )
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
