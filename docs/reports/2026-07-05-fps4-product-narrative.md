# FPS4 Product Narrative README Surface

> Scope: FPS4 README/product narrative check for the firm-facing local demo surface.

## One-Line Result

The README now explains the current firm-facing demo command, capability boundary, and non-goals.

## README

- path: `README.md`
- ok: True

## Narrative Claims

- The product is a local accounting-intelligence toolkit prototype for firm-side PoC.
- The current showable surface is the K-IFRS 1116 operator walkthrough packet.
- The output is decision-support only; accountant judgment and sign-off remain human.
- Protected standards, embeddings, dogfood material, and private client payloads are not published.

## Missing Phrases

- none

## Forbidden Hits

- none

## Machine Result

```json
{
  "title": "FPS4 Product Narrative README Surface",
  "ok": true,
  "horizon": "firm-facing-product-surface",
  "milestone": "FPS4",
  "readme_path": "README.md",
  "required_phrases": [
    "Firm-Facing Local Demo",
    "python scripts/firm_facing_operator_demo_command.py --format markdown --write",
    "What it can do now",
    "What it does not do",
    "does not replace accountant judgment",
    "not a packaged SaaS product yet"
  ],
  "missing_phrases": [],
  "forbidden_hits": [],
  "narrative_claims": [
    "The product is a local accounting-intelligence toolkit prototype for firm-side PoC.",
    "The current showable surface is the K-IFRS 1116 operator walkthrough packet.",
    "The output is decision-support only; accountant judgment and sign-off remain human.",
    "Protected standards, embeddings, dogfood material, and private client payloads are not published."
  ],
  "report_path": "docs/reports/2026-07-05-fps4-product-narrative.md",
  "next_leaf": "FPS5_firm_facing_surface_close_gate"
}
```
