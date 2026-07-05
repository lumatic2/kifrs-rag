from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rlp1-parser-prototype-asset-inventory.md"


@dataclass(frozen=True)
class ParserPrototypeAsset:
    asset_id: str
    path: str
    category: str
    stage: str
    reusable_for: list[str]
    gap_to_next: str
    exists: bool


def build_inventory() -> dict[str, Any]:
    asset_specs = [
        (
            "local-parser-module",
            "kifrs/feedback/local_parser.py",
            "core_module",
            "prototype_contract",
            ["RLP2", "RLP3", "RLP4", "RLP5"],
            "Needs a more realistic local fixture adapter instead of only synthetic dry-run handoff.",
        ),
        (
            "case-intake-module",
            "kifrs/feedback/case_intake.py",
            "core_module",
            "intake_redaction_deletion",
            ["RLP2", "RLP3", "RLP4", "RLP5"],
            "Needs product-level leak tests around every parser-facing public artifact.",
        ),
        (
            "upload-storage-policy",
            "docs/reports/2026-07-05-cpu1-client-private-upload-storage-policy.md",
            "policy",
            "completed_prior_asset",
            ["RLP3", "RLP5"],
            "Policy exists, but RLP still needs a close gate tying policy to the prototype flow.",
        ),
        (
            "parser-dry-run-fixture",
            "docs/reports/2026-07-05-pdf1-private-parser-dry-run-fixture.md",
            "fixture",
            "completed_prior_asset",
            ["RLP2", "RLP4"],
            "Fixture exists, but RLP2 needs a fixture-like adapter path that emits review questions.",
        ),
        (
            "deletion-attestation-gate",
            "docs/reports/2026-07-05-lda1-local-deletion-attestation-gate.md",
            "deletion_gate",
            "completed_prior_asset",
            ["RLP3", "RLP5"],
            "Attestation exists, but deletion automation is still simulated/manual.",
        ),
        (
            "local-parser-close-gate",
            "docs/reports/2026-07-05-cpl1-client-private-local-parser-close-gate.md",
            "close_gate",
            "completed_prior_asset",
            ["RLP5"],
            "Prior close gate proves readiness, not the new RLP prototype sequence.",
        ),
        (
            "prototype-spike",
            "docs/reports/2026-07-05-lpp1-local-parser-prototype-spike.md",
            "prototype",
            "completed_prior_asset",
            ["RLP2"],
            "Prototype spike needs to be wrapped by a reusable local fixture adapter.",
        ),
        (
            "adapter-contract",
            "docs/reports/2026-07-05-lpa1-local-parser-adapter-contract.md",
            "adapter_contract",
            "completed_prior_asset",
            ["RLP2", "RLP4"],
            "Contract exists, but RLP2 needs adapter output with structured facts plus review questions.",
        ),
        (
            "adapter-dry-run-gate",
            "docs/reports/2026-07-05-lpad1-local-parser-adapter-dry-run-gate.md",
            "adapter_gate",
            "completed_prior_asset",
            ["RLP2", "RLP5"],
            "Dry-run gate exists, but RLP needs a horizon-specific close gate.",
        ),
        (
            "adapter-scaffold",
            "docs/reports/2026-07-05-lpas1-local-parser-adapter-scaffold.md",
            "adapter_scaffold",
            "completed_prior_asset",
            ["RLP2"],
            "Scaffold exists, but a real local parser adapter is still deferred.",
        ),
        (
            "operator-runbook",
            "docs/reports/2026-07-05-lpor1-local-parser-operator-runbook.md",
            "operator_runbook",
            "completed_prior_asset",
            ["RLP5"],
            "Runbook exists, but operator UX hardening remains a later horizon.",
        ),
        (
            "real-adapter-decision-gate",
            "docs/reports/2026-07-05-lprd1-local-parser-real-adapter-decision-gate.md",
            "decision_gate",
            "completed_prior_asset",
            ["RLP2", "RLP5"],
            "Real adapter remains deferred until explicit local-only private-file authorization.",
        ),
        (
            "real-adapter-implementation-plan",
            "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md",
            "implementation_plan",
            "completed_prior_asset",
            ["RLP2", "RLP5"],
            "Implementation plan exists, but RLP should not introduce real private files.",
        ),
        (
            "parser-runtime-close-report",
            "docs/reports/2026-07-05-client-private-parser-runtime-close-report.md",
            "runtime_close",
            "completed_prior_asset",
            ["RLP5"],
            "Runtime close is prior evidence; RLP needs a new prototype close result.",
        ),
    ]
    assets = [
        ParserPrototypeAsset(
            asset_id=asset_id,
            path=path,
            category=category,
            stage=stage,
            reusable_for=list(reusable_for),
            gap_to_next=gap_to_next,
            exists=(ROOT / path).exists(),
        )
        for asset_id, path, category, stage, reusable_for, gap_to_next in asset_specs
    ]
    missing = [asset.path for asset in assets if not asset.exists]
    rlp_gaps = {
        "RLP2": "Build a local-safe fixture adapter that turns fixture-like input into structured facts and review questions.",
        "RLP3": "Simulate deletion states and block close when retention/deletion attestation is incomplete.",
        "RLP4": "Add product-level leak tests for parser outputs and generated reports.",
        "RLP5": "Tie RLP1 through RLP4 into a close gate with carried trust/runtime evidence.",
    }
    return {
        "title": "RLP1 Parser Prototype Asset Inventory",
        "ok": not missing,
        "active_horizon": "real-local-parser-prototype",
        "completed_milestone": "RLP1",
        "next_milestone": "RLP2",
        "assets": [asdict(asset) for asset in assets],
        "missing_assets": missing,
        "rlp_gaps": rlp_gaps,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    lines = [
        f"# {inventory['title']}",
        "",
        "> Scope: inventory reusable parser/runtime assets before implementing the local parser prototype path.",
        "",
        "## Result",
        "",
        f"- ok: {inventory['ok']}",
        f"- active horizon: `{inventory['active_horizon']}`",
        f"- completed milestone: `{inventory['completed_milestone']}`",
        f"- next milestone: `{inventory['next_milestone']}`",
        "",
        "## Asset Inventory",
        "",
        "| Asset | Category | Stage | Path | Reusable For | Gap |",
        "|---|---|---|---|---|---|",
    ]
    for asset in inventory["assets"]:
        reusable_for = ", ".join(asset["reusable_for"])
        lines.append(
            f"| {asset['asset_id']} | {asset['category']} | {asset['stage']} | `{asset['path']}` | {reusable_for} | {asset['gap_to_next']} |"
        )
    lines.extend(["", "## RLP2-RLP5 Gaps", ""])
    for milestone, gap in inventory["rlp_gaps"].items():
        lines.append(f"- {milestone}: {gap}")
    lines.extend(["", "## Missing Assets", ""])
    if inventory["missing_assets"]:
        lines.extend(f"- `{path}`" for path in inventory["missing_assets"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- RLP1 does not implement a parser adapter.",
            "- RLP1 does not introduce real client files, OCR, private embeddings, protected source text, or raw private payload.",
            "- RLP1 only fixes the asset map and next gaps for RLP2 through RLP5.",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(inventory, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    inventory = build_inventory()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(inventory), encoding="utf-8")
    return inventory


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory local parser prototype assets for RLP1.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    inventory = write_report(args.out) if args.write else build_inventory()
    if args.format == "json":
        print(json.dumps(inventory, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(inventory), end="")
    else:
        print(inventory["title"])
        print(f"- ok: {inventory['ok']}")
        print(f"- assets: {len(inventory['assets'])}")
        print(f"- missing: {len(inventory['missing_assets'])}")
        print(f"- next milestone: {inventory['next_milestone']}")
    if not inventory["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
