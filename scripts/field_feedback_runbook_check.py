from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

PROTECTED_MARKERS = {
    "data/",
    "embeddings/",
    "*.db",
    "*.pdf",
    "data/dogfood/",
    "raw_contract",
    "customer_identifier",
}


def check_manifest(manifest_path: Path, *, root: Path = ROOT) -> tuple[bool, list[str]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for artifact in manifest.get("required_artifacts", []):
        if _is_protected_requirement(artifact):
            errors.append(f"protected required artifact: {artifact}")
            continue
        path = root / artifact
        if not path.exists():
            errors.append(f"missing artifact: {artifact}")

    required_sections: dict[str, list[str]] = manifest.get("required_sections", {})
    for artifact, sections in required_sections.items():
        path = root / artifact
        if not path.exists():
            errors.append(f"missing section source: {artifact}")
            continue
        text = path.read_text(encoding="utf-8")
        for section in sections:
            if section not in text:
                errors.append(f"missing section in {artifact}: {section}")
    return not errors, errors


def _is_protected_requirement(value: Any) -> bool:
    text = str(value)
    return any(marker in text for marker in PROTECTED_MARKERS)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check field feedback runbook manifest.")
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    ok, errors = check_manifest(args.manifest)
    print(f"ok: {ok}")
    for error in errors:
        print(f"- {error}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
