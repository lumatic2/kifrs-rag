from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.rag_quality_final_gate import (  # noqa: E402
    BASELINE_RETRIEVER,
    TARGET_RETRIEVER,
    build_report as build_rag_quality_report,
)
from scripts.accounting_intelligence_gap_audit import build_gap_audit  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-odv1-opt-in-retriever-demo-validation.md"


def build_demo_validation() -> dict[str, Any]:
    quality = build_rag_quality_report()
    gap_audit = build_gap_audit()
    failures: list[str] = []

    if quality["ok"] is not True:
        failures.append("rag_quality_final_gate did not pass")
    if quality["target_recall20"] < 1.0:
        failures.append(f"{TARGET_RETRIEVER} recall@20 is below 1.000")
    if quality["target_buckets"]["absent"] != 0:
        failures.append(f"{TARGET_RETRIEVER} still has absent citations")
    if quality["target_misses"]:
        failures.append(f"{TARGET_RETRIEVER} still has misses")
    if not any(
        "opt-in retriever" in gap and "deferred" in gap for gap in gap_audit.remaining_gaps
    ):
        failures.append("gap audit does not expose default promotion boundary")
    expected_next_leaf = "RAG reliability revalidation RR2/RR3/RR5, then explicit authorization before default retriever change"

    return {
        "ok": not failures,
        "errors": failures,
        "baseline_retriever": BASELINE_RETRIEVER,
        "target_retriever": TARGET_RETRIEVER,
        "items": quality["n_items"],
        "k": quality["k"],
        "baseline_recall20": quality["baseline_recall20"],
        "target_recall20": quality["target_recall20"],
        "baseline_buckets": quality["baseline_buckets"],
        "target_buckets": quality["target_buckets"],
        "target_misses": quality["target_misses"],
        "default_promotion": "deferred",
        "demo_ready_for_opt_in": quality["ok"] and not quality["target_misses"],
        "gap_audit_remaining_gaps": gap_audit.remaining_gaps,
        "gap_audit_next_leaf": gap_audit.next_leaf,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": expected_next_leaf,
    }


def render_report(payload: dict[str, Any]) -> str:
    lines = [
        "# ODV1 Opt-In Retriever Demo Validation",
        "",
        "> Scope: prove the final opt-in retriever stack is demo-ready without promoting it to the default retriever.",
        "",
        "## 한 줄 결론",
        "",
        (
            f"`{payload['target_retriever']}` is ready for opt-in demo use: "
            f"50-item recall@20 is {payload['target_recall20']:.3f} and required-citation absent count is "
            f"{payload['target_buckets']['absent']}. Default retriever promotion remains deferred."
        ),
        "",
        "## Retrieval Result",
        "",
        "| Retriever | recall@20 | absent required citations | top-20 misses |",
        "|---|---:|---:|---:|",
        (
            f"| `{payload['baseline_retriever']}` | {payload['baseline_recall20']:.3f} | "
            f"{payload['baseline_buckets']['absent']} | n/a |"
        ),
        (
            f"| `{payload['target_retriever']}` | {payload['target_recall20']:.3f} | "
            f"{payload['target_buckets']['absent']} | {len(payload['target_misses'])} |"
        ),
        "",
        "## Demo Boundary",
        "",
        "- Use the target retriever only as an opt-in demo/evaluation path.",
        "- Keep the default retriever unchanged until stronger internal evaluation evidence and explicit authorization support promotion.",
        "- Treat this as retrieval evidence, not answer-quality proof or final accounting judgment.",
        "",
        "## Gap-Audit Check",
        "",
        f"- gap-audit next leaf: {payload['gap_audit_next_leaf']}",
        "- gap audit still exposes the default-promotion boundary.",
        "",
        "## Next Leaf",
        "",
        str(payload["next_leaf"]),
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        "```",
    ]
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    payload = build_demo_validation()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(payload), encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate opt-in retriever readiness for demo use.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    payload = write_report() if args.write else build_demo_validation()
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(payload), end="")
    else:
        print(f"ok: {payload['ok']}")
        print(f"baseline_retriever: {payload['baseline_retriever']}")
        print(f"target_retriever: {payload['target_retriever']}")
        print(f"baseline_recall@20: {payload['baseline_recall20']:.3f}")
        print(f"target_recall@20: {payload['target_recall20']:.3f}")
        print(f"target_absent: {payload['target_buckets']['absent']}")
        print(f"default_promotion: {payload['default_promotion']}")
        print(f"next_leaf: {payload['next_leaf']}")
        for error in payload["errors"]:
            print(f"- {error}")

    if not payload["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
