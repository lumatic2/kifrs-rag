from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.authority import search_authority


def main() -> None:
    parser = argparse.ArgumentParser(description="Search metadata-only authority registry.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(search_authority(args.query, args.limit), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
