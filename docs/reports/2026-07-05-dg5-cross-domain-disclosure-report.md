# DG5 — Cross-domain Disclosure Report

> Date: 2026-07-05
> Horizon: `f-acc-disclosure-generalization`

## 한 문장 결과

1116, 1115, 1109 산출물을 공통 `DisclosureChecklistItem` surface로 변환했고, 1115/1109는 review pack
기반 disclosure skeleton까지 생성된다.

## 도메인별 결과

| 도메인 | 입력 surface | 자동 후보 | 사람 보완 경계 | 결과 |
|---|---|---:|---:|---|
| 1116 리스 | disclosure requirement 11개 | 8 | 3 | 기존 1116 주석 요구항목을 common schema로 adapter |
| 1115 수익 | review pack 4개 | 4 pack | 각 pack 1 human action | 수익인식 판단/측정/입력검토 skeleton 생성 |
| 1109 금융상품 | review pack 10개 | 6 pack | 4 pack + 자동 pack human action | 분류/측정/위험자료 skeleton 생성 |

## 구현 evidence

| 단계 | 산출물 |
|---|---|
| DG1 | `docs/reports/2026-07-05-dg1-disclosure-surface-inventory.md` |
| DG2 | `kifrs/workflows/disclosure/schema.py`, `adapters.py`, `tests/test_disclosure_common.py` |
| DG3 | `kifrs/workflows/kifrs1115/disclosure.py`, `tests/test_1115_disclosure.py` |
| DG4 | `kifrs/workflows/kifrs1109/disclosure.py`, `tests/test_1109_disclosure.py` |

## 제품 의미

이제 F-ACC pack은 검토메모/분개뿐 아니라 주석 checklist surface까지 가진다. 1116은 정량 주석 항목,
1115는 수익인식 판단과 측정, 1109는 분류와 금융위험/공정가치 자료 요청으로 출발점은 다르지만,
사용자에게 보이는 구조는 같다.

```text
자동 산출 후보
사람 보완 필요
근거/citation
```

## 남은 경계

- 실제 회사 주석 문구와 회계정책 서술은 사람이 보완해야 한다.
- 1109 금융위험 주석은 회사 전체 위험관리 자료가 필요하다.
- 1115 수익 주석은 계약 포트폴리오와 유의적 판단 disclosure가 필요하다.
- DART 원문 대사는 local-only 자료와 별도 parser 품질에 의존한다.

## 다음 sequence

다음 horizon은 `f-acc-1109-hardening`이다. 이유는 1109가 review pack 10개 중 6개 automated, 4개
NeedsHumanReview로 남아 있고, disclosure skeleton에서도 1109의 human boundary가 가장 넓다. 기존
제품 표면이 생겼으므로 이제 1109 잔여 특수 케이스를 줄이는 것이 품질 향상에 가장 직접적이다.
