from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.eval.retrieval import (  # noqa: E402
    citation_rank_bucket,
    evaluate,
    must_cite_rank_summary,
)
from scripts.rag_quality_final_gate import (  # noqa: E402
    BASELINE_RETRIEVER,
    DEFAULT_GOLDSET,
    DEFAULT_K,
    TARGET_RETRIEVER,
)
from scripts.rag_reliability_eval_matrix import build_eval_matrix  # noqa: E402
from kifrs.eval.harness import load_goldset  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rr3-retrieval-citation-diagnostics.md"


def build_diagnostics(*, goldset: Path = DEFAULT_GOLDSET, k: int = DEFAULT_K) -> dict[str, Any]:
    items = load_goldset(goldset)
    retrieval_report = evaluate(items, [BASELINE_RETRIEVER, TARGET_RETRIEVER], k)
    eval_matrix = build_eval_matrix()
    item_buckets = {row["id"]: row["buckets"] for row in eval_matrix["public_safe_matrix"]}

    transition_rows = _citation_transition_rows(retrieval_report, item_buckets)
    bucket_summary = _bucket_summary(transition_rows)
    item_summary = _item_summary(retrieval_report, item_buckets)
    target_misses = [
        {
            "id": row["id"],
            "buckets": item_buckets.get(row["id"], []),
            "miss_count": len(row["miss"]),
            "miss_citations": row["miss"],
        }
        for row in retrieval_report["retrievers"][TARGET_RETRIEVER]["per_item"]
        if row["miss"]
    ]
    baseline_misses = [
        row
        for row in retrieval_report["retrievers"][BASELINE_RETRIEVER]["per_item"]
        if row["miss"]
    ]
    recovered_items = sorted(
        {
            row["id"]
            for row in baseline_misses
            if not next(
                target_row["miss"]
                for target_row in retrieval_report["retrievers"][TARGET_RETRIEVER]["per_item"]
                if target_row["id"] == row["id"]
            )
        }
    )
    failures = []
    if target_misses:
        failures.append(f"{TARGET_RETRIEVER} still has top-{k} misses")
    return {
        "ok": not failures,
        "title": "RR3 Retrieval and Citation Diagnostics",
        "milestone": "RR3",
        "k": k,
        "retrievers": [BASELINE_RETRIEVER, TARGET_RETRIEVER],
        "retrieval_aggregate": {
            name: retrieval_report["retrievers"][name]["aggregate"]
            for name in [BASELINE_RETRIEVER, TARGET_RETRIEVER]
        },
        "citation_rank_summary": must_cite_rank_summary(retrieval_report),
        "bucket_summary": bucket_summary,
        "item_summary": item_summary,
        "target_misses": target_misses,
        "recovered_item_ids": recovered_items,
        "failure_taxonomy": _failure_taxonomy(transition_rows, target_misses),
        "protected_fields_excluded": ["question", "source_ref", "notes", "answer body", "paragraph body"],
        "errors": failures,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(diagnostics: dict[str, Any]) -> str:
    lines = [
        "# RR3 Retrieval and Citation Diagnostics",
        "",
        "> Scope: public-safe bucket-level retrieval/citation comparison between default and opt-in K-IFRS retrievers.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(diagnostics),
        "",
        "## Retrieval Aggregate",
        "",
        "| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, aggregate in diagnostics["retrieval_aggregate"].items():
        lines.append(
            "| `{name}` | {r1:.3f} | {r3:.3f} | {r5:.3f} | {r10:.3f} | {r20:.3f} | {mrr:.3f} | {ndcg:.3f} |".format(
                name=name,
                r1=aggregate["recall@1"],
                r3=aggregate["recall@3"],
                r5=aggregate["recall@5"],
                r10=aggregate["recall@10"],
                r20=aggregate["recall@20"],
                mrr=aggregate["mrr"],
                ndcg=aggregate["ndcg@10"],
            )
        )
    lines.extend(
        [
            "",
            "## Required-Citation Rank Buckets",
            "",
            "| Retriever | hit@5 | hit@10 | hit@20 | beyond@20 | absent |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for name, summary in diagnostics["citation_rank_summary"].items():
        lines.append(
            f"| `{name}` | {summary['hit@5']} | {summary['hit@10']} | {summary['hit@20']} | {summary['beyond@20']} | {summary['absent']} |"
        )
    lines.extend(
        [
            "",
            "## Bucket Diagnostics",
            "",
            "| Eval Bucket | Citations | Recovered | Still Absent | Target Worse | Target Hit@20 |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for bucket, summary in diagnostics["bucket_summary"].items():
        lines.append(
                "| {bucket} | {citations} | {recovered} | {still_absent} | {target_worse} | {target_hit20} |".format(
                    bucket=bucket,
                    citations=summary.get("citations", 0),
                    recovered=summary.get("recovered", 0),
                    still_absent=summary.get("still_absent", 0),
                    target_worse=summary.get("target_worse", 0),
                    target_hit20=summary.get("target_hit20", 0),
                )
            )
    lines.extend(
        [
            "",
            "## Failure Taxonomy",
            "",
        ]
    )
    lines.extend(f"- {key}: {value}" for key, value in diagnostics["failure_taxonomy"].items())
    lines.extend(
        [
            "",
            "## Item Summary",
            "",
            "| ID | Buckets | Baseline Misses | Target Misses | Best Target Bucket |",
            "|---|---|---:|---:|---|",
        ]
    )
    for row in diagnostics["item_summary"]:
        lines.append(
            "| {id} | {buckets} | {baseline_misses} | {target_misses} | {best_target_bucket} |".format(
                id=row["id"],
                buckets=", ".join(row["buckets"]),
                baseline_misses=row["baseline_miss_count"],
                target_misses=row["target_miss_count"],
                best_target_bucket=row["best_target_bucket"],
            )
        )
    lines.extend(
        [
            "",
            "## Target Misses",
            "",
        ]
    )
    if diagnostics["target_misses"]:
        for miss in diagnostics["target_misses"]:
            lines.append(f"- {miss['id']}: {miss['miss_count']} citations missing from target top-{diagnostics['k']}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Excluded Protected Fields",
            "",
        ]
    )
    lines.extend(f"- {field}" for field in diagnostics["protected_fields_excluded"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(diagnostics, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    diagnostics = build_diagnostics()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(diagnostics), encoding="utf-8")
    return diagnostics


def _citation_transition_rows(report: dict[str, Any], item_buckets: dict[str, list[str]]) -> list[dict[str, Any]]:
    baseline_rows = _rank_rows_by_item_citation(report, BASELINE_RETRIEVER)
    target_rows = _rank_rows_by_item_citation(report, TARGET_RETRIEVER)
    out: list[dict[str, Any]] = []
    for key, baseline in sorted(baseline_rows.items()):
        target = target_rows[key]
        item_id, citation = key
        out.append(
            {
                "item_id": item_id,
                "citation": citation,
                "buckets": item_buckets.get(item_id, []),
                "baseline_rank": baseline["rank"],
                "baseline_bucket": baseline["bucket"],
                "target_rank": target["rank"],
                "target_bucket": target["bucket"],
                "transition": _transition(baseline["rank"], target["rank"]),
            }
        )
    return out


def _rank_rows_by_item_citation(report: dict[str, Any], retriever: str) -> dict[tuple[str, str], dict[str, Any]]:
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for item in report["retrievers"][retriever]["per_item"]:
        for citation, rank in item.get("gold_ranks", {}).items():
            rows[(item["id"], citation)] = {
                "rank": rank,
                "bucket": citation_rank_bucket(rank),
            }
    return rows


def _transition(baseline_rank: int | None, target_rank: int | None) -> str:
    if baseline_rank is None and target_rank is not None:
        return "recovered_from_absent"
    if target_rank is None:
        return "still_absent" if baseline_rank is None else "regressed_to_absent"
    if baseline_rank is None:
        return "recovered_from_absent"
    if target_rank < baseline_rank:
        return "rank_improved"
    if target_rank > baseline_rank:
        return "rank_worse"
    return "unchanged"


def _bucket_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    summary: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        for bucket in row["buckets"]:
            summary[bucket]["citations"] += 1
            if row["transition"] in {"recovered_from_absent", "rank_improved"}:
                summary[bucket]["recovered"] += 1
            if row["transition"] in {"still_absent", "regressed_to_absent"}:
                summary[bucket]["still_absent"] += 1
            if row["transition"] in {"rank_worse", "regressed_to_absent"}:
                summary[bucket]["target_worse"] += 1
            if row["target_bucket"] in {"hit@5", "hit@10", "hit@20"}:
                summary[bucket]["target_hit20"] += 1
    return {
        bucket: {
            "citations": counts.get("citations", 0),
            "recovered": counts.get("recovered", 0),
            "still_absent": counts.get("still_absent", 0),
            "target_worse": counts.get("target_worse", 0),
            "target_hit20": counts.get("target_hit20", 0),
        }
        for bucket, counts in sorted(summary.items())
    }


def _item_summary(report: dict[str, Any], item_buckets: dict[str, list[str]]) -> list[dict[str, Any]]:
    baseline = {row["id"]: row for row in report["retrievers"][BASELINE_RETRIEVER]["per_item"]}
    target = {row["id"]: row for row in report["retrievers"][TARGET_RETRIEVER]["per_item"]}
    out = []
    for item_id in sorted(target):
        target_buckets = [
            citation_rank_bucket(rank)
            for rank in target[item_id].get("gold_ranks", {}).values()
        ]
        out.append(
            {
                "id": item_id,
                "buckets": item_buckets.get(item_id, []),
                "baseline_miss_count": len(baseline[item_id]["miss"]),
                "target_miss_count": len(target[item_id]["miss"]),
                "best_target_bucket": _best_bucket(target_buckets),
            }
        )
    return out


def _best_bucket(buckets: list[str]) -> str:
    order = ["hit@5", "hit@10", "hit@20", "beyond@20", "absent"]
    for bucket in order:
        if bucket in buckets:
            return bucket
    return "none"


def _failure_taxonomy(rows: list[dict[str, Any]], target_misses: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(row["transition"] for row in rows)
    counts["target_items_with_misses"] = len(target_misses)
    return dict(sorted(counts.items()))


def _one_line_conclusion(diagnostics: dict[str, Any]) -> str:
    target = diagnostics["retrieval_aggregate"][TARGET_RETRIEVER]
    baseline = diagnostics["retrieval_aggregate"][BASELINE_RETRIEVER]
    return (
        f"`{TARGET_RETRIEVER}` improves recall@20 from {baseline['recall@20']:.3f} to "
        f"{target['recall@20']:.3f}; target top-{diagnostics['k']} required-citation misses: "
        f"{len(diagnostics['target_misses'])}."
    )


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render RR3 retrieval and citation diagnostics.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    diagnostics = write_report(args.out) if args.write else build_diagnostics()
    if args.format == "json":
        print(json.dumps(diagnostics, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(diagnostics), end="")
    else:
        print(diagnostics["title"])
        print(f"- ok: {diagnostics['ok']}")
        print(f"- retrievers: {diagnostics['retrievers']}")
        print(f"- target_misses: {len(diagnostics['target_misses'])}")
        print(f"- recovered_item_ids: {diagnostics['recovered_item_ids']}")
        print(f"- report_path: {diagnostics['report_path']}")
    if not diagnostics["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
