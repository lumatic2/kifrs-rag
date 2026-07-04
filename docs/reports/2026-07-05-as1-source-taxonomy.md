# AS1 Source Taxonomy

> Horizon: `authority-source-map`
> Step: AS1 — Source Taxonomy
> Date: 2026-07-05

## 한 줄 결론

회계 업무 RAG의 source는 최소 7개 class로 나눠야 한다. 현재 registry는 K-IFRS primary, KASB/FSS
interpretive 후보, 상법/세법 boundary, exam convention은 갖고 있지만, **audit standards, DART/XBRL,
client-private, supporting material class가 아직 비어 있다.**

## Source Classes

| Class | Examples | RAG role | Authority level | Storage boundary |
|---|---|---|---|---|
| Primary accounting standards | K-IFRS 기준서 본문 | recognition/measurement/presentation/disclosure의 1차 근거 | highest | local-private body, public metadata |
| Interpretive accounting material | KASB 해석/교육자료, FSS/FSC 질의회신/감리자료 | 기준서 적용 맥락과 실무 해석 보조 | high but below primary | metadata first, body ingestion only after policy |
| Audit standards | KSA/감사기준, KAASB/KICPA 자료 | 감사계획, 위험평가, 감사절차, 조서화 근거 | high for audit workflow | separate F-AUD namespace |
| Law/regulation | 외감법, 상법, 자본시장법, 시행령/시행규칙 | 법적 요건, 공시/감사 대상, 자본거래 boundary | high for legal boundary | public legal locator + chunk policy |
| Filing/data | DART/OpenDART, XBRL, 사업보고서, 감사보고서 | 회사별 수치, 공시 사례, peer comparison | factual filing, not accounting rule | structured data namespace |
| Client-private | 계약서, 회계정책서, TB, 조서, management memo | 실제 case fact pattern | fact source, not authority | local/private only |
| Supporting material | 회계법인 public guide, 기사, 교육자료 | 설명, checklist, background | low/supporting | metadata or short citation only |

## Current Registry Mapping

### `docs/authority/sources.json`

| Current source id | Maps to class | Status |
|---|---|---|
| `kifrs-primary` | Primary accounting standards | present |
| `kasb-interpretation-material` | Interpretive accounting material | present as metadata-only |
| `fss-accounting-inquiry` | Interpretive accounting material | present as metadata-only |
| `commercial-act-capital` | Law/regulation | present but narrow |
| `tax-law-boundary` | Law/regulation / boundary | present as handoff boundary |
| `exam-convention` | Supporting / exam convention | present as local convention |

### `docs/authority/source_pack.json`

| Current item id | Maps to class | Status |
|---|---|---|
| `kifrs-local-paragraph-db` | Primary accounting standards | available-local-private |
| `kasb-implementation-material-index` | Interpretive accounting material | collection_seed |
| `fss-accounting-inquiry-index` | Interpretive accounting material | collection_seed |
| `commercial-act-capital-boundary` | Law/regulation | collection_seed |
| `tax-law-accounting-boundary` | Law/regulation / handoff | collection_seed |
| `exam-convention-local-notes` | Supporting / local-authored convention | available-local-private |

## Missing Classes

| Missing class | Why it matters | Proposed source id |
|---|---|---|
| Audit standards | F-AUD workflow needs audit procedure/workpaper authority separate from accounting treatment | `audit-standards-ksa` |
| Filing/data | statement draft and audit analytics need company facts, not only rules | `opendart-filing-data` |
| Client-private | actual PoC requires contracts/TB/policies/workpapers as fact sources | `client-private-documents` |
| Supporting material | firm guides can help explain/checklist but must not outrank authority | `firm-public-guides` |

## RAG Use Policy by Class

| Class | May answer from it alone? | Citation role |
|---|---|---|
| Primary accounting standards | yes, if question is accounting treatment | primary citation |
| Interpretive accounting material | no, unless primary standard is also cited or question asks about the material itself | supporting interpretation |
| Audit standards | yes for audit workflow; no for accounting measurement | audit authority citation |
| Law/regulation | yes for legal/procedural requirement; no for K-IFRS measurement | legal boundary citation |
| Filing/data | no for rules; yes for factual company values | fact evidence |
| Client-private | no for authority; yes for case facts | client-provided fact |
| Supporting material | no | explanatory support only |

## Gap Against Next Steps

AS2 should decide:

- exact authority priority order when classes conflict
- answer section layout for primary vs supporting vs fact evidence
- when to say "근거 부족"
- whether registry needs new fields: `source_class`, `namespace`, `body_storage_policy`, `citation_role`

AS3 should decide:

- which classes may store body text
- which classes must store metadata/link only
- which classes are local-private only

AS4 should decide:

- fetch/parse/chunk/embed/index feasibility per class
- structured retrieval vs document RAG boundary for DART/OpenDART

## AS1 Decision

AS1 is complete enough to move to AS2.

The next implementation should not ingest documents yet. It should first update authority/citation policy so later
chunks have a clear role in answers.

