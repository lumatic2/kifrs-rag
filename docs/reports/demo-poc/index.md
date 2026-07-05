# K-IFRS RAG Product Packaging PoC

Demo scenario: 1115 수익인식 + F/S draft + audit analytics linkage.

## Files
- `1115-significant-financing-review-pack.md`
- `1115-repurchase-review-pack.md`
- `statement-candidates.md`
- `evidence-boundary.md`
- `audit-analytics-note.md`
- `audit-facc-links.md`
- `1116-lease-review-pack.md`
- `../2026-07-05-espdn1-external-source-connector-post-close-demo-packet-note.md`
- `../2026-07-05-eslrc1-external-source-connector-live-metadata-report-close-gate.md`

## External Connector Evidence
- Open `../2026-07-05-espdn1-external-source-connector-post-close-demo-packet-note.md` first when explaining the KASB/FSS connector boundary.
- KASB/FSS connector readiness is shown as metadata-only evidence in `../2026-07-05-eslrc1-external-source-connector-live-metadata-report-close-gate.md`.
- The connector evidence is locator/status readiness only; it does not fetch, store, chunk, embed, or answer from external source body text.

## Boundary
- 기준서 원문, DB, embedding, dogfood 자료는 포함하지 않는다.
- 산출물은 decision-prep draft이며 회계사 검토를 대체하지 않는다.
