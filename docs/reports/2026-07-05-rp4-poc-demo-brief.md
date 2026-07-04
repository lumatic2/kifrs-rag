# F-ACC Review Pack PoC Demo Brief

> Date: 2026-07-05
> Audience: 회계법인 Accounting Advisory / Financial Statement support 팀
> Demo scope: K-IFRS 1116 리스 계약 review pack

## 1. 한 문장 설명

리스 계약 조건과 지급 스케줄을 넣으면, K-IFRS 1116 검토메모, 최초분개, 주석 초안, 리뷰 checklist,
사람 검토 필요 항목을 하나의 회계자문 workpaper pack으로 묶어 내는 로컬 AI 도구다.

## 2. 왜 F-ACC인가

회계자문팀의 반복 병목은 단순 기준서 검색이 아니라 다음 산출물을 연결하는 일이다.

| workflow 단계 | 기존 업무 | demo에서 줄이는 부분 |
|---|---|---|
| 자료수집 | 계약 조건, 리스료 스케줄, 회사 정책 확인 | 입력 스키마에 맞춰 판단에 필요한 필드 정리 |
| 판단 | 리스 식별, 면제, 최초/후속 측정, 변경 처리 판단 | 기준서 근거가 붙은 판단 초안과 자동화 경계 표시 |
| 계산/분개 | 리스부채/사용권자산, 이자, 감가상각, 조정분개 | fixture 기반 계산 결과와 분개 초안 |
| 문서화 | 검토메모, 주석 초안, 리뷰노트 작성 | 검토메모 + 주석 + checklist를 같은 pack으로 생성 |
| 리뷰 | 매니저/파트너/감사인 질문 대응 | 사람 검토 질문과 추가자료 목록을 별도 queue로 표시 |

## 3. 현재 demo에서 되는 것

- 1116 fixture 10개 전체에서 review pack 생성 경로 검증
- 자동 생성: 9개 fixture
- 사람 검토 경계: 1개 fixture
- pack 구성: 판단 요약, 검토메모, 최초분개, 리스 주석 초안, 리뷰 checklist, 인용 목록
- 자동화된 리스이용자 pack은 회사 회계정책, 변동리스료, 전대리스, 판매후리스, 만기분석 보완 항목을 별도 표시
- 자동 판단이 멈춘 경우에도 실패 문구가 아니라 추가자료, 리뷰 질문, 기준서 처리 방향을 제시

## 4. Demo flow

1. 단순 사무실 리스 fixture를 입력한다.
2. 도구가 리스이용자 인식 경로를 판단하고 최초분개를 생성한다.
3. 같은 run에서 검토메모와 1116 주석 초안을 생성한다.
4. review checklist가 회사 특수 정책, 조건부 주석 항목, 표현 보완 지점을 표시한다.
5. 확장+축소 동시 변경 fixture를 입력한다.
6. 도구가 억지로 결론을 내지 않고 `NeedsHumanReview`로 멈춘 뒤, 필요한 추가자료와 리뷰 질문을 제시한다.

## 5. 사람이 계속 책임지는 경계

이 PoC는 최종 회계 판단을 대체하지 않는다.

- 계약 원문 해석, 경영진 의도, 별도 리스 여부 판단
- 중요성, 표시, 주석 문구의 회사별 톤
- 감사인 또는 고객과의 커뮤니케이션
- 최종 review, 서명, 책임

도구의 역할은 junior/senior가 초안을 만드는 시간을 줄이고, manager review 전에 빠뜨리기 쉬운 확인
항목을 workpaper queue로 노출하는 것이다.

## 6. PoC에서 확인할 질문

1. 이 pack 형식이 실제 회계자문팀 review memo / workpaper 흐름과 맞는가?
2. 현재 자동화 9/10 경계가 실무적으로 납득 가능한가?
3. `NeedsHumanReview` checklist의 추가자료·리뷰질문이 manager review 전에 유용한가?
4. 다음 demo 도메인은 1116 확장, 1115 수익, 1109 금융상품, 주석 대사 중 어디가 좋은가?
5. 입력 인터페이스는 엑셀 템플릿, 계약 요약 폼, 또는 기존 workpaper 양식 중 무엇이 적합한가?

## 7. 공개/비공개 경계

공개 repo에는 코드, 아키텍처, 테스트, 요약 리포트만 둔다. 기준서 원문, 파싱 DB, 임베딩, 회계사 기출
dogfood, 고객자료는 포함하지 않는다. 실제 PoC에서는 사용자가 보유한 자료를 로컬에서만 인덱싱하는
구조를 유지한다.

## 8. Evidence

- `kifrs/workflows/kifrs1116/review_pack.py`
- `tests/test_1116_review_pack.py`
- `docs/reports/2026-07-04-rp1-1116-review-pack-sample.md`
- `docs/reports/2026-07-04-rp2-1116-review-pack-fixture-summary.md`
- `docs/reports/2026-07-05-rp3-needs-human-review-checklist.md`

## 9. 다음 결정

RP4 이후 선택지는 세 가지다.

| 선택지 | 의미 | 추천 조건 |
|---|---|---|
| 회계사 인터뷰(PM2) | 실제 F-ACC/Audit 사용자에게 brief를 보여주고 입력·산출물 피드백을 받는다 | 접촉 가능한 회계사가 있으면 최우선 |
| PoC 패키징 | CLI/demo script, sample input, README를 정리해 10분 데모로 만든다 | 외부 소개 일정이 잡혔거나 곧 잡을 수 있으면 |
| 다음 도메인 구현 | 1115/1109/주석 대사 등으로 review pack 패턴을 확장한다 | 현업 피드백 없이 기술 커버리지를 늘리고 싶을 때 |
