"""parsed JSON → SQLite 적재 파이프라인.

실행:
  uv run python scripts/ingest.py                  # data/standards/parsed/*.json 전부
  uv run python scripts/ingest.py --only 1115       # 특정 기준서만
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kifrs import store

PARSED_DIR = Path(__file__).resolve().parent.parent / "data" / "standards" / "parsed"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="특정 기준서만 (파일명 stem, 예: 1115)")
    args = ap.parse_args()

    store.init_db()
    files = sorted(PARSED_DIR.glob("*.json"))
    files = [f for f in files if not f.stem.endswith("_view") and f.stem != "index"]
    if args.only:
        files = [f for f in files if f.stem == args.only]
    if not files:
        print("  [WARN] 적재할 JSON 없음. 먼저 `uv run python -m kifrs.parse` 실행.")
        return
    for f in files:
        r = store.upsert_from_json(f)
        print(f"  ✓ {r['standard']}: {r['paragraphs']} paragraphs")
    print(f"\n총 {len(files)}개 기준서 적재 완료 → {store.DB_PATH.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
