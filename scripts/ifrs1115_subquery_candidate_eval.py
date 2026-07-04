from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

try:
    from kifrs.embed import search_hybrid
    from kifrs.eval.models import GoldItem
    from kifrs.eval.retrieval import (
        _load_goldset,
        _ranked_keys,
        gold_rank_summary,
        rrf_fuse_results,
        search_source_routed_hybrid,
    )
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.embed import search_hybrid
    from kifrs.eval.models import GoldItem
    from kifrs.eval.retrieval import (
        _load_goldset,
        _ranked_keys,
        gold_rank_summary,
        rrf_fuse_results,
        search_source_routed_hybrid,
    )


DEFAULT_GOLDSET = Path("data/eval/goldset.json")
DEFAULT_ITEMS = ("Q001", "Q006")
DEFAULT_K = 20
DEFAULT_LIMIT = 100
DEFAULT_SUBQUERY_WEIGHT = 2


@dataclass(frozen=True)
class SubqueryCandidate:
    item_id: str
    candidate_id: str
    target_citation: str
    standard: str
    subquery: str
    rationale: str


DEFAULT_CANDIDATES = (
    SubqueryCandidate(
        item_id="Q001",
        candidate_id="q001-performance-obligation-criteria",
        target_citation="1115-27",
        standard="1115",
        subquery="고객 효익 쉽게 구할 수 있는 다른 자원 별도 식별 계약 내 다른 약속 구별",
        rationale="Q001 already recovers 1115-22; the missing citation is the distinct-good-or-service criteria paragraph.",
    ),
    SubqueryCandidate(
        item_id="Q006",
        candidate_id="q006-variable-consideration-refund",
        target_citation="1115-51",
        standard="1115",
        subquery="리베이트 환불 가격할인 변동대가 미래 사건 거래가격 환불부채",
        rationale="Q006 already recovers 1115-55; the missing citation is the variable-consideration source paragraph.",
    ),
)


SearchFn = Callable[[str, str | None, int], list[dict[str, Any]]]


def evaluate_subqueries(
    items: list[GoldItem],
    candidates: tuple[SubqueryCandidate, ...] = DEFAULT_CANDIDATES,
    *,
    k: int = DEFAULT_K,
    limit: int = DEFAULT_LIMIT,
    subquery_weight: int = DEFAULT_SUBQUERY_WEIGHT,
    baseline_search_fn: SearchFn = search_source_routed_hybrid,
    subquery_search_fn: SearchFn = search_hybrid,
) -> dict[str, Any]:
    item_by_id = {item.id: item for item in items}
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        item = item_by_id[candidate.item_id]
        gold = {(cite.standard, str(cite.no)) for cite in item.must_cite}
        baseline_results = baseline_search_fn(item.question, None, limit)
        subquery_results = subquery_search_fn(candidate.subquery, candidate.standard, limit)
        fused_results = rrf_fuse_results(
            [baseline_results, *([subquery_results] * subquery_weight)],
            limit=limit,
        )
        baseline_ranks = gold_rank_summary(gold, _ranked_keys(baseline_results))
        subquery_ranks = gold_rank_summary(gold, _ranked_keys(subquery_results))
        fused_ranks = gold_rank_summary(gold, _ranked_keys(fused_results))
        target_before = baseline_ranks.get(candidate.target_citation)
        target_after = fused_ranks.get(candidate.target_citation)
        rows.append(
            {
                "item_id": candidate.item_id,
                "candidate_id": candidate.candidate_id,
                "target_citation": candidate.target_citation,
                "standard": candidate.standard,
                "subquery": candidate.subquery,
                "baseline_ranks": baseline_ranks,
                "subquery_ranks": subquery_ranks,
                "fused_ranks": fused_ranks,
                "target_rank_before": target_before,
                "target_rank_after": target_after,
                "target_recovered": _in_gate(target_after, k) and not _in_gate(target_before, k),
                "preserves_existing_hits": _preserves_existing_hits(baseline_ranks, fused_ranks, k),
                "rationale": candidate.rationale,
            }
        )
    for row in rows:
        row["candidate"] = row["target_recovered"] and row["preserves_existing_hits"]
    return {"k": k, "limit": limit, "subquery_weight": subquery_weight, "rows": rows}


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# IFRS 1115 Subquery Candidate Evaluation",
        "",
        f"> K: {report['k']}",
        f"> Limit: {report['limit']}",
        f"> Subquery weight: {report['subquery_weight']}",
        "",
        "| Item | Candidate | Target | Before | After | Decision |",
        "|---|---|---|---:|---:|---|",
    ]
    for row in report["rows"]:
        decision = "candidate" if row["candidate"] else "reject"
        lines.append(
            "| {item} | `{candidate}` | `{target}` | {before} | {after} | {decision} |".format(
                item=row["item_id"],
                candidate=row["candidate_id"],
                target=row["target_citation"],
                before=_rank_text(row["target_rank_before"]),
                after=_rank_text(row["target_rank_after"]),
                decision=decision,
            )
        )
    lines.extend(["", "## Detail", ""])
    for row in report["rows"]:
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- Subquery: `{row['subquery']}`",
                f"- Baseline ranks: `{json.dumps(row['baseline_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Subquery-only ranks: `{json.dumps(row['subquery_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Fused ranks: `{json.dumps(row['fused_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Preserves existing hits: `{row['preserves_existing_hits']}`",
                f"- Rationale: {row['rationale']}",
                "",
            ]
        )
    return "\n".join(lines)


def _in_gate(rank: int | None, k: int) -> bool:
    return rank is not None and rank <= k


def _preserves_existing_hits(
    before: dict[str, int | None],
    after: dict[str, int | None],
    k: int,
) -> bool:
    for citation, rank in before.items():
        if not _in_gate(rank, k):
            continue
        if not _in_gate(after.get(citation), k):
            return False
    return True


def _rank_text(value: int | None) -> str:
    return "absent" if value is None else str(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate focused IFRS 1115 subqueries for remaining hard misses.")
    parser.add_argument("--goldset", type=Path, default=DEFAULT_GOLDSET)
    parser.add_argument("--only", nargs="+", default=list(DEFAULT_ITEMS))
    parser.add_argument("--k", type=int, default=DEFAULT_K)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--subquery-weight", type=int, default=DEFAULT_SUBQUERY_WEIGHT)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    wanted = set(args.only)
    items = [item for item in _load_goldset(args.goldset) if item.id in wanted]
    missing = sorted(wanted - {item.id for item in items})
    if missing:
        raise ValueError(f"goldset missing item ids: {', '.join(missing)}")
    candidates = tuple(candidate for candidate in DEFAULT_CANDIDATES if candidate.item_id in wanted)
    payload = evaluate_subqueries(
        items,
        candidates,
        k=args.k,
        limit=args.limit,
        subquery_weight=args.subquery_weight,
    )
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
