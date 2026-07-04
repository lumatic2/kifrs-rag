# Field Feedback Capture Package

> Public-safe sample capture package. This is not actual accountant feedback evidence.

## Files

1. `feedback-notes.sample.md` - sample structured feedback notes
2. `capture-report.md` - capture summary and next actions
3. `feedback-queue.jsonl` - queue records generated from safe corrections
4. `feedback-queue-report.md` - queue report
5. `capture-manifest.json` - machine-readable capture manifest

## Boundary

- The sample notes are not actual accountant feedback.
- Protected payloads are rejected before queue conversion.
- Raw contracts, customer identifiers, copied source bodies, private filings, parsed standards, embeddings, and workpaper payloads are not stored.

## Regeneration

```powershell
python scripts\field_feedback_capture.py --out docs\reports\field-feedback-capture
```
