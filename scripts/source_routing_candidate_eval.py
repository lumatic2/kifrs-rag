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
    from kifrs.eval.retrieval import _load_goldset, _ranked_keys, gold_rank_summary, rrf_fuse_results
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.embed import search_hybrid
    from kifrs.eval.models import GoldItem
    from kifrs.eval.retrieval import _load_goldset, _ranked_keys, gold_rank_summary, rrf_fuse_results


DEFAULT_GOLDSET = Path("data/eval/goldset.json")
DEFAULT_GATE_K = 20
DEFAULT_LIMIT = 50


@dataclass(frozen=True)
class SourceRouteCandidate:
    item_id: str
    target_citation: str
    route_standard: str
    rationale: str


DEFAULT_CANDIDATES = (
    SourceRouteCandidate("Q001", "1115-27", "1115", "Revenue recognition cluster."),
    SourceRouteCandidate("Q004", "1001-69", "1001", "Current liability classification cluster."),
    SourceRouteCandidate("Q006", "1115-51", "1115", "Variable consideration constraint cluster."),
    SourceRouteCandidate("Q008", "1109-2.1", "1109", "Financial instrument scope plus lease cross-standard cluster."),
    SourceRouteCandidate("Q013", "1037-68", "1037", "Provision/contingent liability disclosure cluster."),
    SourceRouteCandidate("Q025", "1037-83", "1037", "Provision disclosure cluster."),
    SourceRouteCandidate("Q026", "1037-60", "1037", "Provision discounting/unwinding cluster."),
    SourceRouteCandidate("Q029", "1116-45", "1116", "Lease modification cluster."),
    SourceRouteCandidate("Q040", "1109-4.1.4", "1109", "Financial asset classification cluster."),
    SourceRouteCandidate("Q041", "1102-11", "1102", "Share-based payment vesting condition cluster."),
)


SearchFn = Callable[[str, str | None, int], list[dict[str, Any]]]


def evaluate_candidates(
    items: list[GoldItem],
    candidates: tuple[SourceRouteCandidate, ...] = DEFAULT_CANDIDATES,
    *,
    limit: int = DEFAULT_LIMIT,
    gate_k: int = DEFAULT_GATE_K,
    search_fn: SearchFn = search_hybrid,
) -> dict[str, Any]:
    item_by_id = {item.id: item for item in items}
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        item = item_by_id[candidate.item_id]
        gold = {(cite.standard, str(cite.no)) for cite in item.must_cite}
        baseline = search_fn(item.question, None, limit)
        routed = search_fn(item.question, candidate.route_standard, limit)
        fused = rrf_fuse_results([baseline, baseline, routed], limit=limit)
        base_ranked = _ranked_keys(baseline)
        routed_ranked = _ranked_keys(routed)
        fused_ranked = _ranked_keys(fused)
        base_ranks = gold_rank_summary(gold, base_ranked)
        routed_ranks = gold_rank_summary(gold, routed_ranked)
        fused_ranks = gold_rank_summary(gold, fused_ranked)
        base_rank = base_ranks.get(candidate.target_citation)
        routed_rank = routed_ranks.get(candidate.target_citation)
        fused_rank = fused_ranks.get(candidate.target_citation)
        rows.append(
            {
                "item_id": candidate.item_id,
                "target_citation": candidate.target_citation,
                "route_standard": candidate.route_standard,
                "target_rank_before": base_rank,
                "target_rank_routed": routed_rank,
                "target_rank_fused": fused_rank,
                "target_improved": _is_improved(base_rank, fused_rank, gate_k),
                "preserves_existing_hits": _preserves_existing_hits(base_ranks, fused_ranks, gate_k),
                "candidate": _is_improved(base_rank, fused_rank, gate_k)
                and _preserves_existing_hits(base_ranks, fused_ranks, gate_k),
                "base_ranks": base_ranks,
                "routed_ranks": routed_ranks,
                "fused_ranks": fused_ranks,
                "rationale": candidate.rationale,
            }
        )
    return {"limit": limit, "gate_k": gate_k, "rows": rows}


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Source Routing Candidate Evaluation",
        "",
        f"> Limit: {report['limit']}",
        f"> Gate K: {report['gate_k']}",
        "",
        "| Item | Route | Target | Before | Routed | Fused | Decision |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for row in report["rows"]:
        decision = "candidate" if row["candidate"] else "reject"
        lines.append(
            "| {item} | `{route}` | `{target}` | {before} | {routed} | {fused} | {decision} |".format(
                item=row["item_id"],
                route=row["route_standard"],
                target=row["target_citation"],
                before=_rank_text(row["target_rank_before"]),
                routed=_rank_text(row["target_rank_routed"]),
                fused=_rank_text(row["target_rank_fused"]),
                decision=decision,
            )
        )
    lines.extend(["", "## Detail", ""])
    for row in report["rows"]:
        lines.extend(
            [
                f"### {row['item_id']} -> {row['route_standard']}",
                "",
                f"- Target citation: `{row['target_citation']}`",
                f"- Base ranks: `{json.dumps(row['base_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Routed ranks: `{json.dumps(row['routed_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Fused ranks: `{json.dumps(row['fused_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Target improved: `{row['target_improved']}`",
                f"- Preserves existing hits: `{row['preserves_existing_hits']}`",
                f"- Rationale: {row['rationale']}",
                "",
            ]
        )
    return "\n".join(lines)


def _is_improved(before: int | None, after: int | None, gate_k: int) -> bool:
    if after is None or after > gate_k:
        return False
    if before is None or before > gate_k:
        return True
    return after < before


def _preserves_existing_hits(
    before: dict[str, int | None],
    after: dict[str, int | None],
    gate_k: int,
) -> bool:
    for citation, rank in before.items():
        if rank is None or rank > gate_k:
            continue
        new_rank = after.get(citation)
        if new_rank is None or new_rank > gate_k:
            return False
    return True


def _rank_text(value: int | None) -> str:
    return "absent" if value is None else str(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate supplemental standard routing candidates.")
    parser.add_argument("--goldset", type=Path, default=DEFAULT_GOLDSET)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--gate-k", type=int, default=DEFAULT_GATE_K)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    wanted = {candidate.item_id for candidate in DEFAULT_CANDIDATES}
    items = [item for item in _load_goldset(args.goldset) if item.id in wanted]
    report = evaluate_candidates(items, limit=args.limit, gate_k=args.gate_k)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
