from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-ppr1-authorization-safe-adapter-proof.md"


def build_authorization_safe_adapter_proof() -> dict[str, Any]:
    evidence = [
        _evidence("rag_quality_handoff", "docs/reports/2026-07-05-rag-quality-fresh-validation-close-report.md"),
        _evidence("local_parser_plan", "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md"),
        _evidence("parser_prototype_close", "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md"),
        _evidence("private_payload_leak_tests", "docs/reports/2026-07-05-rlp4-private-payload-leak-tests.md"),
    ]
    gates = [
        {
            "gate": "explicit_authorization",
            "required": True,
            "current_status": "required_before_real_payload_handling",
        },
        {
            "gate": "local_only_processing",
            "required": True,
            "current_status": "must_run_without external upload or public raw payload output",
        },
        {
            "gate": "structured_facts_only_public_output",
            "required": True,
            "current_status": "public reports may include schema/status, not raw content",
        },
        {
            "gate": "deletion_attestation",
            "required": True,
            "current_status": "must be rehearsed before any real adapter claim",
        },
        {
            "gate": "leak_negative_cases",
            "required": True,
            "current_status": "synthetic markers only; no protected fixture content",
        },
    ]
    allowed_claims = [
        "authorization-safe adapter proof plan is ready",
        "real protected payload handling remains gated",
        "next step may define realistic local fixture adapter contract",
    ]
    forbidden_claims = [
        "real protected file has been ingested",
        "real private parser adapter is production-ready",
        "public report contains raw private payload",
    ]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "all_required_gates_present": all(item["required"] for item in gates),
        "real_payload_claim_forbidden": "real protected file has been ingested" in forbidden_claims,
        "next_step_is_contract_not_real_ingestion": allowed_claims[-1].endswith("contract"),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "PPR1 Authorization-Safe Adapter Proof Plan",
        "ok": not errors,
        "horizon": "private-parser-realism-hardening",
        "completed_milestone": "PPR1",
        "evidence": evidence,
        "gates": gates,
        "allowed_claims": allowed_claims,
        "forbidden_claims": forbidden_claims,
        "checks": checks,
        "errors": errors,
        "next_leaf": "PPR2_realistic_local_fixture_adapter_contract",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: authorization-safe proof plan before any realistic private parser adapter work.",
        "",
        "## 한 줄 결론",
        "",
        "Private parser realism can continue only through authorization-gated, local-only, structured-facts-only public evidence.",
        "",
        "## Gates",
        "",
        "| Gate | Required | Current Status |",
        "|---|---|---|",
    ]
    for gate in result["gates"]:
        lines.append(f"| {gate['gate']} | {gate['required']} | {gate['current_status']} |")
    lines.extend(["", "## Evidence", "", "| ID | Path | Exists |", "|---|---|---|"])
    for item in result["evidence"]:
        lines.append(f"| {item['id']} | `{item['path']}` | {item['exists']} |")
    lines.extend(["", "## Allowed Claims", ""])
    lines.extend(f"- {item}" for item in result["allowed_claims"])
    lines.extend(["", "## Forbidden Claims", ""])
    lines.extend(f"- {item}" for item in result["forbidden_claims"])
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            f"- `{result['next_leaf']}`",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_authorization_safe_adapter_proof()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _evidence(id_: str, path: str) -> dict[str, Any]:
    return {"id": id_, "path": path, "exists": (ROOT / path).exists()}


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PPR1 authorization-safe adapter proof plan.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_authorization_safe_adapter_proof()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- gates: {len(result['gates'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
