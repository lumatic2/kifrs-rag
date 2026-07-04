# Local Toolkit Readiness

This folder defines the public-safe readiness package for the `kifrs-rag` local accounting intelligence toolkit.

## What This Readiness Package Proves

- The demo bundle can be regenerated from public synthetic fixtures.
- The source-aware workflow rebuild report can be regenerated.
- The feedback eval/backlog queue sample can be regenerated.
- The public-safe quality preflight passes.

## What It Does Not Include

- K-IFRS source PDFs
- parsed K-IFRS text
- SQLite DB dumps
- embeddings
- CPA exam dogfood questions
- raw DART filings
- customer or client workpapers

Those assets are intentionally outside the public readiness package.

## Default Check

```powershell
python scripts\toolkit_readiness.py --manifest docs\toolkit\readiness_manifest.json --out docs\reports\2026-07-05-tk3-toolkit-readiness-report.md
```

## Manual Reproduction Commands

```powershell
python scripts\quality_preflight.py --format text
python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc
python scripts\workflow_rebuild_report.py --out docs\reports\2026-07-05-wr3-source-aware-rebuild-report.md
python scripts\feedback_queue_report.py --queue docs\feedback\feedback_queue.sample.jsonl --out docs\reports\2026-07-05-fi3-feedback-queue-report.md
```
