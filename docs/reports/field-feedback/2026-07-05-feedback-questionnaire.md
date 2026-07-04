# Field Feedback Questionnaire

> Date: 2026-07-05
> Use with: `docs/reports/field-feedback/2026-07-05-demo-brief.md`
> Demo bundle: `docs/reports/demo-poc/`

## 응답 전제

이 질문지는 제품 도입 여부를 묻기 위한 영업 설문이 아니다. 회계사가 demo 산출물을 보고 실제 업무에서
검토 시간을 줄일 수 있는지, 어떤 위험이 있는지, 다음 PoC에 어떤 익명화 사례를 넣어야 하는지 판단하기
위한 피드백 수집지다.

점수 문항은 1~5점으로 답한다.

- 1 = 전혀 아니다
- 3 = 조건부 가능
- 5 = 매우 그렇다

## A. 정확성 / 근거

1. 1115 review pack의 판단 흐름이 실제 수익인식 검토 순서와 맞는가? (1~5)
2. 1116 review pack의 리스 식별, 분개, 주석 질문 흐름이 실제 검토 순서와 맞는가? (1~5)
3. `evidence-boundary.md`처럼 primary K-IFRS evidence와 external evidence를 나눠 보여주는 방식이 신뢰 형성에 도움이 되는가? (1~5)
4. 기준서 citation 외에 반드시 추가되어야 하는 근거는 무엇인가?
   - 계약 원문 조항
   - 회사 회계정책
   - 과거 감사조서
   - 외부 평가자료
   - DART/공시 원문
   - 기타
5. 현재 demo에서 근거가 부족하거나 오해될 수 있는 부분은 어디인가?

## B. 실무 유용성

6. 이 demo는 어느 팀 업무에 가장 가깝다고 보는가?
   - 회계자문 / F-S support
   - 감사팀 회계이슈 검토
   - 결산 지원
   - 내부회계 / K-SOX
   - 기타
7. 실제 업무에서 가장 시간이 줄어들 가능성이 큰 산출물은 무엇인가?
   - review pack
   - 분개 초안
   - statement draft candidates
   - audit analytics note
   - evidence boundary
   - human review questions
8. `statement-candidates.md`의 Evidence column이 표시 후보 검토에 도움이 되는가? (1~5)
9. synthetic fact evidence가 붙어 있다는 표시가 충분히 명확한가? (1~5)
10. 이 산출물을 실제 업무 초안으로 쓴다면 어떤 입력 자료가 더 필요할까?

## C. 검토 부담

11. review pack을 상위자/파트너가 읽기 쉬운 구조라고 보는가? (1~5)
12. 사람이 반드시 다시 검토해야 하는 section이 명확히 보이는가? (1~5)
13. 현재 산출물이 오히려 검토 부담을 늘릴 수 있는 지점은 어디인가?
14. human review questions 중 실제로 유용한 질문과 불필요한 질문을 구분해달라.
15. 이 demo를 실무에서 쓰려면 reviewer checklist에 어떤 항목이 추가되어야 하는가?

## D. 위험 / 통제

16. 자동화되면 가장 위험하다고 느껴지는 부분은 무엇인가?
   - 회계 판단 결론
   - 금액 측정
   - 분개 초안
   - 재무제표 표시 후보
   - 감사 분석 finding
   - 외부 근거 표시
17. 외부 evidence가 primary K-IFRS evidence와 분리되어 있다는 점이 충분히 명확한가? (1~5)
18. synthetic DART-like fact가 실제 회사 수치로 오해될 위험이 있는가? (1~5)
19. 로컬 도구킷 형태에서 필요한 보안/권한/데이터 반출 조건은 무엇인가?
20. 이 도구가 절대 자동으로 하면 안 되는 작업은 무엇인가?

## E. 다음 PoC 후보

21. 다음 PoC에 넣을 실제 익명화 거래 유형은 무엇이 좋은가?
22. 1115, 1116, 1109 중 어느 도메인이 법인 소개에 가장 설득력 있는가? 이유는?
23. 공정가치/손상/연결/확정급여 중 다음으로 확장할 가치가 큰 영역은 무엇인가?
24. audit analytics는 독립 기능으로 볼 가치가 있는가, 아니면 F-ACC review pack의 보조 기능이면 충분한가?
25. 다음 demo에서 반드시 보여줘야 하는 한 가지 개선사항은 무엇인가?

## Follow-up Decision

피드백 후 다음 중 하나를 선택한다.

1. `real-anonymized-transaction-poc` — 익명화 실제 거래 1건으로 demo를 재구성한다.
2. `firm-introduction-material` — 법인 소개용 자료와 10분 발표 deck을 만든다.
3. `runtime-hardening` — 정확성/위험 피드백을 반영해 엔진과 evidence boundary를 강화한다.
4. `source-expansion` — 실제 DART/KASB/FSS/law connector 후보를 더 구체화한다.

