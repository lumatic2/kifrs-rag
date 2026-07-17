# Horizon: Portfolio Visualization Site

> Status: closed (2026-07-12)
> Created: 2026-07-12
> Previous: `docs/horizons/drift-watch-automation.md` (closed)
> Objective 링크: `docs/OBJECTIVE.md` — 성공기준 D축(포트폴리오)의 kifrs-rag 트랙 (사용자 발제 예외 3건째, 2026-07-12)
> Plan doc: `docs/plans/2026-07-12-portfolio-viz-site.md`

## Goal

kifrs-rag 지식 엔진을 **메타데이터만으로** 시각화한 공개 포트폴리오 사이트를 만들어
`kifrs.askewly.com`(Cloudflare, wrangler assets-only)에 배포한다. 콘텐츠 4종:
① 기준서 지도(100 기준서 계층·문단 규모) ② 참조 네트워크 그래프(기준서 간 상호참조)
③ eval 대시보드(recall/MRR 개선 곡선·dogfood 이력) ④ 아키텍처/파이프라인 스토리
(다운로드→파싱→임베딩→MCP→drift 감시). 스택 = Astro (정적 + 그래프·차트만 island).

**저작권 하드 경계**: 기준서 본문·문단 텍스트는 어떤 형태로도 사이트 데이터에 포함하지
않는다 — 번호·제목·개수·구조·참조 관계·지표만. export 단계에 public-safe gate 를 둔다.

## Why now

- drift 계열 완료로 엔진이 "살아있는 시스템"(감지·갱신 루프) 서사까지 갖춤 — 보여줄 것이 완성됨.
- 참조 그래프 추출은 `cross_reference` 테이블(스키마만)의 첫 실사용 — RAG 품질(관련 조항 탐색)에도 재사용되는 자산.
- ai-accounting-firm 공개 웹사이트(포트폴리오 정본 경로)와 별개의 kifrs-rag 단독 증거물.

## Milestones

### PV1. 데이터 레이어 — 메타데이터 export + 참조 추출 (P0)

Status: completed

- Deliverable: `scripts/export_web_data.py`(DB→`web/src/data/*.json`: 기준서 계층·문단 규모·
  eval 이력·파이프라인 통계) + 문단 본문에서 기준서 간 참조 추출(`cross_reference` 테이블
  적재 + 그래프 JSON) + **public-safe gate**(export 산출물에 문단 본문 문자열 미포함 검증 스크립트).
- Acceptance: export 실행으로 JSON 세트 생성 + gate PASS(synthetic 본문 주입 시 FAIL 확인) +
  cross_reference 행 수·그래프 노드/엣지 수 관측.

### PV2. Astro 사이트 구현 (P0)

Status: completed

- Deliverable: `web/` Astro 프로젝트 — 기준서 지도·참조 그래프(island)·eval 대시보드·
  아키텍처 스토리 4뷰. /frontend-design·dataviz 스킬 적용.
- Acceptance: `npm run build` 성공 + 로컬 프리뷰를 실제 브라우저(/browse)로 4뷰 E2E 확인.

### PV3. 배포 + 공개 검증 (P1)

Status: completed

- Deliverable: wrangler assets-only 배포(`kifrs.askewly.com` custom domain) + 배포 후
  라이브 URL 브라우저 검증 + 최종 public-safe 점검.
- Acceptance: 라이브 URL 4뷰 렌더 확인 + 배포 산출물 gate 재실행 PASS.

## Close criteria

- PV1~PV3 완료, `kifrs.askewly.com` 라이브.
- 기준서 본문 비노출 원칙이 gate 로 검증된 상태 유지 (배포 산출물 기준).
- 기존 품질 게이트 비퇴행 (cross_reference 적재가 검색 경로에 영향 없음 확인).

## Close Result

`portfolio_viz_live` (2026-07-12) — **https://kifrs.askewly.com 라이브**, changeset 6개(#40~#45).
4뷰(서가 히어로·참조 그래프 d3-force·eval 대시보드·파이프라인 스토리) 전부 실브라우저 E2E.
저작권 경계는 3중 검증: export gate 양방향(전수 17,244 문단 대조 — 초기 표본 방식이 주입을
놓쳐 전수로 강화) + 배포 산출물(dist) 재스캔 0건. 부수 자산: `cross_reference` 첫 적재
(1,850행/655쌍 — 향후 '관련 조항' 기능 재사용 가능).

크기 회고: PV1(2cs)·PV2(3cs) 적정, PV3(1cs)는 step 크기였음 — §A1 인플레 적발, 다음 같은
크기는 milestone 로 만들지 않는다.

## Objective 임팩트

성공기준 D축(포트폴리오)이 "블로그 발행" 수준에서 **공개 라이브 시각화 사이트**로 상향 —
ai-accounting-firm 공개 웹사이트(정본 경로)와 별개의 kifrs-rag 단독 증거물. 재배포 경로
(`export → gate → build → wrangler deploy`)가 레포에 박제되어 지표 갱신 시 사이트도 따라간다.

## Decision Log

- 콘텐츠 4종(지도+eval / 참조 그래프 / 아키텍처 스토리), 스택=Astro, 배포=Cloudflare
  askewly 서브도메인 — 사용자 확정 2026-07-12. drift 현황 배지는 미선택(제외).
- 데이터는 빌드타임 정적 임베드 — 서버·API 없음 (저작권·운영 부담 최소).
- 참조 추출 방식·그래프 렌더 라이브러리·서브도메인 정확 명칭(kifrs.askewly.com)은 구현 재량.
