from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROTECTED_PATH_MARKERS = ("data/", "embeddings/", ".db", ".pdf", "dogfood")


@dataclass(frozen=True)
class ReadinessCheck:
    check_id: str
    kind: str
    status: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {
            "check_id": self.check_id,
            "kind": self.kind,
            "status": self.status,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class ReadinessResult:
    manifest_path: Path
    checks: tuple[ReadinessCheck, ...]

    @property
    def ok(self) -> bool:
        return all(check.status in {"PASS", "SKIP"} for check in self.checks)

    @property
    def failed(self) -> tuple[ReadinessCheck, ...]:
        return tuple(check for check in self.checks if check.status == "FAIL")


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_readiness(manifest_path: Path, *, run_commands: bool = True) -> ReadinessResult:
    manifest = load_manifest(manifest_path)
    checks: list[ReadinessCheck] = []

    for artifact in manifest.get("required_artifacts", []):
        artifact_path = str(artifact)
        if _is_protected_artifact(artifact_path):
            checks.append(ReadinessCheck(artifact_path, "artifact", "FAIL", "protected asset cannot be required"))
            continue
        path = ROOT / artifact_path
        checks.append(
            ReadinessCheck(
                artifact_path,
                "artifact",
                "PASS" if path.exists() else "FAIL",
                "exists" if path.exists() else "missing",
            )
        )

    for command in manifest.get("reproduction_commands", []):
        command_id = str(command["id"])
        command_line = str(command["cmd"])
        required = bool(command.get("required", True))
        if not run_commands:
            checks.append(ReadinessCheck(command_id, "command", "SKIP", "command execution disabled"))
            continue
        completed = subprocess.run(
            command_line,
            cwd=ROOT,
            shell=True,
            text=True,
            capture_output=True,
            timeout=120,
        )
        if completed.returncode == 0:
            checks.append(ReadinessCheck(command_id, "command", "PASS", _last_output_line(completed)))
        else:
            status = "FAIL" if required else "SKIP"
            checks.append(ReadinessCheck(command_id, "command", status, _last_output_line(completed)))

    return ReadinessResult(manifest_path=manifest_path, checks=tuple(checks))


def render_readiness_report(result: ReadinessResult) -> str:
    lines = [
        "# Toolkit Readiness Report",
        "",
        f"- Manifest: `{_display_path(result.manifest_path)}`",
        f"- Overall: {'PASS' if result.ok else 'FAIL'}",
        "",
        "## Checks",
        "",
        "| Check | Kind | Status | Detail |",
        "|---|---|---|---|",
    ]
    for check in result.checks:
        lines.append(f"| {check.check_id} | {check.kind} | {check.status} | {_escape_pipe(check.detail)} |")

    lines.extend(["", "## Next Action", ""])
    if result.ok:
        lines.append("- Readiness package is reproducible with public-safe artifacts and commands.")
        lines.append("- Next product step: prepare firm-facing PoC narrative or installation handoff.")
    else:
        lines.append("- Fix failed checks before using this as a PoC readiness package.")
        for check in result.failed:
            lines.append(f"- {check.check_id}: {check.detail}")

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This readiness report does not prove protected K-IFRS source data, DB, embeddings, dogfood questions, customer workpapers, or raw filings are present.",
        "- It only proves public-safe demo/report/feedback queue reproducibility.",
    ])
    return "\n".join(lines) + "\n"


def write_report(path: Path, result: ReadinessResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_readiness_report(result), encoding="utf-8")


def _is_protected_artifact(path: str) -> bool:
    normalized = path.replace("\\", "/").lower()
    return any(marker in normalized for marker in PROTECTED_PATH_MARKERS)


def _last_output_line(completed: subprocess.CompletedProcess[str]) -> str:
    combined = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    lines = [line.strip() for line in combined.splitlines() if line.strip()]
    return lines[-1] if lines else f"exit {completed.returncode}"


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _escape_pipe(value: str) -> str:
    return value.replace("|", "\\|")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate public-safe toolkit readiness.")
    parser.add_argument("--manifest", type=Path, default=ROOT / "docs/toolkit/readiness_manifest.json")
    parser.add_argument("--out", type=Path, default=ROOT / "docs/reports/2026-07-05-tk3-toolkit-readiness-report.md")
    parser.add_argument("--no-run-commands", action="store_true")
    args = parser.parse_args()

    result = run_readiness(args.manifest, run_commands=not args.no_run_commands)
    write_report(args.out, result)
    print(f"wrote {args.out}")
    print(f"ok: {result.ok}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
