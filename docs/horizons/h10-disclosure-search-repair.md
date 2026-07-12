# Horizon: H10 Disclosure Search Repair

> Status: active
> Created: 2026-07-12
> Previous: `docs/horizons/portfolio-viz-site.md` (closed)
> Objective 링크: `docs/OBJECTIVE.md` — issue-back → 수리 루프 (2회전째, 정규 입력)
> Input: `BACKLOG.md` Issue-back Queue #4 (2026-07-12(b) H10 C8-2 공시 체크리스트 실험, 원본:
> `~/projects/ai-accounting-firm/docs/cases/2026-07-12-disc-checklist/mcp-log.md`)
> Plan doc: `docs/plans/2026-07-12-h10-disclosure-search-repair.md`

## Goal

H10 실험(5번째 실소비, 24회 호출)이 확인한 구조 결함 1건을 수리한다:

**[신규] search() 에 절(section) 필터가 없어 "공시 절만" 조회의 정밀도가 구조적으로 낮다** —
5개 기준서(1116/1115/1107/1016/1012) 전수에서 reranked·hierarchical 공통으로 공시 절 문단이
BC·측정 절에 밀림(1016은 공시 8문단 중 5개가 top-20 밖). `paragraph.section` 라벨은 이미
존재·정상이므로 `search(section=...)` 필터를 추가하면 구조적으로 해소.

부수 표면화: 실험이 실증한 정본 경로(전략 A — `list_sections → get_context`, 5/5 완전 회수)를
/accounting 에 공시·절 단위 수집 권장 경로로 문서화.

## Why now

- 소비자 판정은 "승격 조건 아님(안정적 우회 존재)"이나, 공시 업무형 소비(주석 체크리스트 등)는
  F-ACC review pack 의 반복 패턴 — 검색 UX 개선의 실효가 크고 재현 방법이 명세돼 있음.
- 기수리 3건 회귀 없음이 4개 사례에서 반복 확인됨 — 수리 루프 신뢰 유지.

## Milestones

### DS1. search `section` 필터 (P0)

Status: active

- Deliverable: `search(query, standard, section, limit, mode)` — 전 모드(lexical/semantic/
  hybrid/hierarchical/reranked)에서 `paragraph.section` LIKE 부분일치 필터. store/embed 검색
  함수에 파라미터 관통 + tool docstring(1115/1107처럼 라벨 분산 기준서 주의 포함).
- Acceptance: mcp-log 재현 쿼리(§7·§15·§17·§22)에 `section="공시"` 적용 시 공시 절 문단 회수
  개선 관측(±기준: 1016 73~79 중 top-20 노출 3→6+ 등) + 필터 미사용 경로 eval 비퇴행 +
  존재하지 않는 section 은 빈 결과(오류 아님).

### DS2. 정본 경로 표면화 + 재현 close gate (P1)

Status: pending

- Deliverable: /accounting SKILL.md 에 "절 단위 수집 = list_sections→get_context 정본 +
  search(section=) 보조" 안내 + mcp-log 재현 4쿼리 before/after 기록 close report.
- Acceptance: 재현 기록에서 개선 확인 + 기존 tool smoke·focused pytest 비퇴행.

## Close criteria

- DS1·DS2 완료 + 품질 게이트 비퇴행. ai-accounting-firm 쪽 재소비 검증은 그쪽 레포 세션 몫 —
  이 horizon 은 재현 가능한 개선 증거까지 책임진다.

## Decision Log

- 필터 방식 = `section` 부분일치 (소비자 제안 두 안 중) — 기존 `paragraph.section` 데이터
  그대로, 신규 분류 체계 불요, 공시 외 절에도 일반화. `paragraph_type` 파생 분류는 라벨 분산
  (1115/1107) 문제를 해결하지 못하면서 유지비만 추가라 기각.
- BC 감점(_BC_DEMOTE) 추가 강화는 하지 않음 — IB2 에서 캘리브레이션된 값, 전역 변경은 eval
  재캘리브레이션 비용이 크고 section 필터가 니즈를 직접 해결.
