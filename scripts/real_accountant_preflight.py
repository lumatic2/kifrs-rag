from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.real_accountant_run_sheet import build_run_sheet
    from scripts.real_accountant_session_check import check_session_manifest
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    try:
        from scripts.real_accountant_run_sheet import build_run_sheet
        from scripts.real_accountant_session_check import check_session_manifest
    except ModuleNotFoundError:
        from real_accountant_run_sheet import build_run_sheet
        from real_accountant_session_check import check_session_manifest


DEFAULT_MANIFEST = Path("docs/reports/real-accountant-session/session_manifest.json")


def check_preflight(
    *,
    root: Path,
    manifest: Path = DEFAULT_MANIFEST,
    run_generators: bool = False,
    timeout: int = 120,
) -> tuple[bool, list[str], dict[str, Any]]:
    errors: list[str] = []
    sheet = build_run_sheet()
    evidence: dict[str, Any] = {
        "open_files": {},
        "generator_results": [],
    }

    session_ok, session_errors, mode = check_session_manifest(manifest, root=root)
    evidence["session_mode"] = mode
    if not session_ok:
        errors.extend(f"session_manifest: {error}" for error in session_errors)
    if mode != "ready_to_schedule":
        errors.append(f"session_manifest: expected ready_to_schedule before session, got {mode}")

    for item in sheet["open_files"]:
        exists = (root / item).exists()
        evidence["open_files"][item] = exists
        if not exists:
            errors.append(f"missing open file: {item}")

    if run_generators:
        for command in sheet["preflight_commands"]:
            result = _run_command(command, root=root, timeout=timeout)
            evidence["generator_results"].append(result)
            if result["returncode"] != 0:
                errors.append(f"generator failed: {command}")

    return not errors, errors, evidence


def render_text(ok: bool, errors: list[str], evidence: dict[str, Any]) -> str:
    lines = [
        f"ok: {ok}",
        f"session_mode: {evidence.get('session_mode')}",
        "open_files:",
    ]
    for path, exists in evidence.get("open_files", {}).items():
        lines.append(f"- {path}: {exists}")
    if evidence.get("generator_results"):
        lines.append("generator_results:")
        for result in evidence["generator_results"]:
            lines.append(f"- {result['cmd']}: {result['returncode']}")
    for error in errors:
        lines.append(f"- {error}")
    return "\n".join(lines) + "\n"


def _run_command(command: str, *, root: Path, timeout: int) -> dict[str, Any]:
    proc = subprocess.run(
        command,
        cwd=root,
        text=True,
        capture_output=True,
        shell=True,
        timeout=timeout,
    )
    return {
        "cmd": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check real accountant session preflight files and optional generators.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--run-generators", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    ok, errors, evidence = check_preflight(
        root=args.root,
        manifest=args.manifest,
        run_generators=args.run_generators,
        timeout=args.timeout,
    )
    if args.format == "json":
        print(json.dumps({"ok": ok, "errors": errors, "evidence": evidence}, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(ok, errors, evidence), end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
