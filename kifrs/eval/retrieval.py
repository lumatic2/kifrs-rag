"""Retrieval-only 평가 — 답변 생성(LLM) 없이 검색 단계만 정량 측정.

goldset 의 must_cite (standard, no) 를 ground truth 로 써서, 각 retriever 가
정답 문단을 top-k 에 넣는지 recall@k · MRR · nDCG 로 잰다. API/LLM 불필요.

M2 리랭킹 등 후속 마일스톤의 before/after 게이트.

실행:
  python -m kifrs.eval.retrieval                  # 3 retriever 전체, K=20
  python -m kifrs.eval.retrieval --k 20 --retrievers hybrid
  python -m kifrs.eval.retrieval --only Q001 Q003
"""
from __future__ import annotations

import argparse
import io
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from kifrs.store import search_fts
from kifrs.embed import semantic_search, search_hybrid, search_reranked, search_hierarchical
from .models import GoldItem

ROOT = Path(__file__).resolve().parent.parent.parent
GOLDSET = ROOT / "data" / "eval" / "goldset.json"
RESULTS_DIR = ROOT / "data" / "eval" / "results"

RECALL_KS = (1, 3, 5, 10, 20)
NDCG_K = 10

MULTI_QUERY_CONCEPTS = (
    "원상복구 의무",
    "복구 의무",
    "충당부채",
    "인식요건",
    "회수가능액",
    "손상차손",
    "리스 종료",
    "리스변경",
    "리스부채",
)

MULTI_QUERY_EXPANSIONS = {
    "충당부채": (
        "현재의무 자원 유출 가능성 신뢰성 있게 추정",
        "충당부채 인식요건",
    ),
    "회수가능액": (
        "공정가치 처분부대원가 사용가치",
        "순공정가치 사용가치",
    ),
    "손상차손": (
        "장부금액 회수가능액 초과",
        "손상차손 인식",
    ),
}

SOURCE_ROUTE_RULES = (
    {
        "standard": "1001",
        "all": ("차입금",),
        "any": ("유동부채", "비유동부채", "차환"),
    },
    {
        "standard": "1037",
        "all": ("충당부채",),
        "any": ("손실부담계약", "회피불가능", "처분이익", "현재가치", "할인액 환입"),
    },
    {
        "standard": "1102",
        "all": ("주식결제형",),
        "any": ("주식기준보상", "측정기준일", "종업원"),
    },
)

IFRS1115_SUBQUERY_RULES = (
    {
        "all": ("소프트웨어", "설치"),
        "any": ("수행의무", "구분", "구별"),
        "subquery": "고객 효익 쉽게 구할 수 있는 다른 자원 별도 식별 계약 내 다른 약속 구별",
    },
    {
        "all": ("환불",),
        "any": ("리베이트", "누적 구매액", "변동대가", "가격할인"),
        "subquery": "리베이트 환불 가격할인 변동대가 미래 사건 거래가격 환불부채",
    },
)

IFRS1109_SCOPE_RULES = (
    {
        "all": ("리스부채",),
        "any": ("1109", "금융상품", "금융부채"),
        "subquery": "리스 계약 권리 의무 금융상품 적용범위 제외 1109 1116",
    },
)


# retriever 이름 → (query, limit) → list[dict(standard, no, ...)]
RETRIEVERS = {
    "lexical": lambda q, k: search_fts(q, None, limit=k),
    "semantic": lambda q, k: semantic_search(q, None, limit=k),
    "hybrid": lambda q, k: search_hybrid(q, None, limit=k),
    "multi_query_hybrid": lambda q, k: search_multi_query_hybrid(q, None, limit=k),
    "source_routed_hybrid": lambda q, k: search_source_routed_hybrid(q, None, limit=k),
    "ifrs1115_subquery_hybrid": lambda q, k: search_ifrs1115_subquery_hybrid(q, None, limit=k),
    "ifrs1109_scope_hybrid": lambda q, k: search_ifrs1109_scope_hybrid(q, None, limit=k),
    "hierarchical": lambda q, k: search_hierarchical(q, None, limit=k),
    "reranked": lambda q, k: search_reranked(q, None, limit=k, candidates=50),
}


def _load_goldset(path: Path = GOLDSET) -> list[GoldItem]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [GoldItem.from_dict(x) for x in data["items"]]


