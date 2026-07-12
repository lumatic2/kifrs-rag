# Plan: portfolio-viz-site

> Created: 2026-07-12
> Horizon: `docs/horizons/portfolio-viz-site.md` (active)
> Objective: `docs/OBJECTIVE.md` — 성공기준 D축(포트폴리오) kifrs-rag 트랙
> 산출물: 전부 changeset

## Step 트리

### PV1 — 데이터 레이어 (P0)

- [x] PV1-S1: `scripts/export_web_data.py` — DB→`web/src/data/*.json`(기준서 계층·문단 규모·eval 이력·파이프라인 통계) + public-safe gate 스크립트 (verify: export 실행 JSON 생성 + gate PASS + synthetic 본문 주입 시 gate FAIL)
- [x] PV1-S2: 기준서 간 참조 추출 — 문단 본문 "제NNNN호" 계열 언급 파싱 → `cross_reference` 적재 + 그래프 JSON export (verify: 행 수·노드/엣지 수 관측 + 알려진 참조(1116↔1109 등) 존재 확인 + 기존 검색 eval 비퇴행)

### PV2 — Astro 사이트 구현 (P0)

- [ ] PV2-S1: Astro scaffold + 공통 레이아웃/디자인 토큰(/frontend-design) + 기준서 지도 뷰 (verify: `npm run build` + /browse 렌더 확인)
- [ ] PV2-S2: 참조 네트워크 그래프 island (verify: /browse 인터랙션 확인)
- [ ] PV2-S3: eval 대시보드(dataviz 스킬) + 아키텍처/파이프라인 스토리 뷰 (verify: /browse 4뷰 전체 E2E)

### PV3 — 배포 + 공개 검증 (P1)

- [ ] PV3-S1: wrangler assets-only 배포 + `kifrs.askewly.com` custom domain + 라이브 검증 + 배포 산출물 public-safe gate 재실행 (verify: 라이브 URL 4뷰 렌더 + gate PASS)

## 중단점

- milestone 경계 커밋. 라이브 배포(PV3)는 gate PASS 없이 진행 금지.
- cross_reference 적재로 검색 eval 퇴행 시 정지·진단.

## 결정 로그

- 사용자 확정(2026-07-12): 콘텐츠 4종 / Astro / Cloudflare askewly 서브도메인. 잔여 사용자 소유
  결정 **없음** — 그래프 라이브러리·디자인 방향·참조 추출 정규식은 구현 재량.

## planning_gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  scope_posture: selective
  delegation_decision:
    remote_background_agents: skip
    reason: "단일 레포 정적 사이트 + 로컬 export — 검증 커맨드(/browse·gate) 명확, 자체검토 충분"
    target_roles: []
    execution_path: local_manual
  spec_delta: "새 horizon portfolio-viz-site (사용자 발제 예외 3건째) — horizon/plan doc + ROADMAP marker"
  perspectives:
    product: "포트폴리오 증거물 — 지도·그래프·지표·서사 4뷰로 엔진의 깊이를 비전문가에게도 전달"
    architecture: "빌드타임 정적 데이터 임베드, 서버 0 — Astro islands 로 인터랙션 국소화"
    security: "저작권 하드 경계 = public-safe gate (본문 문자열 미포함 자동 검증, 배포 전 필수)"
    qa: "gate 양방향(PASS/synthetic FAIL) + /browse 실브라우저 E2E + 라이브 URL 검증 + eval 비퇴행"
    skeptic: "참조 추출 정규식이 과추출(개정 경과규정의 타기준서 언급)할 수 있음 — 노이즈면 본문 참조만 필터"
  dod:
    - "PV1: export JSON + gate 양방향 + cross_reference 적재 관측"
    - "PV2: build 성공 + /browse 4뷰 E2E"
    - "PV3: kifrs.askewly.com 라이브 + 배포 산출물 gate PASS"
```
