# Authority Source Pack Rules

> Purpose: define how external authority candidates may be collected without mixing them with primary K-IFRS evidence or committing protected body text.

## Boundary

K-IFRS paragraph DB remains the primary evidence source. External sources are supporting or boundary signals only unless a future plan explicitly promotes a source with verified legal/accounting authority and a separate evidence rule.

The public repo may store:

- source id and authority type;
- title and publisher;
- canonical URL or local-private locator label;
- jurisdiction and effective date metadata;
- allowed use case;
- priority and freshness policy;
- keywords and short notes written by the repo author.

The public repo must not store:

- K-IFRS source body text;
- external document body text;
- copied inquiry replies, law articles, education material, or exam source text;
- embeddings, parsed DB dumps, PDFs, or dogfood source questions.

## Allowed Use Cases

| Use Case | Meaning |
|---|---|
| `primary_evidence` | K-IFRS local paragraph DB only. |
| `supporting_interpretation` | KASB/FSS/external material may inform interpretation after primary K-IFRS evidence is cited. |
| `legal_boundary` | Law/tax source may mark where K-IFRS answer must stop or hand off. |
| `answer_convention` | Exam/dogfood convention may affect answer shape, not accounting authority. |
| `collection_seed` | Metadata candidate queued for private/manual collection. |

## Ranking Rule

Lower `priority` means stronger authority within the same query context.

1. K-IFRS primary evidence is always first.
2. KASB standard-setter material may support implementation explanation.
3. FSS/regulatory material may support Korean practice or enforcement context.
4. Commercial law and tax law are boundary sources, not K-IFRS substitutes.
5. Exam convention is answer-shape guidance only.

## Required Fields

Each `source_pack` item must include:

- `id`
- `source_id`
- `title`
- `publisher`
- `authority_type`
- `allowed_use`
- `priority`
- `locator`
- `status`
- `keywords`
- `notes`

`source_id` must exist in `docs/authority/sources.json`.

## Forbidden Fields

The validator rejects fields that imply committed source body:

- `body`
- `text`
- `content`
- `full_text`
- `source_body`
- `excerpt`
- `quote`
- `embedding`

Short author-written `notes` are allowed, but they must not reproduce source body text.
