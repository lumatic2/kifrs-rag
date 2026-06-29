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
        timeout=180,
    )
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Integrated expanded Engine Quality Ops smoke.")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    commands = [
        [
            sys.executable, "scripts/eval_quality_gate.py",
            "--runner", "local-rag",
            "--only", "Q019", "Q020", "Q021", "Q022", "Q023",
            "--min-composite", "0.6",
            "--min-cite", "0.45",
            "--format", "text",
        ],
        [sys.executable, "scripts/validate_authority_sources.py"],
        [sys.executable, "scripts/validate_authority_source_pack.py"],
        [sys.executable, "scripts/authority_index_smoke.py", "--query", "금융감독원 질의회신 수익"],
        [sys.executable, "scripts/migrate_user_notes_v2.py", "--format", "text"],
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
