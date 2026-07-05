# External Source Body Storage Policy

> Scope: policy required before any live external source body fetch, cache, chunk, embed, or index work.

## Decision

This policy does not authorize body ingestion. It defines the storage boundary that must exist before a separate authorization gate can allow implementation.

## Covered Source Classes

- `interpretive_accounting_material`
- `law_regulation`
- `primary_audit_standard`
- `supporting_material`

## Storage Boundary

- Body storage mode: `local_private_body_only_after_source_review`
- Public artifact rule: public repo may store metadata, locators, schema, tests, aggregate metrics, and author-written notes only
- Local artifact rule: body cache, chunks, and embeddings may exist only in gitignored local/private paths after source-specific review

## Required Source Checks

- record publisher and canonical locator
- check robots/terms/license constraints for the exact source
- classify authority role before retrieval use
- choose source-specific chunk strategy before storing any chunk
- document deletion/reindex command before first local cache write

## Required Operator Checks

- run metadata-only live validation before source-specific review
- verify target cache/index paths are gitignored
- run forbidden-field scan before committing any report or manifest
- keep K-IFRS primary evidence priority above external body text
- record explicit user authorization before live body ingestion

## Public Forbidden Fields

- `api_key`
- `body`
- `content`
- `credential`
- `embedding`
- `excerpt`
- `full_text`
- `pdf_bytes`
- `quote`
- `raw_xml`
- `source_body`
- `text`
- `token`
- `xbrl_dump`

## Authorization Boundary

- Body fetching allowed by this policy: False
- Chunking allowed by this policy: False
- Embedding allowed by this policy: False
- Commit allowed by this policy: False
