from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

try:
    from kifrs.eval.models import GoldItem
    from kifrs.eval.retrieval import (
        _load_goldset,
        _ranked_keys,
        gold_rank_summary,
        search_source_routed_hybrid,
    )
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.eval.models import GoldItem
    from kifrs.eval.retrieval import (
        _load_goldset,
        _ranked_keys,
        gold_rank_summary,
        search_source_routed_hybrid,
    )


DEFAULT_GOLDSET = Path("data/eval/goldset.json")
DEFAULT_ITEMS = ("Q001", "Q006", "Q008", "Q029", "Q040")


@dataclass(frozen=True)
class HardMissCandidate:
    item_id: str
    candidate_id: str
    target_citation: str
    expansion: str
    rationale: str


DEFAULT_CANDIDATES = (
    HardMissCandidate(
        item_id="Q001",
        candidate_id="q001-distinct-performance-obligation",
        target_citation="1115-27",
        expansion="구별되는 수행의무 고객이 그 자체로 효익 별도로 식별 가능 계약 내 다른 약속과 구별",
        rationale="K-IFRS 1115-27 distinct performance obligation criteria are not explicit enough in the package-sale question.",
    ),
    HardMissCandidate(
        item_id="Q006",
        candidate_id="q006-variable-consideration-constraint",
        target_citation="1115-51",
        expansion="변동대가 추정치 제약 유의적인 수익 환원 가능성이 매우 높음 환불부채",
        rationale="The refund program question finds refund liability guidance but misses the variable consideration constraint paragraph.",
    ),
    HardMissCandidate(
        item_id="Q008",
        candidate_id="q008-lease-liability-ifrs9-scope",
        target_citation="1109-2.1",
        expansion="리스부채 금융상품 기준서 적용 제외 리스 기준서 적용 범위 금융부채 상각후원가",
        rationale="The lease liability question blends K-IFRS 1116 measurement with K-IFRS 1109 scope exclusions.",
    ),
    HardMissCandidate(
        item_id="Q029",
        candidate_id="q029-lease-modification-decrease-scope",
        target_citation="1116-45",
        expansion="리스변경 별도 리스 아님 리스 범위 감소 사용권자산 장부금액 감소 손익 인식",
        rationale="Lease scope decrease wording should route to K-IFRS 1116-45 before the generic remeasurement paragraph.",
    ),
    HardMissCandidate(
        item_id="Q040",
        candidate_id="q040-sppi-fail-fvtpl-classification",
        target_citation="1109-4.1.4",
        expansion="계약상 현금흐름 원리금 지급만 아님 SPPI 불충족 당기손익 공정가치 측정 금융자산",
        rationale="SPPI failure should retrieve the residual fair value through profit or loss classification paragraph.",
    ),
)


SearchFn = Callable[[str, str | None, int], list[dict[str, Any]]]


def evaluate_candidates(
    items: list[GoldItem],
    candidates: tuple[HardMissCandidate, ...] = DEFAULT_CANDIDATES,
    *,
    limit: int = 50,
    gate_k: int = 20,
    search_fn: SearchFn = search_source_routed_hybrid,
) -> dict[str, Any]:
    item_by_id = {item.id: item for item in items}
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        item = item_by_id[candidate.item_id]
        gold = {(cite.standard, str(cite.no)) for cite in item.must_cite}
        baseline_ranked = _ranked_keys(search_fn(item.question, None, limit))
        expanded_ranked = _ranked_keys(search_fn(f"{item.question} {candidate.expansion}", None, limit))
        baseline_ranks = gold_rank_summary(gold, baseline_ranked)
        expanded_ranks = gold_rank_summary(gold, expanded_ranked)
        target_before = baseline_ranks.get(candidate.target_citation)
        target_after = expanded_ranks.get(candidate.target_citation)
        target_improved = _is_improved(target_before, target_after, gate_k)
        preserved = _preserves_existing_hits(baseline_ranks, expanded_ranks, gate_k)
        rows.append(
            {
                "item_id": candidate.item_id,
                "candidate_id": candidate.candidate_id,
                "target_citation": candidate.target_citation,
                "expansion": candidate.expansion,
                "target_rank_before": target_before,
                "target_rank_after": target_after,
                "target_improved": target_improved,
                "preserves_existing_hits": preserved,
                "candidate": target_improved and preserved,
                "baseline_ranks": baseline_ranks,
                "expanded_ranks": expanded_ranks,
                "rationale": candidate.rationale,
            }
        )
    return {"limit": limit, "gate_k": gate_k, "rows": rows}


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Hard Miss Candidate Evaluation",
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
                f"- Expansion: `{row['expansion']}`",
                f"- Target citation: `{row['target_citation']}`",
                f"- Baseline ranks: `{json.dumps(row['baseline_ranks'], ensure_ascii=False, sort_keys=True)}`",
                f"- Expanded ranks: `{json.dumps(row['expanded_ranks'], ensure_ascii=False, sort_keys=True)}`",
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
    parser = argparse.ArgumentParser(description="Evaluate expansion candidates for remaining hard misses.")
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
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
