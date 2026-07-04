# Field Feedback Demo Brief

> Date: 2026-07-05
> Horizon: `field-feedback-ready-demo`
> Demo bundle: `docs/reports/demo-poc/MANIFEST.md`
> Command: `python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc`

## 목적

이 demo는 회계사에게 "K-IFRS 검색 도구"를 보여주기 위한 자료가 아니다. 핵심은 다음이다.

> 기준서 문단 검색에서 끝나지 않고, 수익인식 판단, 분개 초안, 검토메모, 재무제표 표시 후보,
> 감사 분석 질문, 외부 근거 boundary까지 이어지는 decision-prep draft가 실제 업무 검토 시작점으로
> 쓸 만한지 확인한다.

이 산출물은 회계사 검토를 대체하지 않는다. 피드백 요청의 초점은 "정답 여부를 최종 판정해달라"가 아니라,
실제 회계자문/F-S support/감사 회계이슈 검토 업무에서 검토 시간을 줄일 수 있는지, 어떤 부분이 위험한지,
다음 PoC에 어떤 실제 익명화 사례를 넣어야 하는지다.

## 10분 Demo Flow

### 0:00-1:00 — 문제 제기

열 파일:

- `docs/reports/demo-poc/index.md`

말할 포인트:

- 많은 AI 활용은 기준서 검색, 요약, 문서 초안에 머문다.
- 회계법인 실무에서 더 부담이 큰 지점은 거래 판단, 측정, 분개, 표시, 주석 질문을 연결하는 것이다.
- 이 demo는 최종 결론이 아니라 reviewer가 검토할 decision-prep draft를 만든다.

### 1:00-3:00 — 1115 review pack

열 파일:

- `docs/reports/demo-poc/1115-significant-financing-review-pack.md`
- `docs/reports/demo-poc/1115-repurchase-review-pack.md`

볼 것:

- 수익인식 path
- 측정 결과와 분개 초안
- review checklist와 human review questions
- `## 외부 근거` section

말할 포인트:

- 기준서 판단이 검토메모와 분개 초안까지 내려간다.
- 외부 근거는 보조/경계/수치 사실로 분리되어 표시된다.
- 계약 원문, SSP, 지급조건, 회사 정책 검토는 여전히 사람 책임이다.

### 3:00-5:00 — Statement draft candidates

열 파일:

- `docs/reports/demo-poc/statement-candidates.md`

볼 것:

- 수익, 매출채권, 계약부채, 금융부채, 금융비용, 사용권자산, 리스부채 후보
- source standard, case id, source field
- `Evidence` column의 synthetic fact reference

말할 포인트:

- 재무제표를 완성하는 것이 아니라 표시 후보를 추적 가능하게 정리한다.
- `Evidence` column은 실제 회사 DART data가 아니라 public-safe synthetic fact evidence다.
- 회사별 TB, 계정 mapping, 중요성, 표시 정책은 별도 검토가 필요하다.

### 5:00-6:30 — Evidence boundary

열 파일:

- `docs/reports/demo-poc/evidence-boundary.md`

볼 것:

- Primary K-IFRS evidence
- Supporting interpretation
- Legal boundary
- Fact evidence

말할 포인트:

- K-IFRS 문단 근거와 외부 해석/법령/수치 근거를 같은 권위로 섞지 않는다.
- 외부 근거는 source body 없이 locator/fact metadata만 가진다.
- 법령과 수치 fact는 회계 결론을 자동 확정하지 않는다.

### 6:30-8:00 — Audit analytics linkage

열 파일:

- `docs/reports/demo-poc/audit-analytics-note.md`
- `docs/reports/demo-poc/audit-facc-links.md`

볼 것:

- 수익 증가, 영업이익률 하락, 부채비율 상승 finding
- finding과 F-ACC statement candidate 연결
- audit boundary 문구

말할 포인트:

- 감사의견이나 KAM을 쓰는 기능이 아니다.
- 분석적 절차 초안과 reviewer question을 만드는 보조 기능이다.

### 8:00-9:00 — 1116 secondary card

열 파일:

- `docs/reports/demo-poc/1116-lease-review-pack.md`

볼 것:

- 사용권자산/리스부채 분개
- 리스 주석 초안
- 회사 정책/변동리스료/전대리스 review questions
- 같은 external evidence panel 반복

말할 포인트:

- 1115뿐 아니라 1116에서도 같은 review-pack 구조가 반복된다.
- 도메인을 늘리더라도 "판단-분개-검토메모-주석/표시-근거 boundary" 패턴을 유지한다.

### 9:00-10:00 — Feedback ask

요청할 것:

- 실제 업무에서 가장 쓸모 있는 section이 무엇인지.
- 자동화되면 위험한 section이 무엇인지.
- reviewer가 반드시 추가로 확인해야 할 질문이 무엇인지.
- 다음 PoC에 넣을 익명화 거래 유형이 무엇인지.

## Demo Boundary

- 기준서 원문, 파싱 DB, embedding, dogfood 자료는 포함하지 않는다.
- KASB/FSS 질의회신 본문, 법령 조문, raw DART filing은 포함하지 않는다.
- demo의 DART-like fact는 synthetic fixture다.
- 산출물은 decision-prep draft이며 회계사 검토를 대체하지 않는다.
- 최종 회계 판단, 감사의견, 서명 책임은 사람에게 남는다.

## 피드백 받을 때의 질문 방식

좋지 않은 질문:

- "이게 맞나요?"
- "이걸 도입할 수 있나요?"

좋은 질문:

- "이 산출물 중 실제 검토 시간을 줄일 가능성이 큰 부분은 어디인가요?"
- "상위자/파트너 리뷰에서 바로 막힐 부분은 어디인가요?"
- "이 demo가 실제 업무에 가까워지려면 어떤 입력 자료가 더 필요하나요?"
- "다음 익명화 사례로 어떤 거래를 넣으면 설득력이 생기나요?"

