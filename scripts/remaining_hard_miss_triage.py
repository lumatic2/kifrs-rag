from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from kifrs.eval.retrieval import _load_goldset, evaluate
    from scripts.hard_miss_candidate_eval import DEFAULT_CANDIDATES, evaluate_candidates
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.eval.retrieval import _load_goldset, evaluate
    from scripts.hard_miss_candidate_eval import DEFAULT_CANDIDATES, evaluate_candidates


DEFAULT_GOLDSET = Path("data/eval/goldset.json")
DEFAULT_ITEMS = ("Q001", "Q006", "Q008", "Q040")
DEFAULT_RETRIEVER = "source_routed_hybrid"

TRIAGE_NOTES: dict[str, dict[str, str]] = {
    "Q001": {
        "classification": "near_miss_candidate_pool",
        "finding": "1115-22 is recovered but 1115-27 stays just outside the gate after expansion.",
        "next_action": "Do not add a one-off seed yet; test a 1115 performance-obligation subquery or rerank rule.",
    },
    "Q006": {
        "classification": "concept_gap",
        "finding": "1115-55 is recovered but 1115-51 remains absent even with the variable-consideration expansion.",
        "next_action": "Rework query design around variable consideration and refund liability rather than adding the rejected seed.",
    },
    "Q008": {
        "classification": "cross_standard_scope_gap",
        "finding": "1116 lease measurement citations are recovered but the 1109 scope exclusion remains absent.",
        "next_action": "Handle as cross-standard decomposition: ask a separate 1109 scope-exclusion subquery while preserving 1116 hits.",
    },
    "Q040": {
        "classification": "k_boundary_near_miss",
        "finding": "1109-4.1.4 moves near top-20 but does not enter the gate.",
        "next_action": "Review whether K=20 is the right gate for this citation or test a narrow 1109 classification reranker.",
    },
}


def build_report(
    *,
    goldset: Path = DEFAULT_GOLDSET,
    item_ids: tuple[str, ...] = DEFAULT_ITEMS,
    retriever: str = DEFAULT_RETRIEVER,
    k: int = 20,
    candidate_limit: int = 50,
) -> dict[str, Any]:
    wanted = set(item_ids)
    items = [item for item in _load_goldset(goldset) if item.id in wanted]
    missing = sorted(wanted - {item.id for item in items})
    if missing:
        raise ValueError(f"goldset missing item ids: {', '.join(missing)}")

    eval_report = evaluate(items, [retriever], k)
    per_item = {
        row["id"]: row
        for row in eval_report["retrievers"][retriever]["per_item"]
    }
    candidates = tuple(candidate for candidate in DEFAULT_CANDIDATES if candidate.item_id in wanted)
    candidate_report = evaluate_candidates(items, candidates, limit=candidate_limit, gate_k=k)
    candidate_by_item = {row["item_id"]: row for row in candidate_report["rows"]}

    rows = []
    for item_id in item_ids:
        item_row = per_item[item_id]
        candidate_row = candidate_by_item[item_id]
        note = TRIAGE_NOTES[item_id]
        rows.append(
            {
                "item_id": item_id,
                "miss": item_row["miss"],
                "hit": item_row["hit"],
                "gold_ranks": item_row["gold_ranks"],
                "candidate_id": candidate_row["candidate_id"],
                "candidate_target": candidate_row["target_citation"],
                "candidate_rank_before": candidate_row["target_rank_before"],
                "candidate_rank_after": candidate_row["target_rank_after"],
                "candidate_decision": "candidate" if candidate_row["candidate"] else "reject",
                "classification": note["classification"],
                "finding": note["finding"],
                "next_action": note["next_action"],
            }
        )

    aggregate = eval_report["retrievers"][retriever]["aggregate"]
    return {
        "retriever": retriever,
        "k": k,
        "candidate_limit": candidate_limit,
        "aggregate": aggregate,
        "rows": rows,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Remaining Hard Miss Triage",
        "",
        f"> Retriever: `{report['retriever']}`",
        f"> K: {report['k']}",
        f"> Candidate limit: {report['candidate_limit']}",
        "",
        "## Summary",
        "",
        "| Item | Miss | Existing hit | Candidate after | Decision | Classification |",
        "|---|---|---|---:|---|---|",
    ]
    for row in report["rows"]:
        lines.append(
            "| {item} | {miss} | {hit} | {after} | {decision} | `{classification}` |".format(
                item=row["item_id"],
                miss=_citations_text(row["miss"]),
                hit=_citations_text(row["hit"]),
                after=_rank_text(row["candidate_rank_after"]),
                decision=row["candidate_decision"],
                classification=row["classification"],
            )
        )
    lines.extend(["", "## Triage", ""])
    for row in report["rows"]:
        lines.extend(
            [
                f"### {row['item_id']}",
                "",
                f"- Gold ranks: `{json.dumps(row['gold_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Candidate: `{row['candidate_id']}` -> `{row['candidate_decision']}`",
                f"- Finding: {row['finding']}",
                f"- Next action: {row['next_action']}",
                "",
            ]
        )
    return "\n".join(lines)


def _citations_text(citations: list[Any]) -> str:
    if not citations:
        return "-"
    return ", ".join(f"`{standard}-{no}`" for standard, no in citations)


def _rank_text(value: int | None) -> str:
    return "absent" if value is None else str(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify remaining source_routed_hybrid hard misses.")
    parser.add_argument("--goldset", type=Path, default=DEFAULT_GOLDSET)
    parser.add_argument("--only", nargs="+", default=list(DEFAULT_ITEMS))
    parser.add_argument("--retriever", default=DEFAULT_RETRIEVER)
    parser.add_argument("--k", type=int, default=20)
    parser.add_argument("--candidate-limit", type=int, default=50)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    payload = build_report(
        goldset=args.goldset,
        item_ids=tuple(args.only),
        retriever=args.retriever,
        k=args.k,
        candidate_limit=args.candidate_limit,
    )
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
