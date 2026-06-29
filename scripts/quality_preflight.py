from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_COMMANDS = [
    {
        "name": "focused_pytest",
        "cmd": [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_eval_gates.py",
            "tests/test_authority.py",
            "tests/test_authority_source_pack.py",
            "tests/test_user_note_v2_runtime.py",
            "tests/test_user_notes.py",
            "tests/test_user_note_v2_migration.py",
            "-q",
        ],
    },
    {
        "name": "local_rag_threshold_gate",
        "cmd": [
            sys.executable,
            "scripts/eval_quality_gate.py",
            "--runner",
            "local-rag",
            "--only",
            "Q019",
            "Q020",
            "Q021",
            "Q022",
            "Q023",
            "--min-composite",
            "0.6",
            "--min-cite",
            "0.45",
            "--format",
            "text",
        ],
    },
    {
        "name": "authority_registry",
        "cmd": [sys.executable, "scripts/validate_authority_sources.py"],
    },
    {
        "name": "authority_source_pack",
        "cmd": [sys.executable, "scripts/validate_authority_source_pack.py"],
    },
    {
        "name": "user_note_v2_audit",
        "cmd": [sys.executable, "scripts/audit_user_notes.py", "--source", "v2", "--format", "json"],
    },
]


def run_command(entry: dict[str, Any], timeout: int) -> dict[str, Any]:
    proc = subprocess.run(
        entry["cmd"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    return {
        "name": entry["name"],
        "cmd": entry["cmd"],
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def run_preflight(timeout: int = 240) -> dict[str, Any]:
    results = [run_command(entry, timeout) for entry in DEFAULT_COMMANDS]
    return {
        "ok": all(result["returncode"] == 0 for result in results),
        "public_safe": True,
        "protected_assets_required": False,
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run public-safe K-IFRS RAG quality preflight.")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()

    payload = run_preflight(timeout=args.timeout)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {payload['ok']}")
        print(f"public_safe: {payload['public_safe']}")
        print(f"protected_assets_required: {payload['protected_assets_required']}")
        for result in payload["results"]:
            print(f"- {result['name']}: {result['returncode']}")
    if not payload["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
