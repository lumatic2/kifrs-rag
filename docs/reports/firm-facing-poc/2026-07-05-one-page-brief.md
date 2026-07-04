# One-Page PoC Brief

> Accounting Intelligence local toolkit for K-IFRS decision-prep drafts

## 대상

1순위는 회계자문/F-S support 팀이다. 복잡 거래를 K-IFRS 기준으로 검토하고, 검토메모·분개·주석
초안을 만드는 업무에 맞춘다. 감사팀은 회계이슈 검토와 주석 요구사항 대사 보조 적용처로 둔다.

## 한 문장

기준서 검색 AI가 아니라, 거래 조건을 받아 **판단초안 + 분개 후보 + 주석 후보 + human-review 질문**을
남기는 로컬 회계 AI 도구킷이다.

## 현재 보여줄 수 있는 것

| 항목 | 보여주는 것 |
|---|---|
| 1115 review pack | 수익 계약의 significant financing/repurchase 판단초안 |
| 1116 review pack | 리스 계약 판단과 표시 후보 |
| statement candidates | 재무제표 표시 후보와 synthetic fact evidence |
| evidence boundary | K-IFRS 근거, 외부 evidence metadata, human-review boundary 분리 |
| readiness checker | 공개 산출물과 재현 명령이 실제로 통과하는지 확인 |

## 10분 소개 흐름

1. 회계법인 service-line map: 왜 F-ACC가 첫 PoC 대상인지 설명한다.
2. demo PoC bundle: review pack과 evidence boundary를 보여준다.
3. limitations: 최종 판단·서명·세무/법률 판단은 사람이 맡는다고 먼저 말한다.

## 30분 데모 흐름

1. demo bundle 재생성 명령 실행
2. 1115 review pack 확인
3. evidence boundary 확인
4. statement candidates 확인
5. 피드백 질문지 작성

## PoC 요청사항

1. 익명화된 복잡 거래 1건
2. 회계사 reviewer 1명
3. 평가 기준 3개: 시간 절감, 근거 추적성, human-review boundary

## 다음 결정

이 소개 자료의 다음 단계는 `real-anonymized-transaction-poc`이다. 실제 익명화 거래 1건으로 F-ACC
review pack을 만들고, 회계사 correction을 eval/backlog queue에 반영한다.
