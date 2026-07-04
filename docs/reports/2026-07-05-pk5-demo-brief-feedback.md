# PK5 Demo Brief and Feedback Questionnaire

> Date: 2026-07-05
> Horizon: `product-packaging-poc`
> Demo bundle: `docs/reports/demo-poc/MANIFEST.md`

## 10분 demo 목적

회계법인에 "K-IFRS RAG"를 검색 도구로 소개하지 않는다. 핵심 메시지는 다음이다.

> 이 도구는 기준서 문단을 찾아주는 데서 끝나지 않고, 복잡 거래의 판단·측정·분개·검토메모·주석 질문·
> 재무제표 표시 후보·감사 분석 질문까지 이어지는 decision-prep draft를 만든다.

## Demo script

### 0:00-1:00 — 문제 제기

- 현재 많은 AI 활용은 기준서 검색, 자료 요약, 문서 초안에 머문다.
- 회계법인 실무에서 더 부담이 큰 지점은 "이 거래를 어떻게 판단하고, 어떤 분개/표시/주석 질문으로
  가져갈 것인가"다.
- 이 PoC는 최종 결론이 아니라 회계사가 검토할 초안을 자동 생성한다.

### 1:00-4:00 — 1115 primary flow

열 파일:

- `docs/reports/demo-poc/1115-significant-financing-review-pack.md`
- `docs/reports/demo-poc/1115-repurchase-review-pack.md`

보여줄 것:

- 수익인식 path
- recognized revenue, financing effect, repurchase liability
- 수익, 매출채권, 이연금융수익, 금융부채, 금융비용 분개 초안
- review checklist와 human review questions

말할 포인트:

- 기준서 판단이 분개와 검토메모로 내려간다.
- 계약 원문, SSP, 지급조건 검토는 여전히 사람 책임으로 남는다.

### 4:00-6:00 — F/S draft candidates

열 파일:

- `docs/reports/demo-poc/statement-candidates.md`

보여줄 것:

- 수익 → 손익계산서 후보
- 계약부채/금융부채/매출채권 → 재무상태표 후보
- source standard, case id, source field가 남아 추적 가능함

말할 포인트:

- 재무제표를 완성하는 게 아니라, 표시 후보를 근거와 함께 정리한다.
- 회사별 TB, 계정 mapping, 중요성 판단은 사람과 회사 정책 영역이다.

### 6:00-8:00 — Audit analytics linkage

열 파일:

- `docs/reports/demo-poc/audit-analytics-note.md`
- `docs/reports/demo-poc/audit-facc-links.md`

보여줄 것:

- 수익 증가, 영업이익률 하락, 부채비율 상승 같은 finding
- finding과 1115 금융부채 candidate 연결
- audit boundary 문구

말할 포인트:

- 감사의견이나 KAM을 쓰는 것이 아니다.
- 분석적 절차 초안과 reviewer question을 만드는 보조 도구다.

### 8:00-9:00 — 1116 secondary card

열 파일:

- `docs/reports/demo-poc/1116-lease-review-pack.md`

보여줄 것:

- 사용권자산/리스부채 분개
- 리스 주석 초안
- 회사 정책/변동리스료/전대리스 review questions

말할 포인트:

- 리스처럼 직관적인 도메인에서도 같은 review-pack 패턴이 반복된다.

### 9:00-10:00 — Boundary and ask

말할 경계:

- 기준서 원문, DB, embedding은 배포하지 않는다.
- 사용자가 자기 기준서 자료를 로컬에서 인덱싱하는 구조다.
- 산출물은 decision-prep draft이며 회계사 검토를 대체하지 않는다.

요청할 것:

- 실제 회계자문/감사 업무에서 이 초안이 검토 시간을 줄이는지 피드백.
- 어느 단계가 가장 쓸모 있고 어느 단계가 위험한지 피드백.
- 다음 PoC에 넣을 실제 익명화 거래 유형 제안.

## Feedback questionnaire

### A. 업무 적합성

1. 이 demo는 회계법인의 어느 팀 업무에 가장 가까운가?
   - 회계자문/F-S support
   - 감사팀 회계이슈 검토
   - 결산 지원
   - 기타
2. 실제 업무에서 가장 시간이 걸리는 단계는 무엇인가?
   - 기준서 리서치
   - 사실관계 구조화
   - 분개/측정
   - 검토메모 작성
   - 주석/표시 검토
   - reviewer 질문 정리
3. 이 도구가 줄일 수 있을 것 같은 시간은 어느 단계인가?

### B. 산출물 품질

4. review pack의 구조는 상위자/감사인 리뷰에 충분히 읽기 쉬운가?
5. 분개 초안은 검토 시작점으로 쓸 만한가?
6. F/S 표시 후보는 계정 mapping 전 단계로 의미가 있는가?
7. audit analytics finding은 감사 질문 초안으로 쓸 만한가?

### C. 신뢰와 위험

8. 어떤 산출물은 자동화되면 위험하다고 느껴지는가?
9. 어떤 human review question이 반드시 더 필요하다고 보는가?
10. 기준서 citation보다 더 필요한 근거는 무엇인가?
    - 계약 원문 조항
    - 회사 회계정책
    - 과거 감사조서
    - 공정가치/외부 평가 자료
    - 기타

### D. 도입 장벽

11. 로컬 도구킷 형태가 법인/개인 실험에 적합한가?
12. 기준서 원문과 DB를 직접 인덱싱해야 하는 전제가 수용 가능한가?
13. 실제 PoC를 하려면 어떤 보안/권한/데이터 반출 조건이 필요한가?

### E. 다음 PoC 후보

14. 다음에 넣어야 할 거래 유형은 무엇인가?
15. 1115/1116/1109 중 어느 도메인이 가장 설득력 있는가?
16. 감사 분석적 절차는 독립 기능으로 쓸 가치가 있는가, 아니면 회계이슈 review pack의 부속 기능이면 충분한가?

## Demo decision

이 horizon의 packaging PoC는 "배포 가능한 제품"이 아니라 **법인 소개/피드백 수집용 demo pack**으로 닫는다.
다음 실제 제품화 판단은 회계사 피드백을 받은 뒤 한다.