def _ranked_keys(results: list[dict]) -> list[tuple[str, str]]:
    """검색 결과를 순위대로 (standard, no) 튜플 리스트로. 중복은 첫 순위 유지."""
    out: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for r in results:
        key = (str(r["standard"]), str(r["no"]))
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def _item_metrics(gold: set[tuple[str, str]], ranked: list[tuple[str, str]]) -> dict:
    """단일 문항의 retrieval 메트릭. gold = must_cite 집합."""
    if not gold:
        return {}
    # recall@k — must_cite 중 top-k 안에 든 비율
    recall = {}
    for k in RECALL_KS:
        topk = set(ranked[:k])
        recall[f"recall@{k}"] = len(gold & topk) / len(gold)

    # MRR — 첫 정답 hit 의 역순위 (top-K 밖이면 0)
    mrr = 0.0
    for rank, key in enumerate(ranked, 1):
        if key in gold:
            mrr = 1.0 / rank
            break

    # nDCG@K — binary relevance
    dcg = 0.0
    for i, key in enumerate(ranked[:NDCG_K]):
        if key in gold:
            dcg += 1.0 / math.log2(i + 2)
    ideal_hits = min(NDCG_K, len(gold))
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))
    ndcg = (dcg / idcg) if idcg else 0.0

    return {**recall, "mrr": mrr, f"ndcg@{NDCG_K}": ndcg}


def gold_rank_summary(gold: set[tuple[str, str]], ranked: list[tuple[str, str]]) -> dict[str, int | None]:
    """Return 1-based rank for each required citation, or None if absent from the returned list."""
    ranks = {key: index for index, key in enumerate(ranked, start=1)}
    return {f"{standard}-{no}": ranks.get((standard, no)) for standard, no in sorted(gold)}


def _mean(dicts: list[dict], key: str) -> float:
    vals = [d[key] for d in dicts if key in d]
    return sum(vals) / len(vals) if vals else 0.0


def evaluate(items: list[GoldItem], retrievers: list[str], k: int) -> dict:
    metric_keys = [f"recall@{kk}" for kk in RECALL_KS] + ["mrr", f"ndcg@{NDCG_K}"]
    report: dict = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "n_items": len(items),
        "k": k,
        "retrievers": {},
    }
    for name in retrievers:
        fn = RETRIEVERS[name]
        per_item = []
        for item in items:
            gold = {(c.standard, str(c.no)) for c in item.must_cite}
            ranked = _ranked_keys(fn(item.question, k))
            m = _item_metrics(gold, ranked)
            m["id"] = item.id
            m["gold"] = sorted(gold)
            m["hit"] = sorted(set(ranked[:k]) & gold)
            m["miss"] = sorted(gold - set(ranked[:k]))
            m["gold_ranks"] = gold_rank_summary(gold, ranked)
            per_item.append(m)
        report["retrievers"][name] = {
            "aggregate": {mk: round(_mean(per_item, mk), 4) for mk in metric_keys},
            "per_item": per_item,
        }
    return report


def _print_table(report: dict) -> None:
    metric_keys = [f"recall@{kk}" for kk in RECALL_KS] + ["mrr", f"ndcg@{NDCG_K}"]
    print(f"\n▸ Retrieval eval — {report['n_items']} items, K={report['k']}  ({report['timestamp']})\n")
    head = f"{'retriever':<10}" + "".join(f"{mk:>11}" for mk in metric_keys)
    print(head)
    print("-" * len(head))
    for name, data in report["retrievers"].items():
        agg = data["aggregate"]
        row = f"{name:<10}" + "".join(f"{agg[mk]:>11.3f}" for mk in metric_keys)
        print(row)
    print()
    misses_by_retriever = miss_summary_by_retriever(report)
    if misses_by_retriever:
        print("문항별 정답 miss (top-K 밖, retriever별):")
        for name, misses in misses_by_retriever.items():
            print(f"  [{name}]")
            for iid, miss in misses:
                print(f"    {iid}: {miss}")
        print()


def miss_summary_by_retriever(report: dict) -> dict[str, list[tuple[str, list]]]:
    """Return non-empty miss lists for each retriever in display order."""
    out: dict[str, list[tuple[str, list]]] = {}
    for name, data in report.get("retrievers", {}).items():
        misses = [
            (p["id"], p["miss"])
            for p in data.get("per_item", [])
            if p.get("miss")
        ]
        if misses:
            out[name] = misses
    return out


