# IB2 — 파싱 수리: BC 세분화 + 섹션 제목 (H4 issue-back)

> Date: 2026-07-12
> Milestone: IB2 (`docs/horizons/h4-issue-back-repair.md`)
> Input: mcp-log #15(BC 통짜 문단), #1/#2(섹션 제목 잘림)
> Public-safe: 문단 번호·수량·점수만 기록.

## 결함과 원인

1. **BC 통짜 문단** — `BC1`/`한BC104.1`/`BCE.15`/`DO1` 등 결론도출근거 계열 번호가 파서의
   어떤 문단 정규식에도 매치되지 않아(부록 패턴은 단일 문자 한정) 직전 문단에 통째 흡수.
   1001 `1#2`=32,357자 등. `get_context` 1회에 수만 자 반환.
2. **섹션 제목 잘림** — 두 형태:
   (a) 진짜 제목이 PDF에서 두 줄로 감기고 앞줄(전폭 ~33자)이 30자 제한에 걸려 뒷조각만
   채택 — 1109 "택권"(원제: "금융자산을 당기손익-공정가치 측정 항목으로 지정할 수 있는 선택권")
   (b) 본문 wrap 마지막 조각이 문단 번호 직전에 위치해 제목으로 오탐 — 1032 "는 금융상품"
   (풋가능 금융상품 정의문 조각), 1001 "체 분류한 영업이익…"(한138.4 목록 조각).

## 수리 (changeset `20260712-ib2-parse-bc-sections`)

- `kifrs/parse.py`: ① BC 계열 정규식(`BC[A-Z]?` + 한BC + BC 구간 내 DO/IN) + BC 구간 진입 후
  일반 번호 오매치 차단 ② 감긴 제목 후방 join(직전 줄이 전폭 25~40자 + heading 문자셋 +
  문장 미종결 + 그 앞줄 문장 종결일 때) ③ 본문 조각 오탐 차단(직전 줄 전폭+문장 미종결이면
  거부, 조사 시작 줄 거부)
- `tests/test_parse_bc_sections.py`: 합성 fixture 7건 (실측 패턴 재현)
- 재인제스트: `parse --all`(100 기준서) → `ingest.py` → `.venv/Scripts/python -m kifrs.embed build`(GPU)
  → orphan embedding 정리

## 검증 결과

| 항목 | 수리 전 | 수리 후 |
|---|---|---|
| 문단 수 | 8,298 | 17,896 (+9,598 = 정확히 BC/DO/IN 신규분, 감소 기준서 0) |
| 임베딩 커버 | 8,298 (100%) | 17,896 (100%, orphan 정리 후) |
| 1001 최대 문단 | 32,357자 (`1#2` BC blob) | 13,802자 (BC 분리 후, 1001 BC 246개 개별화) |
| `get_paragraph(1001, "한BC104.1")` | 불가(문단 없음) | 단독 반환 (658자, 리픽싱 BC 원문) |
| `get_context(1001, "한138.5", 1)` | 수만 자 blob 포함 | 3문단 전부 정상 크기(최대 ~1.4k자) |
| `list_sections(1032)` | "는 금융상품"·"산시 발생하는 의무" 등 잘림 | 잘린 제목 0 + BC 섹션 구조 노출 |
| 리픽싱 reranked (필터 없음) | 1#4 blob rank 1 | **한BC104.1 rank 1 (0.875)**, 104.3 rank 2 |
| `quality_preflight.py` | ok | ok (focused/local-rag/authority/user_note 전부 통과) |
| focused pytest | — | `test_parse_bc_sections.py` + `test_store_search.py` 20 passed |
| retrieval eval (hybrid) | recall@10 0.7133 / @20 0.8867 / MRR 0.4635 | (아래 eval 절) |

### Retrieval eval 비퇴행 (goldset 50문항, k=20)

BC 9,598 문단을 그대로 후보 풀에 넣으면 본문 골드가 밀려 hybrid recall@20 0.887→0.760으로
**퇴행**했다 (per-item 분석: 골드가 rank 21~25로 밀리는 희석, 10/50 문항). 대응으로
`kifrs/embed.py`에 ① RRF 융합 시 BC/DO/IN 기여 가중치 `_BC_DEMOTE=0.5` ② 후보 풀 50→100
확대를 넣었다 (hybrid·hierarchical 공통, reranked는 hybrid 후보를 상속).

| hybrid (50문항) | BC 이전 | BC+감점 후 |
|---|---|---|
| recall@5 | 0.5467 | **0.5767** |
| recall@10 | 0.7133 | **0.7467** |
| recall@20 | 0.8867 | **0.9100** |
| MRR | 0.4635 | **0.4897** |
| nDCG@10 | 0.4824 | **0.5093** |

전 지표 비퇴행 + 개선 (풀 확대 효과 포함). 감점 후에도 리픽싱 reranked는 한BC104.1
rank 1(0.875) 유지 — 고유하게 관련된 BC는 여전히 도달 가능. reranked는 같은 조건의
직전 baseline이 없어(환경 이슈) BC 유무 전후 비교만 가능: 0.593/0.534 → 0.593/0.538 평탄.

## 잔여 한계 (수리 범위 밖, 기록)

- 30자 초과 단일 줄 제목(예: 1032 "부채와 자본(문단 AG13~AG14J, AG25~AG29A 참조)")은
  기존부터 미검출 — 구 파서는 그 자리에 깨진 조각을 넣었고, 새 파서는 직전 제목이 이어짐.
- 인접한 상위+하위 제목에서 상위가 25자 이상이면 드물게 join 노이즈(1109 1건 확인).
- 표 조각 제목 오탐("적립금 530 485") — 기존 존재 클래스, 빈도 낮음.
- 1109 부록 B 대형 문단(B7.2.4, 49k자)은 BC가 아니라 이번 범위 밖.

## 환경 이슈 (같은 세션에서 해결)

GPU torch(cu128)는 `.venv`에만 있음 — bare `python`(시스템 3.12, `+cpu`)으로 임베딩/eval 실행 시
조용히 CPU로 돌아 수십 분 소요. `CLAUDE.md` 한계 #4에 재발 함정 기록. 임베딩·eval·리랭킹은
`.venv/Scripts/python` 필수.
