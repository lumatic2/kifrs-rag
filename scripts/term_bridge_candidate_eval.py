from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

try:
    from kifrs.embed import search_hybrid
    from kifrs.eval.models import GoldItem
    from kifrs.eval.retrieval import _load_goldset, _ranked_keys, gold_rank_summary
except ModuleNotFoundError:
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.embed import search_hybrid
    from kifrs.eval.models import GoldItem
    from kifrs.eval.retrieval import _load_goldset, _ranked_keys, gold_rank_summary


DEFAULT_GOLDSET = Path("data/eval/goldset.json")
DEFAULT_ITEMS = ("Q039", "Q048")


@dataclass(frozen=True)
class TermBridgeCandidate:
    item_id: str
    candidate_id: str
    trigger: str
    expansion: str
    target_citation: str
    rationale: str


DEFAULT_CANDIDATES = (
    TermBridgeCandidate(
        item_id="Q039",
        candidate_id="q039-provision-recognition",
        trigger="충당부채",
        expansion="현재의무 과거사건 자원 유출 가능성 신뢰성 있는 추정",
        target_citation="1037-14",
        rationale="IAS 37/K-IFRS 1037 provision recognition criteria terms are absent from the original lease-focused question.",
    ),
    TermBridgeCandidate(
        item_id="Q039",
        candidate_id="q039-restoration-provision",
        trigger="원상복구 의무",
        expansion="원상복구 복구원가 충당부채 현재의무",
        target_citation="1037-14",
        rationale="Tests whether restoration-cost wording alone is enough to retrieve the provision recognition paragraph.",
    ),
    TermBridgeCandidate(
        item_id="Q048",
        candidate_id="q048-recoverable-amount-definition",
        trigger="회수가능액",
        expansion="공정가치 처분부대원가 사용가치 둘 중 큰 금액",
        target_citation="1036-18",
        rationale="K-IFRS 1036-18 defines recoverable amount through fair value less costs of disposal and value in use.",
    ),
    TermBridgeCandidate(
        item_id="Q048",
        candidate_id="q048-impairment-recoverable",
        trigger="손상차손",
        expansion="회수가능액 순공정가치 사용가치",
        target_citation="1036-18",
        rationale="Tests a shorter impairment/recoverable amount bridge that may preserve the 1036-59 hit.",
    ),
)


SearchFn = Callable[[str, str | None, int], list[dict[str, Any]]]


def evaluate_candidates(
    items: list[GoldItem],
    candidates: tuple[TermBridgeCandidate, ...] = DEFAULT_CANDIDATES,
    *,
    limit: int = 50,
    gate_k: int = 20,
    search_fn: SearchFn = search_hybrid,
) -> dict[str, Any]:
    item_by_id = {item.id: item for item in items}
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        item = item_by_id[candidate.item_id]
        gold = {(cite.standard, str(cite.no)) for cite in item.must_cite}
        base_ranked = _ranked_keys(search_fn(item.question, None, limit))
        expanded_query = f"{item.question} {candidate.expansion}"
        candidate_ranked = _ranked_keys(search_fn(expanded_query, None, limit))
        base_ranks = gold_rank_summary(gold, base_ranked)
        candidate_ranks = gold_rank_summary(gold, candidate_ranked)
        target_before = base_ranks.get(candidate.target_citation)
        target_after = candidate_ranks.get(candidate.target_citation)
        preserved = _preserves_existing_hits(base_ranks, candidate_ranks, gate_k)
        target_improved = _is_improved(target_before, target_after, gate_k)
        rows.append(
            {
                "item_id": candidate.item_id,
                "candidate_id": candidate.candidate_id,
                "trigger": candidate.trigger,
                "expansion": candidate.expansion,
                "target_citation": candidate.target_citation,
                "target_rank_before": target_before,
                "target_rank_after": target_after,
                "target_improved": target_improved,
                "preserves_existing_hits": preserved,
                "candidate": target_improved and preserved,
                "base_ranks": base_ranks,
                "candidate_ranks": candidate_ranks,
                "rationale": candidate.rationale,
            }
        )
    return {"limit": limit, "gate_k": gate_k, "rows": rows}


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Term Bridge Candidate Evaluation",
        "",
        f"> Limit: {report['limit']}",
        f"> Gate K: {report['gate_k']}",
        "",
        "| Item | Candidate | Target | Before | After | Decision |",
        "|---|---|---|---:|---:|---|",
    ]
    for row in report["rows"]:
        decision = "candidate" if row["candidate"] else "reject"
        lines.append(
            "| {item_id} | `{candidate_id}` | `{target}` | {before} | {after} | {decision} |".format(
                item_id=row["item_id"],
                candidate_id=row["candidate_id"],
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
                f"- Trigger: `{row['trigger']}`",
                f"- Expansion: `{row['expansion']}`",
                f"- Target citation: `{row['target_citation']}`",
                f"- Base ranks: `{json.dumps(row['base_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Candidate ranks: `{json.dumps(row['candidate_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Target improved: `{row['target_improved']}`",
                f"- Preserves existing hits: `{row['preserves_existing_hits']}`",
                f"- Rationale: {row['rationale']}",
                "",
            ]
        )
    return "\n".join(lines)


def _is_improved(before: int | None, after: int | None, limit: int) -> bool:
    if after is None or after > limit:
        return False
    if before is None or before > limit:
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
    parser = argparse.ArgumentParser(description="Evaluate term bridge candidates without mutating user_note_v2.")
    parser.add_argument("--goldset", type=Path, default=DEFAULT_GOLDSET)
    parser.add_argument("--only", nargs="+", default=list(DEFAULT_ITEMS))
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--gate-k", type=int, default=20)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    wanted = set(args.only)
    items = [item for item in _load_goldset(args.goldset) if item.id in wanted]
    report = evaluate_candidates(items, limit=args.limit, gate_k=args.gate_k)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