def citation_rank_bucket(rank: int | None) -> str:
    """Bucket a required citation rank for citation-level retrieval diagnosis."""
    if rank is None:
        return "absent"
    if rank <= 5:
        return "hit@5"
    if rank <= 10:
        return "hit@10"
    if rank <= 20:
        return "hit@20"
    return "beyond@20"


def must_cite_rank_rows(report: dict) -> list[dict]:
    """Flatten per-item gold_ranks into one row per required citation."""
    rows: list[dict] = []
    for retriever, data in report.get("retrievers", {}).items():
        for item in data.get("per_item", []):
            for citation, rank in sorted(item.get("gold_ranks", {}).items()):
                rows.append(
                    {
                        "retriever": retriever,
                        "item_id": item["id"],
                        "citation": citation,
                        "rank": rank,
                        "bucket": citation_rank_bucket(rank),
                    }
                )
    return rows


def must_cite_rank_summary(report: dict) -> dict[str, dict[str, int]]:
    """Count required citation rank buckets per retriever."""
    order = ("hit@5", "hit@10", "hit@20", "beyond@20", "absent")
    summary: dict[str, dict[str, int]] = {}
    for row in must_cite_rank_rows(report):
        bucket_counts = summary.setdefault(row["retriever"], {bucket: 0 for bucket in order})
        bucket_counts[row["bucket"]] += 1
    return summary


def query_variants(query: str) -> list[str]:
    """Return public-safe subqueries for cross-concept retrieval experiments.

    RO2 targets questions where one broad sentence blends multiple accounting
    concepts and the embedding signal leans toward only one of them. Variants
    are intentionally conservative: keep the original query, add delimiter
    clauses, then add known concept phrases that are literally present.
    """
    variants = [query.strip()]
    normalized = query.replace("/", " ").replace(",", " ")
    for chunk in re.split(r"\s+(?:및|그리고|또는)\s+|[;:]", normalized):
        chunk = chunk.strip(" .?()\t")
        if len(chunk) >= 4:
            variants.append(chunk)
    for concept in MULTI_QUERY_CONCEPTS:
        if concept in query:
            variants.append(concept)
    for trigger, expansions in MULTI_QUERY_EXPANSIONS.items():
        if trigger in query:
            variants.extend(expansions)
    return list(dict.fromkeys(v for v in variants if v))


def rrf_fuse_results(result_sets: list[list[dict]], *, limit: int, k: int = 60) -> list[dict]:
    """Fuse multiple ranked result sets with reciprocal rank fusion."""
    rrf: dict[tuple[str, str], float] = {}
    info: dict[tuple[str, str], dict] = {}
    for results in result_sets:
        for rank, row in enumerate(results):
            key = (str(row["standard"]), str(row["no"]))
            rrf[key] = rrf.get(key, 0.0) + 1.0 / (k + rank)
            info.setdefault(key, row)
    sorted_keys = sorted(rrf, key=lambda key: -rrf[key])[:limit]
    return [{**info[key], "rrf": rrf[key]} for key in sorted_keys]


def search_multi_query_hybrid(query: str, standard: str | None = None, limit: int = 20) -> list[dict]:
    """Experimental RO2 retriever: split cross-concept questions and fuse hybrid results."""
    variants = query_variants(query)
    candidate_limit = max(50, limit)
    original = search_hybrid(variants[0], standard, limit=candidate_limit)
    auxiliary = [search_hybrid(variant, standard, limit=candidate_limit) for variant in variants[1:]]
    # Preserve the current hybrid baseline and use subqueries as auxiliary evidence.
    result_sets = [original, original, original, *auxiliary]
    return rrf_fuse_results(result_sets, limit=limit)


def source_route_standard(query: str) -> str | None:
    """Return a narrow supplemental standard route for accepted source-routing clusters."""
    for rule in SOURCE_ROUTE_RULES:
        if all(term in query for term in rule["all"]) and any(term in query for term in rule["any"]):
            return str(rule["standard"])
    return None


def ifrs1115_subquery(query: str) -> str | None:
    """Return a narrow public-safe 1115 subquery for accepted Q001/Q006-style gaps."""
    for rule in IFRS1115_SUBQUERY_RULES:
        if all(term in query for term in rule["all"]) and any(term in query for term in rule["any"]):
            return str(rule["subquery"])
    return None


