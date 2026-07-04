# Known Limitations and Human-Review Boundary

> Date: 2026-07-05
> Use before: field feedback demo

## 한 줄 경계

이 demo는 회계사 검토를 빠르게 시작하게 하는 decision-prep draft다. 회계 판단, 감사 판단, 서명 책임을
자동화하거나 대체하지 않는다.

## 1. 데이터 / 저작권 경계

포함하지 않는 것:

- K-IFRS 기준서 원문
- 기준서 파싱 DB
- embedding/vector store
- 회계사 시험 dogfood 문항
- KASB/FSS 질의회신 본문
- 법령 조문 본문
- raw DART filing, XML, XBRL payload
- client-private 자료

현재 demo에 포함된 것은 public-safe synthetic fixture와 metadata/locator뿐이다.

## 2. 판단 책임 경계

자동화한 것:

- 구조화 fixture 기반 판단 경로 초안
- 분개 초안
- 검토메모 초안
- 재무제표 표시 후보
- 감사 분석 질문 후보
- external evidence boundary 표시

자동화하지 않은 것:

- 최종 회계처리 결론
- 계약 원문 해석 최종 판단
- 회사 회계정책 반영
- 중요성 판단
- 감사의견 또는 KAM 작성
- reviewer sign-off

회계사 검토는 항상 필요하다.

## 3. 외부 Evidence 경계

`evidence-boundary.md`의 외부 evidence는 세 그룹으로 표시된다.

- Supporting interpretation: KASB/FSS-style metadata seed
- Legal boundary: law locator seed
- Fact evidence: synthetic DART-like fact

중요한 제한:

- 외부 evidence는 primary K-IFRS evidence가 아니다.
- 외부 evidence는 회계 결론을 자동 확정하지 않는다.
- 외부 evidence는 source body가 아니라 locator/fact metadata다.
- 법령 locator는 법률 자문이나 세무 답변을 대체하지 않는다.

## 4. Synthetic Fact 경계

`statement-candidates.md`의 Evidence column에 나오는 DART-like fact는 synthetic fixture다.

의미하는 것:

- structured fact evidence를 재무제표 표시 후보에 연결할 수 있음을 보여준다.
- 나중에 실제 OpenDART connector를 붙일 때 필요한 output shape를 검증한다.

의미하지 않는 것:

- 실제 회사 공시를 검증했다는 뜻이 아니다.
- 실제 DART API payload가 저장되어 있다는 뜻이 아니다.
- 표시 후보 금액이 외부 공시와 대사되었다는 뜻이 아니다.

## 5. Audit Analytics 경계

audit analytics output은 분석적 절차 질문 후보다.

가능한 용도:

- 수익 증가, 이익률 하락, 부채비율 상승 같은 finding을 표시
- F-ACC statement candidate와 연결
- reviewer question 초안 생성

불가능한 용도:

- 감사의견 작성
- 감사위험 최종 평가
- 충분하고 적합한 감사증거 판단
- KAM 문구 확정

## 6. 다음 PoC에서 확인할 것

회계사 피드백 후 확인해야 할 것:

1. 실제 익명화 거래 1건으로 같은 flow가 유지되는가?
2. 계약 원문, 회사 정책, TB, DART 자료가 들어오면 어떤 입력 schema가 필요한가?
3. 외부 evidence boundary가 신뢰를 높이는가, 아니면 오히려 복잡하게 보이는가?
4. reviewer question이 실제 리뷰 시간을 줄이는가?
5. 어느 단계에서 human review gate를 더 강하게 표시해야 하는가?

