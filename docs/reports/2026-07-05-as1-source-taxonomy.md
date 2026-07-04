# AS1 Source Taxonomy

> Horizon: `authority-source-map`
> Step: AS1 — Source Taxonomy
> Date: 2026-07-05
> Inputs: `docs/reports/2026-07-05-non-ifrs-source-map.md`, `docs/authority/sources.json`

## One-Line Decision

Multi-source accounting RAG uses seven source classes. They are separated by what they are allowed to decide:
accounting rules, audit procedure, legal boundary, public facts, private facts, interpretation support, or background.

## Taxonomy

| Class ID | Name | Examples | Primary RAG role | May decide answer? | Public repo body storage |
|---|---|---|---|---|---|
| `primary_accounting_standard` | Primary accounting standards | K-IFRS paragraph DB | Recognition, measurement, presentation, disclosure authority | Yes, for accounting treatment | No body text; local DB only |
| `interpretive_accounting_material` | Interpretive accounting material | KASB education/interpretation material, FSS/FSC accounting inquiry or supervision material | Explain application context after primary standard evidence | No, unless primary evidence is also cited | Metadata only until AS3 decides private storage |
| `primary_audit_standard` | Audit standards | Audit standards, KAASB/KICPA audit authority candidates | Audit planning, risk assessment, evidence, workpaper, opinion workflow authority | Yes, for audit workflow | Metadata only until dedicated audit namespace |
| `law_regulation` | Law and regulation | External Audit Act, Commercial Act, Capital Markets Act, enforcement decrees | Legal/procedural boundary, statutory requirement, filing responsibility | Yes, for legal/procedural boundary only | Metadata/locator only in public repo |
| `filing_data` | Filing and structured facts | DART/OpenDART, XBRL, annual reports, audit reports | Public company facts, disclosed values, peer examples, analytics input | Yes for factual values; no for accounting treatment | Schema and synthetic fixtures only |
| `client_private` | Client-private material | Contracts, accounting policy, trial balance, workpapers, management memo | Fact pattern and case context | Yes for supplied facts; no for authority | Never public; local/private namespace only |
| `supporting_material` | Supporting/background material | Firm guides, articles, training notes, public explainers | Background explanation, checklist inspiration | No | Metadata or author-written notes only |

## Workflow Mapping

| Workflow | Required source classes | Optional source classes | Boundary |
|---|---|---|---|
| F-ACC accounting advisory | `primary_accounting_standard`, `client_private` | `interpretive_accounting_material`, `filing_data`, `supporting_material` | legal/tax points are split or handed off |
| F-AUD audit workflow | `primary_audit_standard`, `client_private`, `filing_data` | `primary_accounting_standard`, `law_regulation` | K-IFRS is accounting context, not audit procedure authority |
| Disclosure draft/review | `primary_accounting_standard`, `filing_data`, `client_private` | `interpretive_accounting_material`, `supporting_material` | filing examples are facts/examples, not rules |
| Legal/procedural check | `law_regulation` | `filing_data`, `primary_accounting_standard` | this repo does not provide legal/tax advice as final advice |
| Benchmark/eval | `primary_accounting_standard` | `exam_convention`, synthetic fixtures | dogfood/question source body remains private |

## Current Registry Mapping

| Current source id | AS1 class | Current status | Notes |
|---|---|---|---|
| `kifrs-primary` | `primary_accounting_standard` | local-private-db | Existing primary evidence source |
| `kasb-interpretation-material` | `interpretive_accounting_material` | metadata-only | Supporting guidance; not primary authority |
| `fss-accounting-inquiry` | `interpretive_accounting_material` | metadata-only | Regulatory/supervisory context |
| `commercial-act-capital` | `law_regulation` | metadata-only | Legal boundary for capital/dividend questions |
| `tax-law-boundary` | `law_regulation` | metadata-only | Boundary/handoff, not tax-agent replacement |
| `opendart-structured-financials` | `filing_data` | metadata-only | Fact source candidate; synthetic fixtures only in public repo |
| `exam-convention` | `supporting_material` | metadata-only | Answer-shape convention, not accounting authority |

## Design Consequences

1. `source_class` should become a required schema field before multi-source ingestion is broadened.
2. Answer composition should group evidence by source class, not by raw retrieval score.
3. `client_private` cannot share storage/index namespace with public examples.
4. `filing_data` needs structured fact retrieval, not only document chunk retrieval.
5. `interpretive_accounting_material` needs a `requires_primary_accounting_evidence` rule.

## AS1 Close

AS1 is complete enough for AS3/AS4. The next useful leaf is AS3 copyright/storage boundary, because ingestion feasibility
depends on whether each class can store body text, metadata only, or local-private artifacts.