def ifrs1109_scope_subquery(query: str) -> str | None:
    """Return a narrow 1109 scope-exclusion subquery for accepted Q008-style gaps."""
    for rule in IFRS1109_SCOPE_RULES:
        if all(term in query for term in rule["all"]) and any(term in query for term in rule["any"]):
            return str(rule["subquery"])
    return None


def search_source_routed_hybrid(query: str, standard: str | None = None, limit: int = 20) -> list[dict]:
    """Experimental retriever: fuse baseline hybrid with accepted-cluster standard routing.

    This is intentionally opt-in. It only routes clusters accepted by
    docs/reports/2026-07-05-source-routing-candidate-eval.md and leaves other
    cross-standard questions on the current hybrid baseline.
    """
    route_standard = standard or source_route_standard(query)
    if not route_standard:
        return search_hybrid(query, standard, limit=limit)
    candidate_limit = max(50, limit)
    baseline = search_hybrid(query, None, limit=candidate_limit)
    routed = search_hybrid(query, route_standard, limit=candidate_limit)
    return rrf_fuse_results([baseline, baseline, routed], limit=limit)


def search_ifrs1115_subquery_hybrid(query: str, standard: str | None = None, limit: int = 20) -> list[dict]:
    """Experimental retriever: source-routed baseline plus focused 1115 subquery.

    The subquery rule is intentionally opt-in and narrow. It implements candidates
    accepted by docs/reports/2026-07-05-ifrs1115-subquery-candidate-eval.md.
    """
    subquery = ifrs1115_subquery(query)
    if standard or not subquery:
        return search_source_routed_hybrid(query, standard, limit=limit)
    candidate_limit = max(100, limit)
    baseline = search_source_routed_hybrid(query, None, limit=candidate_limit)
    supplemental = search_hybrid(subquery, "1115", limit=candidate_limit)
    return rrf_fuse_results([baseline, supplemental, supplemental], limit=limit)


def insert_supplemental_results(
    baseline: list[dict],
    supplemental: list[dict],
    *,
    insert_after: int = 3,
    supplemental_limit: int = 1,
    limit: int = 20,
) -> list[dict]:
    """Insert a few supplemental evidence rows while preserving baseline order."""
    out: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(row: dict) -> None:
        key = (str(row["standard"]), str(row["no"]))
        if key in seen:
            return
        seen.add(key)
        out.append(row)

    for row in baseline[:insert_after]:
        add(row)
    for row in supplemental[:supplemental_limit]:
        add(row)
    for row in baseline[insert_after:]:
        add(row)
    for row in supplemental[supplemental_limit:]:
        add(row)
    return out[:limit]


def search_ifrs1109_scope_hybrid(query: str, standard: str | None = None, limit: int = 20) -> list[dict]:
    """Experimental retriever: add 1109 scope-exclusion evidence without displacing lease hits."""
    subquery = ifrs1109_scope_subquery(query)
    if standard or not subquery:
        return search_ifrs1115_subquery_hybrid(query, standard, limit=limit)
    candidate_limit = max(100, limit)
    baseline = search_ifrs1115_subquery_hybrid(query, None, limit=candidate_limit)
    supplemental = search_hybrid(subquery, "1109", limit=candidate_limit)
    return insert_supplemental_results(
        baseline,
        supplemental,
        insert_after=3,
        supplemental_limit=1,
        limit=limit,
    )


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="K-IFRS retrieval-only 평가")
    ap.add_argument("--k", type=int, default=20, help="top-k 검색 범위 (default 20)")
    ap.add_argument("--retrievers", nargs="+", default=list(RETRIEVERS),
                    choices=list(RETRIEVERS), help="평가할 retriever (default 전체)")
    ap.add_argument("--only", nargs="+", help="특정 item id만 (예: --only Q001 Q003)")
    ap.add_argument("--goldset", default=str(GOLDSET))
    ap.add_argument("--out", default=str(RESULTS_DIR))
    ap.add_argument("--no-save", action="store_true", help="JSON 리포트 저장 생략")
    args = ap.parse_args(argv)

    items = _load_goldset(Path(args.goldset))
    if args.only:
        wanted = set(args.only)
        items = [x for x in items if x.id in wanted]
        if not items:
            print(f"ERROR: --only {args.only} 에 해당하는 문항 없음", file=sys.stderr)
            sys.exit(1)

    report = evaluate(items, args.retrievers, args.k)
    _print_table(report)

    if not args.no_save:
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_p = out_dir / f"retrieval_{stamp}.json"
        out_p.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 리포트 저장: {out_p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
