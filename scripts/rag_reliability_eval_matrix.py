from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.eval.harness import load_goldset  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rr2-eval-matrix.md"

KNOWLEDGE_NODES = [
    "rag-evaluation-metrics",
    "rag-retrieval-rank-debugging-playbook",
    "rag-retrieval-strategy",
    "rag-reranking-strategy",
]

BUCKET_METHOD_METRICS = {
    "direct_standard_lookup": ["context_recall", "citation_hit_rate", "latency"],
    "judgment_paragraph_combination": ["faithfulness", "answer_relevance", "context_recall", "citation_coverage"],
    "workflow_seed_question": ["answer_relevance", "faithfulness", "global_rules", "needs_human_review_boundary"],
    "disclosure_question": ["context_precision", "context_recall", "citation_coverage"],
    "term_bridge_or_exam_convention_dependent": ["context_recall", "term_bridge_hit", "faithfulness"],
}


def build_eval_matrix() -> dict[str, Any]:
    items = load_goldset()
    rows = [_classify_item(item) for item in items]
    bucket_counts = Counter(bucket for row in rows for bucket in row["buckets"])
    standards = sorted({standard for row in rows for standard in row["standards"]})
    coverage_gaps = _coverage_gaps(bucket_counts)
    return {
        "ok": not coverage_gaps,
        "title": "RR2 Eval Matrix and Seed Coverage",
        "milestone": "RR2",
        "methodology_nodes": KNOWLEDGE_NODES,
        "item_count": len(rows),
        "standards": standards,
        "bucket_counts": dict(sorted(bucket_counts.items())),
        "coverage_gaps": coverage_gaps,
        "metric_policy": BUCKET_METHOD_METRICS,
        "public_safe_matrix": rows,
        "protected_fields_excluded": ["question", "source_ref", "notes", "raw answer body"],
        "rr3_input": {
            "needed": "retrieval and citation diagnostics by bucket",
            "compare": ["hybrid", "ifrs1109_classification_hybrid"],
            "metrics": ["recall@k", "MRR", "nDCG@10", "required-citation rank bucket", "target misses"],
        },
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(matrix: dict[str, Any]) -> str:
    lines = [
        "# RR2 Eval Matrix and Seed Coverage",
        "",
        "> Scope: public-safe eval coverage matrix for K-IFRS RAG reliability revalidation.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(matrix),
        "",
        "## Methodology Source",
        "",
        "Knowledge-graph nodes used:",
    ]
    lines.extend(f"- `{node}`" for node in matrix["methodology_nodes"])
    lines.extend(
        [
            "",
            "Applied rule: compare RAG variants on a stable golden set, separating retrieval/citation metrics from answer metrics such as faithfulness, answer relevance, context precision, context recall, latency, and cost.",
            "",
            "## Coverage Summary",
            "",
            f"- Items: {matrix['item_count']}",
            f"- Standards covered: {', '.join(matrix['standards'])}",
            "",
            "| Bucket | Count | Metric Focus |",
            "|---|---:|---|",
        ]
    )
    for bucket, metrics in matrix["metric_policy"].items():
        lines.append(f"| {bucket} | {matrix['bucket_counts'].get(bucket, 0)} | {', '.join(metrics)} |")
    lines.extend(
        [
            "",
            "## Public-Safe Item Matrix",
            "",
            "| ID | Source | Standards | Must Cite Count | May Cite Count | Keyword Count | Buckets |",
            "|---|---|---|---:|---:|---:|---|",
        ]
    )
    for row in matrix["public_safe_matrix"]:
        lines.append(
            "| {id} | {source} | {standards} | {must} | {may} | {keywords} | {buckets} |".format(
                id=row["id"],
                source=row["source"],
                standards=", ".join(row["standards"]),
                must=row["must_cite_count"],
                may=row["may_cite_count"],
                keywords=row["keyword_count"],
                buckets=", ".join(row["buckets"]),
            )
        )
    lines.extend(
        [
            "",
            "## Coverage Gaps",
            "",
        ]
    )
    if matrix["coverage_gaps"]:
        lines.extend(f"- {gap}" for gap in matrix["coverage_gaps"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## RR3 Input",
            "",
            f"- Needed: {matrix['rr3_input']['needed']}",
            f"- Compare: {', '.join(matrix['rr3_input']['compare'])}",
            f"- Metrics: {', '.join(matrix['rr3_input']['metrics'])}",
            "",
            "## Excluded Protected Fields",
            "",
        ]
    )
    lines.extend(f"- {field}" for field in matrix["protected_fields_excluded"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(matrix, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    matrix = build_eval_matrix()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(matrix), encoding="utf-8")
    return matrix


def _classify_item(item: Any) -> dict[str, Any]:
    text = " ".join(
        [
            item.source,
            item.source_ref,
            item.question,
            " ".join(item.keywords),
            item.notes,
        ]
    )
    buckets: list[str] = []
    if len(item.must_cite) <= 1 and not _contains_any(text, ["판단", "분류", "측정", "수행의무", "리스", "공시"]):
        buckets.append("direct_standard_lookup")
    if len(item.must_cite) > 1 or _contains_any(text, ["판단", "분류", "측정", "인식", "구별", "SPPI", "리스"]):
        buckets.append("judgment_paragraph_combination")
    if _contains_any(text, ["분개", "검토메모", "review pack", "workflow", "계산", "회계처리"]):
        buckets.append("workflow_seed_question")
    if _contains_any(text, ["공시", "주석", "표시", "재무제표"]):
        buckets.append("disclosure_question")
    if item.source in {"cpa-1", "cpa-2", "textbook"} or _contains_any(
        text,
        ["user_note", "source pack", "공매도", "상법", "자본시장법", "무상증자", "결산배당"],
    ):
        buckets.append("term_bridge_or_exam_convention_dependent")
    if not buckets:
        buckets.append("direct_standard_lookup")
    return {
        "id": item.id,
        "source": item.source,
        "standards": sorted({cite.standard for cite in [*item.must_cite, *item.may_cite]}),
        "must_cite_count": len(item.must_cite),
        "may_cite_count": len(item.may_cite),
        "keyword_count": len(item.keywords),
        "buckets": sorted(set(buckets)),
    }


def _coverage_gaps(bucket_counts: Counter[str]) -> list[str]:
    gaps: list[str] = []
    for bucket in BUCKET_METHOD_METRICS:
        if bucket_counts.get(bucket, 0) == 0:
            gaps.append(f"missing bucket: {bucket}")
    if bucket_counts.get("direct_standard_lookup", 0) < 5:
        gaps.append("direct standard lookup has fewer than 5 items")
    if bucket_counts.get("judgment_paragraph_combination", 0) < 10:
        gaps.append("judgment and paragraph-combination bucket has fewer than 10 items")
    return gaps


def _contains_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle.lower() in lowered for needle in needles)


def _one_line_conclusion(matrix: dict[str, Any]) -> str:
    if matrix["coverage_gaps"]:
        return "The goldset is usable but not coverage-complete; RR3 should diagnose retrieval by bucket and RR2 should add missing seed classes later."
    return "The goldset covers the required RAG evaluation buckets; RR3 can proceed to retrieval and citation diagnostics by bucket."


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render RR2 RAG eval matrix and seed coverage.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    matrix = write_report(args.out) if args.write else build_eval_matrix()
    if args.format == "json":
        print(json.dumps(matrix, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(matrix), end="")
    else:
        print(matrix["title"])
        print(f"- ok: {matrix['ok']}")
        print(f"- items: {matrix['item_count']}")
        print(f"- buckets: {matrix['bucket_counts']}")
        print(f"- coverage_gaps: {matrix['coverage_gaps']}")
        print(f"- report_path: {matrix['report_path']}")


if __name__ == "__main__":
    main()
