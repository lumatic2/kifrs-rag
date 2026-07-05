from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback.case_intake import (  # noqa: E402
    ClientPrivateDeletionAttestation,
    ClientPrivateParserDryRunFixture,
    RedactedClientPrivateSummary,
    RoutingCandidate,
)
from kifrs.feedback.local_parser import LocalPrivateParserPrototypeResult  # noqa: E402
from kifrs.runtime.client_private_parser import (  # noqa: E402
    client_private_contract_to_authority_reference,
    client_private_contracts_to_authority_boundary,
    contract_from_parser_prototype_result,
)
from kifrs.workflows.kifrs1116.fixtures import FIXTURES  # noqa: E402
from kifrs.workflows.kifrs1116.review_pack import (  # noqa: E402
    generate_review_pack,
    render_review_pack_markdown,
)
from kifrs.workflows.statement_draft import from_1116_review_pack  # noqa: E402
from scripts.client_private_local_parser_adapter_contract_check import (  # noqa: E402
    check_local_parser_adapter_contract,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-cp3-client-private-evidence-adapter.md"


def build_adapter_report() -> dict[str, Any]:
    prototype = _prototype_result(check_local_parser_adapter_contract()["prototype_result"])
    contract = contract_from_parser_prototype_result(prototype)
    reference = client_private_contract_to_authority_reference(contract)
    boundary = client_private_contracts_to_authority_boundary([contract], primary_citations=["[1116-53]"])
    pack = generate_review_pack(FIXTURES[0].txn, authority_boundary=boundary)
    rendered = render_review_pack_markdown(pack)
    candidates = from_1116_review_pack(pack)
    promoted_refs = [
        ref
        for candidate in candidates
        for ref in candidate.evidence_refs
        if ref.get("authority_role") in {"client_private_fact", "primary_kifrs_evidence"}
    ]
    return {
        "title": "CP3 Client-Private Evidence Adapter",
        "ok": reference["authority_role"] == "client_private_fact" and not promoted_refs and _public_safe(rendered),
        "horizon": "client-private-parser-runtime",
        "milestone": "CP3",
        "authority_role": reference["authority_role"],
        "review_pack_has_client_private_fact": bool(pack.authority_boundary.get("client_private_fact")),
        "statement_promoted_refs": len(promoted_refs),
        "public_safe": _public_safe(rendered),
        "next_leaf": "CP4_deletion_and_retention_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['title']}",
        "",
        "> Scope: CP3 adapter from runtime parser contract to client_private_fact authority reference.",
        "",
        "## Result",
        "",
        f"- ok: {report['ok']}",
        f"- horizon: `{report['horizon']}`",
        f"- milestone: `{report['milestone']}`",
        f"- authority role: `{report['authority_role']}`",
        f"- review pack has client-private fact: {report['review_pack_has_client_private_fact']}",
        f"- statement promoted refs: {report['statement_promoted_refs']}",
        f"- public safe: {report['public_safe']}",
        f"- next leaf: `{report['next_leaf']}`",
        "",
        "## Boundary Meaning",
        "",
        "- Parser runtime contract can now become a `client_private_fact` authority reference.",
        "- Review packs can render that reference in the client-private authority section.",
        "- Statement draft amount lines do not consume client-private facts as public fact evidence or primary K-IFRS authority.",
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(report, ensure_ascii=False, indent=2, default=str),
        "```",
    ]
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    report = build_adapter_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(report), encoding="utf-8")
    return report


def _prototype_result(data: dict[str, object]) -> LocalPrivateParserPrototypeResult:
    return LocalPrivateParserPrototypeResult(
        parser_run_id=str(data["parser_run_id"]),
        fixture=ClientPrivateParserDryRunFixture(**data["fixture"]),
        redacted_summary=RedactedClientPrivateSummary(**data["redacted_summary"]),
        route=RoutingCandidate(**data["route"]),
        deletion_attestation=ClientPrivateDeletionAttestation(**data["deletion_attestation"]),
    )


def _public_safe(rendered: str) -> bool:
    forbidden = ("api_key", "token", "source_body", "raw_contract", "contract_body", "full_text")
    return not any(item in rendered for item in forbidden)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Render CP3 client-private evidence adapter report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    report = write_report(args.out) if args.write else build_adapter_report()
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(report), end="")
    else:
        print(report["title"])
        print(f"- ok: {report['ok']}")
        print(f"- authority role: {report['authority_role']}")
        print(f"- next leaf: {report['next_leaf']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
