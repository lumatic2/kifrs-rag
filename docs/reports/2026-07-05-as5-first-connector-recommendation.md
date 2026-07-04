# AS5 First Connector Recommendation

> Horizon: `authority-source-map`
> Step: AS5 — First Connector Recommendation
> Date: 2026-07-05

## 한 줄 결론

다음 horizon은 `multi-source-ingestion-pipeline`로 가야 한다. 첫 connector 후보는 3개로 좁힌다:

1. `kasb-fss-interpretive-catalog`
2. `opendart-structured-financials`
3. `law-regulation-locator`

이 셋이면 회계 판단 보조, 실제 회사 수치, 법적 boundary를 동시에 열 수 있다. Audit standards와
client-private case intake는 중요하지만 첫 파이프라인이 안정된 뒤로 미룬다.

## Recommended First Connectors

### 1. `kasb-fss-interpretive-catalog`

Lane:

- `document_rag` metadata-first

Why first:

- K-IFRS 문단만으로 부족한 실무 적용 맥락을 보완한다.
- F-ACC workflow의 검토메모 품질에 직접 영향을 준다.
- body ingestion 없이도 metadata catalog부터 만들 수 있어 public boundary가 안전하다.

Minimum scope:

- source id
- title
- publisher
- URL/locator
- document type
- publication date if available
- related standard if available
- citation role: `supporting_interpretation`
- storage policy: `public_metadata_only` or `local_private_body`

Explicitly out of scope:

- 질의회신/교육자료 본문 복사
- PDF body commit
- interpretive material alone deciding accounting treatment

### 2. `opendart-structured-financials`

Lane:

- `structured_data`

Why first:

- 재무제표 후보와 감사 분석 기능을 실제 회사 공시 데이터와 연결한다.
- "AI가 기준서만 아는 상태"에서 "회사 수치를 읽고 판단 초안을 만드는 상태"로 넘어가는 핵심이다.
- structured fact source라 document chunking과 다른 pipeline requirement를 일찍 드러낸다.

Minimum scope:

- company id / corp code
- filing id
- report period
- statement type
- line item
- value
- unit
- filing locator
- retrieved_at
- citation role: `fact_evidence`
- storage policy: `local_private_structured_data` with public synthetic fixtures

Explicitly out of scope:

- raw XBRL dump commit
- downloaded filing body commit
- accounting treatment decision from filing data alone
- external API key exposure

### 3. `law-regulation-locator`

Lane:

- `document_rag` locator / law API boundary

Why first:

- 회계 답변에서 법적/procedural boundary를 분리하는 데 필요하다.
- 외감법, 상법, 자본시장법 질문은 K-IFRS만으로 답하면 안 된다.
- body text storage 없이 article locator 중심 prototype이 가능하다.

Minimum scope:

- law id
- article locator
- official URL or registry reference
- effective date if available
- legal topic tags
- citation role: `legal_boundary` or `primary_legal_evidence`
- storage policy: `no_store_link_only` or `local_private_body`

Explicitly out of scope:

- 법령 조문 본문 public copy
- 세법 본답변 구현
- legal advice final conclusion without human review

## Deferred Connectors

| Connector | Why deferred |
|---|---|
| `audit-standards-namespace` | F-AUD workflow is still thinner than F-ACC; start after first ingestion contract proves document lane. |
| `client-private-case-intake` | Highest product value, but requires redaction/security UX and local-private handling first. |
| `firm-public-guides` | Supporting only; should not drive the first authority pipeline. |

## Next Horizon Proposal

Horizon:

- `multi-source-ingestion-pipeline`

Goal:

- Create a reusable ingestion skeleton that can register metadata-only document sources and structured fact sources
  without committing protected body text.

Suggested milestones:

1. **MSI1 — Connector contract and source manifest**
   - Define common connector output schema for document metadata and structured facts.
2. **MSI2 — Metadata-only document catalog prototype**
   - Implement a safe local/public manifest path for KASB/FSS-style interpretive source metadata.
3. **MSI3 — Structured fact fixture prototype**
   - Implement synthetic OpenDART-like financial facts and indexing contract.
4. **MSI4 — Provenance and citation manifest**
   - Connect source ids, locators, storage policies, and citation roles into an evidence manifest.
5. **MSI5 — Ingestion gate and close report**
   - Validate no protected body fields are committed and define next multi-authority runtime horizon inputs.

## Close Decision

`authority-source-map` can close after AS5.

What is now known:

- source classes are defined;
- authority/citation policy is defined;
- storage boundary is defined;
- ingestion lanes are defined;
- first connector candidates are chosen.

What is deliberately not done:

- no body ingestion;
- no parser/fetcher implementation;
- no schema migration;
- no external API call;
- no client-private intake.

Those belong to `multi-source-ingestion-pipeline`.
