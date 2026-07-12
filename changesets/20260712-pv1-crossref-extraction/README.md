# Changeset: PV1-S2 — 기준서 간 참조 추출 + 그래프 JSON

## Target

- ROADMAP milestone: PV1 — 데이터 레이어 (`portfolio-viz-site` horizon)
- Plan: `docs/plans/2026-07-12-portfolio-viz-site.md` PV1-S2

## Scope

- Files: `scripts/build_cross_references.py` (신규), `web/src/data/crossref.json` (산출물),
  `scripts/export_web_data.py` (crossref export 통합)
- Reason: 참조 네트워크 그래프의 데이터가 없음 — `cross_reference` 테이블은 스키마만.
- Expected effect: 문단 본문의 "기업회계기준서 제NNNN호" 계열 언급 → cross_reference 적재(문단
  단위, context 포함 — **DB 로컬 전용**) + 기준서 쌍 aggregate 그래프 JSON(from/to/weight 만) export.

## Contract

- Source of truth: `scripts/build_cross_references.py`. 재실행 idempotent(테이블 rebuild).
- Compatibility: 검색 경로는 cross_reference 를 읽지 않음 — 영향 없음(eval 로 확인).
  **context(주변 본문 스니펫)는 export 금지** — 그래프 JSON 은 from/to/weight aggregate 만.
- Out of scope: 그래프 시각화(PV2-S2), MCP get_related tool(향후 issue-back 판단).

## Verification

- [x] Targeted tests: 1,850 문단 참조 → 655 기준서 쌍 적재. 알려진 참조 존재 — 1116→1109(7),
      1109→1032(4), 1001→1109(10). 상위 엣지 타당성(1107→1109 55건 등)
- [x] CLI smoke: crossref.json 생성 + gate PASS (4파일 전수 대조 — context 미포함 확인)
- [x] Integrated smoke: hybrid eval recall@10 0.747 / @20 0.910 / MRR 0.488 — 비퇴행
- [x] Dirty-tree review: scripts + crossref.json + changeset 만

## Result

- Status: completed (2026-07-12)
- Evidence: 위 checklist 실행 로그, `web/src/data/crossref.json`
- Notes: cross_reference 테이블 첫 적재(스키마 전용 → 1,850행). context 는 DB 로컬 전용 —
  export 는 from/to/weight aggregate 만.
