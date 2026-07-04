# PK1 Demo Scenario Selection

> Date: 2026-07-05
> Horizon: `product-packaging-poc`
> Step: PK1 — demo scenario selection

## 결론

10분 demo의 중심 흐름은 **1115 수익인식 → 재무제표 표시 후보 → 감사 분석적 절차 연결**로 잡는다.
보조 카드로 1116 리스 review pack을 짧게 보여준다.

## 왜 1115 중심인가

회계법인 소개에서 가장 설명이 쉬운 문장은 다음이다.

> "복잡한 수익 계약을 넣으면 5단계 판단, 분개, 검토메모, 주석 질문, 재무제표 표시 후보가 나오고,
> 그 숫자가 감사 분석적 절차의 이상징후 질문과도 연결됩니다."

이 흐름은 단순 RAG와 차이가 분명하다.

- RAG: 기준서 문단을 찾아준다.
- 이 demo: 판단 → 측정 → 분개 → 검토메모 → F/S 표시 후보 → 감사 질문까지 이어진다.

## 선택한 demo flow

### Primary flow — 1115 significant financing / repurchase

추천 입력:

- `scenario_03_significant_financing`
- `scenario_04_repurchase_call_option`

보여줄 output:

1. 1115 revenue decision path
2. measurement: recognized revenue, financing effect, repurchase liability
3. journal entries: 수익, 매출채권, 이연금융수익, 금융부채, 금융비용
4. review memo / review pack
5. statement draft candidates
6. audit anomaly finding linkage

이 flow가 좋은 이유:

- 수익, 금융요소, 금융부채가 동시에 보여서 회계 판단의 깊이가 드러난다.
- F/S draft와 F-AUD linkage까지 자연스럽게 연결된다.
- 기준서 원문 없이도 invented fixture로 공개 demo가 가능하다.

### Secondary flow — 1116 lease review pack

추천 입력:

- `scenario_01_simple_office_lease`

보여줄 output:

1. 리스 판단 summary
2. 사용권자산/리스부채 최초분개
3. 리스 주석 초안
4. review checklist

이 flow가 좋은 이유:

- 회계자문팀 workpaper pack의 제품성이 눈에 잘 보인다.
- 1115 primary flow가 복잡하면 1116은 직관적인 보조 카드가 된다.

## 제외한 flow

- 1109 전체 10-fixture demo: 강력하지만 10분 demo에는 분류 경로가 많아 산만하다.
- DART disclosure 대사: 외부 source와 파싱 설명이 끼어 demo가 길어진다.
- full audit analytics만 단독 demo: K-IFRS 판단 엔진과의 차별성이 약해진다.
- fair value/employee benefits: 아직 review pack surface가 부족하다.

## 10분 demo 구성

| 시간 | 내용 | 산출물 |
|---:|---|---|
| 0:00-1:00 | 문제 제기 | 회계법인 AI가 리서치에 머무는 지점 설명 |
| 1:00-4:00 | 1115 primary flow | 판단 path, measurement, journal entries |
| 4:00-6:00 | review pack | 검토메모, checklist, human review questions |
| 6:00-7:30 | F/S draft | 수익/계약부채/금융부채/금융비용 후보 |
| 7:30-8:30 | audit analytics linkage | 부채비율/영업이익률 finding과 F-ACC candidate 연결 |
| 8:30-9:30 | 1116 secondary card | 사용권자산/리스부채/주석 초안 |
| 9:30-10:00 | boundary | 기준서 원문/DB 비배포, 사람 검토 책임, PoC 질문 |

## 다음 step

PK2는 이 flow를 실행하는 demo command surface를 만든다. 권장 형태:

```powershell
python -m scripts.demo_poc --scenario revenue-financing
```

출력은 markdown files로 남긴다.
