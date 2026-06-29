from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> dict:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=120,
    )
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Integrated Engine Quality Ops smoke.")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    commands = [
        [sys.executable, "scripts/audit_user_notes.py", "--format", "json"],
        [sys.executable, "-m", "kifrs.eval.harness", "--runner", "local-rag", "--only", "Q019", "Q020", "Q021", "--quiet"],
        [sys.executable, "scripts/authority_index_smoke.py", "--query", "상법 자본거래 무상증자"],
    ]
    results = [run(cmd) for cmd in commands]
    payload = {
        "ok": all(result["returncode"] == 0 for result in results),
        "results": results,
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {payload['ok']}")
        for result in results:
            print(f"- {' '.join(result['cmd'])}: {result['returncode']}")

    if not payload["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
