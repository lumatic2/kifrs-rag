# Changeset: 20260712-ib1-repricing-term-bridge

## Target

- ROADMAP milestone: IB1 — 리픽싱 계열 검색 수리 (`docs/horizons/h4-issue-back-repair.md`)
- Plan: `docs/plans/2026-07-12-h4-issue-back-repair.md` IB1-a

## Scope

- Files: `scripts/seed_user_notes.py` (term_bridge seed 3건 추가)
- Reason: H4 RCPS 실소비(mcp-log #7/#11)에서 리픽싱 계열 쿼리가 정답(1001-한138.5)에 기본 경로로
  미도달. "리픽싱"/"리픽셔닝"(실무 용어)은 1001 BC(`1#4`)에만 존재하고, 한138.5 본문 어휘는
  "행사가격이 조정되는 조건"·"주가 변동"이라 어휘 불일치(CLAUDE.md 한계 #1 패턴).
  "고정 대 고정"도 본문 부재 확인(mcp-log #5) — 기준서 표현은 "확정 수량"·"확정 금액"(1032-16).
- Expected effect: expand_query()가 lexical(FTS)·semantic(qvec)·hybrid 전부에 적용되므로
  트리거 포함 쿼리가 한138.5/1032-16 본문 어휘로 확장되어 기본 경로 도달.

## Contract

- Source of truth: `scripts/seed_user_notes.py` SEEDS (user_note_v2 seed의 정본).
  DB row는 `--apply`로 파생 — DB 직접 INSERT 금지.
- Compatibility: additive seed 3건. 기존 20건 seed·legacy mirror 불변. idempotent 재실행 안전.
- Out of scope: standard 필터 안내(IB1-b 별도 changeset), BC 세분화 재파싱(IB2).

## BC 임베딩 진단 (IB1-a ③ — 계획된 진단 항목)

- 1001 BC 계열(`1#2`~`1#4` 등 `#` suffix 문단) 전부 embedding 존재(각 1 vector).
- 단 `1#2`=32,357자, `1#4`=5,576자 통짜 문단에 vector 1개 → 다주제 blob의 의미 희석으로
  semantic 매칭이 구조적으로 약함. 근본 수리는 IB2(BC 세분화 재파싱)에서 수행.
- 한BC 문단(한BC104.1 등)은 개별 paragraph row로 존재하지 않음 (`no LIKE '%BC%'` 0건).

## Verification

- [x] Targeted tests: `python -m pytest tests/test_user_note_v2_runtime.py -q` — 3 passed
- [x] CLI smoke: `python scripts/seed_user_notes.py --apply` inserted 3 → 재실행 new rows 0 (idempotent)
- [x] Integrated smoke: 재현 쿼리 3종 기본 경로 도달 —
      ① `search("전환가액 조정 리픽싱 희석 방지 조항", hybrid)` → 1001-한138.5 **rank 1** (수리 전: top-10 밖, 1#4 BC blob만 rank 1)
      ② `search("전환가액 조정 리픽셔닝 희석 방지 조항", hybrid)` → 1001-한138.5 **rank 1** (수리 전 mcp-log #7: 사실상 실패)
      ③ `search("고정 대 고정 확정수량 보통주 전환 지분상품 조건", hybrid)` → 1032-16 **rank 2**
- [x] Dirty-tree review: seed 파일 + changeset 만 변경. 비퇴행: `quality_preflight.py` ok (focused_pytest/local_rag_threshold_gate 등 전부 0)

## Result

- Status: completed
- Evidence: 위 Verification 재현 로그 (2026-07-12) + `data/kifrs.db` user_note_v2 23 rows
- Notes: expansion은 쿼리 시점 DB 조회라 MCP 서버 재시작 불필요. BC 임베딩 진단(③)은 위 섹션 —
  근본 수리는 IB2로 이관.
