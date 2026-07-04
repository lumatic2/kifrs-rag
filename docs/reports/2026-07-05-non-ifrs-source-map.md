# Non-IFRS Source Map

> Date: 2026-07-05
> Purpose: K-IFRS 본문 외에 회계 업무 RAG에 필요한 정보원을 권위 수준과 ingestion 관점으로 분류한다.

## 원칙

회계 AI가 쓸 정보원은 모두 같은 무게가 아니다. RAG에 넣을 때는 "많이 가져오기"보다
**권위, 최신성, 저작권/저장 가능성, citation 가능성, 업무 활용 위치**를 먼저 정해야 한다.

## Source Classes

| Class | 예시 | RAG 역할 | 권위 | 첫 처리 |
|---|---|---|---|---|
| Accounting standards | K-IFRS 기준서, 시행 중 기준서 목록 | 회계처리 판단의 1차 근거 | 최상 | 기존 인덱스 품질 refresh |
| Interpretive accounting material | KASB 질의회신, FSS/FSC 회계감독/질의회신 | 기준서 적용 맥락, 실무 판단 보조 | 높음 | source catalog 후 수집 가능성 검토 |
| Audit standards | KSA/감사기준, KICPA/KAASB 관련 자료 | 감사 절차/조서/감사의견 판단 | 높음 | F-AUD horizon에서 별도 namespace |
| Law/regulation | 외감법, 상법, 자본시장법, 시행령 | 책임, 공시, 감사 대상, 절차 요건 | 높음 | law source connector 후보 |
| Filing/data | DART/OpenDART, XBRL, 사업보고서, 감사보고서 | 실제 회사 수치/공시/비교 가능 사례 | 중~높음 | structured-data ingestion 후보 |
| Client-private | 계약서, 회계정책서, TB, 조서, 내부 memo | 실제 업무 case context | 업무상 필수 | local-only/private namespace |
| Supporting material | 회계법인 public guide, 기사, 교육자료 | 설명/해설/체크리스트 보조 | 낮음 | authoritative answer에는 보조로만 사용 |

## Source Notes

### KASB / K-IFRS

한국회계기준원(KASB)은 K-IFRS 기준서와 기준서 관련 자료의 중심 source다. KASB 기준서 페이지는
시행 중 기준서와 기준서 연혁을 제공한다. 이 레포의 기존 강점도 여기에 있다.

Ingestion implication:

- 현재 K-IFRS 인덱스를 먼저 quality refresh한다.
- 기준서 본문과 연혁/개정 정보는 별도 document type으로 나눈다.
- 저작권 때문에 공개 레포에는 원문/임베딩을 넣지 않는다.

### KASB/FSS/FSC interpretive material

회계처리 실무에서는 기준서 문단만으로 부족한 경우가 많다. 질의회신, 회계감독 자료, 적용 사례는
판단 맥락을 보완한다.

Ingestion implication:

- source별 metadata를 강하게 잡아야 한다: 발행기관, 발행일, 문서 유형, 적용 기준서, binding 여부.
- 답변에서는 K-IFRS 문단과 interpretive material을 분리해 보여줘야 한다.
- interpretive material이 기준서 본문을 대체하지 못한다는 policy가 필요하다.

### Audit standards / KICPA / KAASB

감사팀 업무는 회계처리 판단과 다르다. 감사 계획, 위험평가, 분석적 절차, 감사증거, 조서화에는
감사기준 계열 source가 필요하다.

Ingestion implication:

- F-ACC와 F-AUD namespace를 분리한다.
- 같은 거래라도 "회계처리" 답변과 "감사절차" 답변의 source priority가 다르다.
- 감사기준은 workflow 산출물도 review memo가 아니라 audit program / workpaper 형태로 바뀐다.

### Law / regulation

외감법, 상법, 자본시장법 등은 기준서와 다른 종류의 권위다. 회계처리 측정 자체보다 공시 의무,
감사 대상, 절차, 책임, 제출 요건에 영향을 준다.

Ingestion implication:

- law source는 조문 단위 chunking이 맞다.
- 시행령/시행규칙/개정 이력까지 provenance가 필요하다.
- 회계 답변에 법령을 섞을 때는 "회계처리 근거"와 "법적 요건"을 분리해야 한다.

### DART / OpenDART / XBRL

DART/OpenDART는 실제 회사 공시와 XBRL 재무제표 데이터를 가져오는 축이다. OpenDART developer guide는
단일/복수 회사 주요 계정, 원본 XBRL, XBRL taxonomy financial statements format 등을 API로 제공한다.

Ingestion implication:

- 이 축은 문서 RAG라기보다 structured data retrieval에 가깝다.
- 재무제표 후보, 감사 분석, peer comparison, disclosure example에 직접 연결된다.
- 제출자가 작성한 공시 데이터이므로 authoritative accounting rule처럼 취급하면 안 된다.

### Client-private material

실제 회계 업무에는 계약서, 회계정책, TB, 조서, management memo가 필요하다. 이 자료는 공개 데이터가
아니므로 local-only/private namespace로만 처리한다.

Ingestion implication:

- anonymized case intake schema가 먼저 필요하다.
- private source는 공개 test fixture와 분리한다.
- answer composer는 "client-provided fact"와 "authority evidence"를 구분해야 한다.

## First Source Expansion Candidates

RAG 품질 refresh 후 첫 ingestion 후보는 다음 순서가 합리적이다.

1. KASB/FSS interpretive material catalog: 회계 판단 품질에 직접 도움.
2. OpenDART/XBRL sample connector: 재무제표 draft와 감사 분석 기능에 바로 연결.
3. Law connector prototype: 외감법/상법/자본시장법 조문 단위 retrieval.
4. Audit standards namespace: F-AUD workflow가 커질 때 시작.

## References Checked

- KASB K-IFRS 기준서 페이지: https://www.kasb.or.kr/front/board/ingAccountingList.do
- IFAC Korea profile: https://www.ifac.org/about-ifac/membership/profile/korea
- IFAC KICPA member profile: https://www.ifac.org/about-ifac/membership/members/korean-institute-certified-public-accountants
- OpenDART developer guide: https://engopendart.fss.or.kr/guide/main.do?apiGrpCd=DE003
- DART English disclosure portal: https://englishdart.fss.or.kr/

