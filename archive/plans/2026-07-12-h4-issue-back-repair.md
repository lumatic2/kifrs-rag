# Plan: H4 Issue-back Repair

> Created: 2026-07-12
> 위계: `docs/OBJECTIVE.md` → `docs/horizons/h4-issue-back-repair.md` → 이 plan
> 산출물: changeset (전 milestone 공통) + 재현/close report

## Scope 경계

- 이번 run이 닫을 범위: IB1 → IB2 → IB3 (horizon 전체, horizon-run 연쇄).
- 중단점: 각 milestone 검증 PASS / blocked·error / 새 사용자 소유 결정 출현.
- 제외: ai-accounting-firm 쪽 H4 재실행과 f-acc-task-01 승격(그쪽 레포 별도 세션),
  retriever default promotion 재판단(별도 issue-back 필요).

## Step 트리

- [x] **IB1 리픽싱 계열 검색 수리** (changeset 2개)
  - [x] IB1-a term_bridge user_note 등록 + BC 임베딩 진단 — "리픽싱↔전환가액 조정/행사가격 조정"(anchor 1001-한138.5),
        "고정 대 고정↔확정 수량·확정 금액"(anchor 1032-16) v2 seed 추가; 1001 BC 문단의 embedding 존재 여부 진단 기록
        (verify: `search("전환가액 조정 리픽싱 희석 방지 조항", mode=hybrid, 필터 없음)`과 reranked에서 1001-한138.5 계열 top-10 도달)
  - [x] IB1-b standard 필터 함정 안내 — search tool 설명(mcp_server.py docstring) + /accounting SKILL.md에
        "낮은 신뢰도(top score 낮음/정답 미도달 의심) 시 standard 필터 해제 재검색" 규칙 명시
        (verify: 두 표면 diff 확인 + mcp-log #7 재현 시나리오를 report에 기록)
- [x] **IB2 파싱 수리** (changeset 2개 + 재인제스트)
  - [x] IB2-a BC(결론도출근거) 세분화 재파싱 — 1001 BC 통짜 문단을 한BC 문단 번호 단위로 분리, 재인제스트(재임베딩 포함)
        (verify: `get_paragraph(1001, "한BC104.1")` 단독 반환 + `get_context(1001, ...)` 반환 크기 정상)
  - [x] IB2-b `list_sections` 섹션 제목 추출 수리 — parse.py 제목 추출 로직 점검·수정
        (verify: `list_sections(1032)`/`list_sections(1109)` 제목 무결 — "는 금융상품"/"택권" 류 잘림 없음)
  - [x] IB2 통합 verify: 문단 수 비퇴행(8,328 기준 — BC 세분화 증가분은 설명 가능해야 함) +
        `quality_preflight.py` ok + retrieval eval 비퇴행
- [x] **IB3 H4 재검증 close gate** (changeset 1개)
  - [x] mcp-log 실패/부분 사례(#5 고정 대 고정, #7/#11 리픽싱, #15 BC 과대) 동일 쿼리 재현 → public-safe report 작성 +
        horizon close + ai-accounting-firm handoff 한 줄
        (verify: 재현 기록에서 기본 경로(hybrid/reranked) 도달 확인, `docs/reports/2026-07-12-h4-issue-back-repair-close-report.md`)

## 결정 로그

- **#1 수리 방향**: ① term_bridge + ② 필터 안내 + ③ BC 임베딩 진단 전부 IB1 포함 — handoff(사용자 기록) 후보 그대로. 확정.
- **#2 수리 방식**: BC 세분화 재파싱 우선(근본 수리), 원문 구조상 불가하면 스니펫 반환 옵션 fallback — 추천안, 계획 승인에 포함.
- **재인제스트 범위**: parse.py 수정은 전 기준서 재파싱을 유발할 수 있음 — 문단 수·eval 비퇴행 게이트로 방어. 확정.
- 그 외 실행 중 예상 사용자 결정: 없음 (secret·외부연동·스코프 변경 없음).

## 완료 기록 (2026-07-12)

- IB1~IB3 전부 완료, horizon closed. 계획 대비 편차: IB2는 changeset 2개 계획 -> 1개 통합(같은 파일·같은 재인제스트 사이클) + embed.py BC 감점 추가(비퇴행 게이트 대응, 계획에 없던 필수 수리). IB3는 changeset 없이 기록형 close report로 마감.
