# CP3 Client-Private Evidence Adapter

> Scope: CP3 adapter from runtime parser contract to client_private_fact authority reference.

## Result

- ok: True
- horizon: `client-private-parser-runtime`
- milestone: `CP3`
- authority role: `client_private_fact`
- review pack has client-private fact: True
- statement promoted refs: 0
- public safe: True
- next leaf: `CP4_deletion_and_retention_gate`

## Boundary Meaning

- Parser runtime contract can now become a `client_private_fact` authority reference.
- Review packs can render that reference in the client-private authority section.
- Statement draft amount lines do not consume client-private facts as public fact evidence or primary K-IFRS authority.

## Machine Result

```json
{
  "title": "CP3 Client-Private Evidence Adapter",
  "ok": true,
  "horizon": "client-private-parser-runtime",
  "milestone": "CP3",
  "authority_role": "client_private_fact",
  "review_pack_has_client_private_fact": true,
  "statement_promoted_refs": 0,
  "public_safe": true,
  "next_leaf": "CP4_deletion_and_retention_gate",
  "report_path": "docs/reports/2026-07-05-cp3-client-private-evidence-adapter.md"
}
```
