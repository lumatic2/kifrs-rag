# Horizon: H4 Issue-back Repair

> Status: active
> Created: 2026-07-12
> Previous: `docs/horizons/demo-rehearsal-improvement-hardening.md` (closed)
> Objective 링크: `docs/OBJECTIVE.md` — "issue-back → 수리 루프" 성공 모습의 첫 실행
> Input: `BACKLOG.md` Issue-back Queue (2026-07-12 H4 RCPS 실험, 원본: `~/projects/ai-accounting-firm/docs/cases/2026-07-12-facc-rcps-memo/mcp-log.md`)

## Goal

ai-accounting-firm H4 RCPS 검토메모 실험(첫 실소비, kifrs MCP 21회 호출)에서 돌아온 결함 3건을 수리하고,
동일 조건 재현으로 수리를 검증한다:

1. **[중요] 리픽싱 계열 검색 실패** — 정답(1001-한138.5/한BC104.1)이 실재함에도 hybrid/semantic 반복 미도달,
   `search("리픽싱", lexical, 필터 없음)`로만 성공. **이 수리가 f-acc-task-01의 ax_possible 승격 조건.**
2. **[중간] BC(결론도출근거) 문단 단위 과대** — 1001 BC가 통짜 문단(수만 자)으로 반환, `get_context` 토큰 낭비.
3. **[경미] `list_sections` 섹션 제목 파싱 깨짐** — "는 금융상품", "택권" 등 잘린 제목.

## Why now

2026-07-12 Objective 재정렬 이후 새 horizon의 유일한 입력은 ai-accounting-firm 사용처 결함(issue-back)이다.
이 horizon은 그 규칙의 첫 실행이며, #1은 실소비에서 나온 유일한 사실상 실패다.

## Milestones

### IB1. 리픽싱 계열 검색 수리 (P0)

Status: active

- Deliverable: term_bridge user_note 등록("리픽싱↔전환가액 조정", "고정 대 고정↔확정 수량·확정 금액") +
  standard 필터 함정 안내(search tool 설명 + /accounting SKILL.md) + BC 파트 임베딩 존재/커버리지 진단
- Acceptance: 필터 없는 기본 경로(hybrid·reranked)에서 리픽싱 계열 쿼리가 1001-한138.5 계열에 도달

### IB2. 파싱 수리 — BC 세분화 + 섹션 제목 (P1)

Status: pending

- Deliverable: `kifrs/parse.py` BC(결론도출근거) 문단 세분화 재파싱 + `list_sections` 섹션 제목 추출 수리 + 재인제스트
- Acceptance: 1001 한BC 문단이 개별 조회 가능, 섹션 제목 무결, 문단 수·retrieval eval 비퇴행

### IB3. H4 재검증 close gate (P1)

Status: pending

- Deliverable: H4 RCPS 쿼리 세트 재현 기록 + horizon close report + ai-accounting-firm 재실행 handoff
- Acceptance: mcp-log의 실패/부분 사례(#5, #7, #11, #15)가 기본 경로에서 해소 확인

## Close criteria

- IB1~IB3 완료 + 기존 품질 게이트(quality_preflight, engine smoke, focused pytest) 비퇴행.
- ai-accounting-firm 쪽 H4 재실행(f-acc-task-01 `ax_conditional` → `ax_possible` 승격 판단)은 그쪽 레포에서
  별도 세션으로 수행 — 이 horizon은 재실행 가능한 상태(수리 + 재현 증거)까지 책임진다.

## Decision Log

- #1 수리 방향: 후보 ①(term_bridge 등록) + ②(필터 해제 재검색 안내) + ③(BC 임베딩 진단) 모두 IB1에 포함
  (CLAUDE.local.md handoff의 후보 3개 그대로 채택).
- #2 수리 방식: BC 세분화 재파싱 우선(근본 수리). 원문 구조상 세분화 불가 시 스니펫 반환 옵션 fallback.
- 재인제스트 범위: parse.py 변경이 전 기준서에 영향할 수 있으므로 문단 수·eval 비퇴행 게이트로 방어.
- 기준서 원문·DB·임베딩 비공개 원칙 불변 — 산출 report는 public-safe(문단 번호·점수만, 원문 인용 최소화).
