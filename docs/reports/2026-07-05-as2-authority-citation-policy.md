# AS2 Authority and Citation Policy

> Horizon: `authority-source-map`
> Step: AS2 — Authority and Citation Policy
> Date: 2026-07-05

## 한 줄 결론

Multi-source RAG에서는 source를 한 ranking list로 섞으면 안 된다. 답변은 **primary accounting evidence,
interpretive support, audit authority, legal boundary, filing/fact evidence, client-provided facts,
supporting material**을 분리해서 보여줘야 한다.

## Authority Priority by Question Type

숫자 priority는 낮을수록 강한 권위다. 단, 모든 질문에 같은 priority를 적용하지 않는다. 질문 유형별로
권위 순서가 달라진다.

### Accounting treatment question

예: 수익인식, 리스 회계처리, 금융상품 분류, 손상, 공정가치 측정.

| Rank | Source class | Citation role | May decide answer? |
|---:|---|---|---|
| 1 | Primary accounting standards | `primary_accounting_evidence` | yes |
| 2 | Interpretive accounting material | `supporting_interpretation` | no, unless primary is also cited |
| 3 | Filing/data | `fact_example` | no |
| 4 | Client-private | `client_fact` | no, fact pattern only |
| 5 | Supporting material | `background_support` | no |
| Boundary | Law/regulation | `legal_boundary` | only for legal/procedural requirement |

Rule:

- Accounting treatment answer must cite K-IFRS primary evidence when available.
- Interpretive material can explain application but cannot replace K-IFRS paragraphs.
- DART or client facts can support fact pattern, not accounting authority.

### Audit workflow question

예: 감사계획, 위험평가, 분석적 절차, 감사증거, 조서화.

| Rank | Source class | Citation role | May decide answer? |
|---:|---|---|---|
| 1 | Audit standards | `primary_audit_evidence` | yes |
| 2 | Law/regulation | `legal_boundary` | yes for statutory audit requirements |
| 3 | Filing/data | `fact_evidence` | no, but drives procedures |
| 4 | Client-private | `client_fact` | no, fact pattern/workpaper input |
| 5 | Primary accounting standards | `accounting_context` | no, unless accounting treatment is also asked |
| 6 | Supporting material | `background_support` | no |

Rule:

- Audit workflow answers must not pretend K-IFRS measurement guidance is audit procedure authority.
- If the question asks both accounting treatment and audit response, answer sections must be split.

### Legal/procedural boundary question

예: 외감 대상, 감사보고서 제출, 배당/자본거래 법적 제한, 세무 handoff.

| Rank | Source class | Citation role | May decide answer? |
|---:|---|---|---|
| 1 | Law/regulation | `primary_legal_evidence` | yes |
| 2 | Regulatory guidance | `supporting_regulatory_context` | no, unless question asks about guidance |
| 3 | Primary accounting standards | `accounting_context` | no |
| 4 | Filing/data | `fact_evidence` | no |
| 5 | Supporting material | `background_support` | no |

Rule:

- Legal/procedural answers must not be answered from K-IFRS alone.
- Tax questions are boundary/handoff in this repo unless a sibling tax source is explicitly invoked.

### Company filing/data question

예: 회사 재무제표 수치, 주석 사례, peer comparison, 감사 분석 숫자.

| Rank | Source class | Citation role | May decide answer? |
|---:|---|---|---|
| 1 | Filing/data | `fact_evidence` | yes for factual values |
| 2 | Client-private | `client_fact` | yes for supplied case facts |
| 3 | Primary accounting standards | `accounting_rule_context` | no for facts, yes for treatment |
| 4 | Interpretive accounting material | `supporting_interpretation` | no |

Rule:

- Filing/data can answer "what was disclosed" or "what is the number".
- Filing/data cannot answer "what should the accounting treatment be" without authority evidence.

## Answer Evidence Sections

Answer composer should group evidence into these sections.

| Section | Required when | Contains |
|---|---|---|
| `Primary accounting evidence` | accounting treatment question | K-IFRS paragraph citations |
| `Interpretive support` | KASB/FSS/FSC material used | material id/link/date and short author-written summary |
| `Audit authority` | audit workflow question | audit standard / KAASB / KICPA source ids |
| `Legal boundary` | law/regulation affects answer | statute/regulation locator |
| `Fact evidence` | DART/OpenDART/XBRL or filing data used | company, filing, period, line item, value |
| `Client-provided facts` | private case input used | document id, fact label, not body text |
| `Supporting material` | firm guide/education/article used | source id, title, use as background only |
| `Insufficient evidence` | required authority missing | missing source class and what human must verify |

## Conflict Policy

### Primary vs interpretive

If interpretive material appears inconsistent with K-IFRS primary evidence:

1. cite K-IFRS primary evidence first;
2. state that interpretive material is support/context;
3. mark as `NeedsHumanReview`;
4. do not override primary evidence with interpretive material.

### Accounting vs legal

If accounting treatment and legal/procedural requirement point to different actions:

1. split the answer into accounting treatment and legal/procedural sections;
2. do not collapse them into a single conclusion;
3. mark the legal point as boundary or handoff if outside repo scope.

### Filing/client facts vs authority

If company filing or client document facts conflict with authority assumptions:

1. treat filing/client material as facts, not rules;
2. show the factual conflict;
3. ask for human confirmation of fact pattern;
4. keep the accounting conclusion conditional.

### Supporting material conflict

If firm guide/article/supporting material conflicts with primary/interpreting source:

- ignore it for the conclusion;
- optionally mention it only as background if useful;
- never cite it as authority.

## Insufficient Evidence Policy

The system must say "근거 부족" or `NeedsHumanReview` when:

- accounting treatment question lacks K-IFRS primary evidence;
- audit workflow question lacks audit authority;
- legal/procedural question lacks law/regulation locator;
- company-specific answer lacks filing/client fact source;
- source classes conflict and no priority rule resolves it;
- only supporting material is available.

Recommended wording pattern:

```text
현재 근거만으로는 결론을 확정할 수 없습니다.
부족한 근거: <missing source class>.
현재 사용할 수 있는 근거: <available evidence sections>.
사람이 확인할 사항: <fact/source/action>.
```

## Current Schema Gaps

Current `docs/authority/*.json` validates metadata-only source records, but it does not yet encode the full answer
policy.

Candidate fields for later schema update:

| Field | Applies to | Why |
|---|---|---|
| `source_class` | source and pack item | map to AS1 taxonomy |
| `namespace` | source and pack item | separate F-ACC, F-AUD, legal, filing, client-private |
| `citation_role` | pack item | answer section routing |
| `body_storage_policy` | source and pack item | public metadata / local-private / no-body |
| `may_decide_answer_types` | source | prevent filing/supporting material from deciding accounting treatment |
| `requires_primary_source_id` | interpretive/supporting sources | ensure K-IFRS primary remains first |
| `conflict_behavior` | source class | mark NeedsHumanReview / split answer / ignore supporting |

AS2 does not change schema yet. AS3 and AS4 should decide which fields become validator-enforced.

## Policy Decision

AS2 is complete enough to move to AS3.

The next step should define copyright/storage boundaries before any schema or ingestion work. Otherwise the project
risks creating fields that imply body text may be stored in the public repo.

