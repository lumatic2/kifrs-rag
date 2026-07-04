from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.ingestion import validate_evidence_manifest


def main() -> None:
    evidence_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    result = validate_evidence_manifest(evidence_path) if evidence_path else validate_evidence_manifest()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

