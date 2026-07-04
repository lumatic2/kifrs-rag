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

# retriever 이름 → (query, limit) → list[dict(standard, no, ...)]
RETRIEVERS = {
    "lexical": lambda q, k: search_fts(q, None, limit=k),
    "semantic": lambda q, k: semantic_search(q, None, limit=k),
    "hybrid": lambda q, k: search_hybrid(q, None, limit=k),
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
