# AS3 Copyright and Storage Boundary

> Horizon: `authority-source-map`
> Step: AS3 — Copyright and Storage Boundary
> Date: 2026-07-05

## 한 줄 결론

이 레포의 public artifact는 **metadata, schema, code, aggregate metrics, synthetic fixture, author-written
notes**까지만 허용한다. 기준서 본문, 외부 문서 본문, 법령/질의회신/guide 복사문, DB dump, embeddings,
client-private 자료는 public repo에 저장하지 않는다.

## Existing Guardrails

### `.gitignore`

Currently protected:

- `data/`
- `*.db`, `*.db-shm`, `*.db-wal`
- `*.pdf`
- `embeddings/`
- `.env`, `.env.*`
- `CLAUDE.local.md`, `.claude/`

### `docs/authority/source_pack_rules.md`

Current forbidden fields:

- `body`
- `text`
- `content`
- `full_text`
- `source_body`
- `excerpt`
- `quote`
- `embedding`

Current public-allowed fields:

- source id
- authority type
- title/publisher
- canonical URL or private locator label
- jurisdiction/effective date metadata
- allowed use
- priority/freshness policy
- keywords
- short author-written notes

## Storage Policy by Source Class

| Source class | Public repo allowed | Public repo forbidden | Private/local allowed |
|---|---|---|---|
| `primary_accounting_standard` | source id, standard id, paragraph locator, aggregate metrics | K-IFRS body text, PDF, parsed DB, embeddings | local DB, parsed text, embeddings |
| `interpretive_accounting_material` | source metadata, URL, document title, publisher, date, author-written summary | copied inquiry replies, copied education text, PDF body, excerpt/quote | private body cache after policy approval |
| `primary_audit_standard` | source metadata, locator, authority type, applicability note | copied standard text, PDF body, embedded chunks | private audit-standard index |
| `law_regulation` | law id, article locator, official URL, effective date metadata | copied article body in public reports unless separately approved | private law chunk store or API/cache |
| `filing_data` | company id, report id, filing locator, line-item schema, aggregate sample metrics | full filing body copy, XBRL dump if copyrighted/restricted, raw downloaded docs | structured local cache, parsed XBRL |
| `client_private` | anonymized case id, synthetic/public fixture, field schema | contracts, TB, policies, workpapers, management memo body | local encrypted/private namespace |
| `supporting_material` | source metadata, title, URL, why-supporting note | guide/article body, copied checklist, long quote | private reading notes if licensed/allowed |

## Storage Policy Labels

Future source registry fields should use one of these labels.

| Label | Meaning |
|---|---|
| `public_metadata_only` | Public repo may store metadata and author-written notes only. |
| `local_private_body` | Body text may exist locally but must not be committed. |
| `local_private_structured_data` | Parsed tables/XBRL/TB may exist locally but public repo only stores schema/sample synthetic data. |
| `public_synthetic_fixture` | Invented test fixture may be committed. |
| `no_store_link_only` | Store locator only; do not cache body without separate review. |
| `no_store_handoff` | Boundary source only; this repo should hand off rather than ingest. |

## Public Report Rules

Public reports may include:

- command outputs and pass/fail status
- aggregate retrieval metrics
- source ids and URLs
- short author-written summaries
- synthetic fixture numbers
- schema names and field names
- citations in locator form, for example `[source-id: article/paragraph locator]`

Public reports must not include:

- copied K-IFRS paragraphs
- copied law articles
- copied KASB/FSS inquiry body
- copied audit standard body
- copied firm guide text
- client document excerpts
- raw XBRL/filing body dumps
- embeddings or serialized vectors
- API keys, tokens, credentials

## Ingestion Boundary

Before any source class enters the ingestion pipeline, it needs:

1. `source_class`
2. `citation_role`
3. `body_storage_policy`
4. `namespace`
5. `public_allowed_fields`
6. `private_allowed_fields`
7. `redaction_or_synthetic_fixture_policy`

If any of these are unknown, the source remains `collection_seed` and metadata-only.

## Special Cases

### Law/regulation

Law may be publicly accessible, but this project still should not copy article bodies into repo reports by default.
Use article locator and official URL. Body-level chunking belongs in a private/local cache or a dedicated approved
connector policy.

### DART/OpenDART

OpenDART-style data is partly structured. Public repo may store schema and synthetic examples, but raw filings,
downloaded XML/XBRL, and company-specific parsed caches should stay local unless a later review explicitly marks
them publishable.

### Client-private material

Client-private source is never public body text. For demos, use:

- anonymized metadata,
- synthetic facts,
- field-level schema,
- generated review output with no identifying source text.

### Supporting material

Firm guides and articles can help product thinking but must not become authority. Store source metadata and a
short author-written note only.

## AS3 Decision

AS3 is complete enough to move to AS4.

AS4 should evaluate ingestion feasibility only under these storage labels. A source that cannot fit a safe storage
policy should not get a connector yet.
