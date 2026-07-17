# 회계법인 서비스라인 지도 (Firm Service Map) Horizon

> Created: 2026-07-04
> ROADMAP goal id: `firm-service-map`
> Status: active
> Objective: `docs/OBJECTIVE.md`

## Why now

`practice-map`은 회계사 업무를 33개 task로 쪼개고 자동화 가능성을 판정했다. 그러나 사용자 점검대로
그 앞단의 회계법인 company/service-line map이 별도 산출물로 충분히 서 있지 않았다. 감사팀,
회계자문팀, 세무팀, 딜/밸류에이션, 내부회계/컨설팅은 고객·입력자료·산출물이 다르다. 같은
"회계처리 판단"이라도 감사팀에서는 이슈 검토 조서이고, 회계자문팀에서는 고객에게 낼 검토메모다.

이 차이를 먼저 세우지 않으면 다음 구현 후보가 "기준서 도메인"이나 "로컬 검증 쉬움" 위주로
빨리 좁혀지고, 실제 회계법인 PoC에서 어느 팀의 어떤 업무에 꽂을지 설명하기 어렵다. 따라서
프로덕트 패키징 전에 조직 지도와 팀별 workflow를 다시 세운다.

## Goal

회계법인의 주요 service-line을 지도화하고, 각 팀의 업무 흐름과 산출물을 기준으로 기존 33개 task와
AI insertion point를 재매핑한다. 그 결과로 다음 자동화 구현 후보를 "법인 팀/업무/산출물" 단위로
다시 고른다.

## Milestone candidates

1. **FM1 — 회계법인 company/service-line map** (completed, 2026-07-04)
   Big4·로컬 법인의 공개 서비스 구조를 기준으로 Audit, Accounting Advisory, Tax, Deal/FAS,
   Risk/K-SOX, Consulting/AI, ESG, Forensic 등 service-line v0를 만들고, 각 팀의 고객·산출물·AI
   insertion point를 정리한다.
2. **FM2 — 팀별 회계사 workflow 문서화** (completed, 2026-07-04)
   FM1의 service-line별로 junior/senior/manager가 실제로 처리하는 workflow를 자료수집 → 판단 →
   계산/대사 → 문서화 → 리뷰/커뮤니케이션 흐름으로 쓴다. 기존 `taxonomy.md` 33 task를 이 조직
   지도에 재매핑한다.
3. **FM3 — service-line 기반 AI 후보 재판정** (completed, 2026-07-04)
   기존 PM3 판정을 폐기하지 않고, service-line 관점으로 다시 정렬한다. 후보는 "Audit용", "Accounting
   Advisory용", "Tax-agent 이관", "Deal/FAS 후보", "내부자료 필요 보류"로 나눈다.
4. **FM4 — 다음 구현 horizon 선정**
   구현 후보 1~2개를 고른다. 선택 기준은 로컬 검증성뿐 아니라 법인 PoC 설명력, 산출물 명확성,
   현업 피드백 가능성이다.

## Close criteria

FM1~FM3가 닫히면 horizon 핵심이 닫힌다: company map, 팀별 workflow, service-line 기반 AI 후보
재판정이 모두 존재해야 한다. FM4는 다음 구현 horizon으로 넘길 후보를 확정하는 close boundary다.
PM2(현업 검증)는 가능해지는 시점에 별도 실행하되, 이 horizon의 문서가 질문지의 기준이 된다.

## Objective 임팩트 가설

이 horizon은 Objective의 축 1(업무 지도 커버리지)을 "task 목록"에서 "회계법인 팀/산출물 지도"로
한 단계 끌어올린다. 직접 구현 수치는 당장 늘지 않지만, 이후 자동화 확장이 법인 PoC 설명력을 갖게
되는지 판정하는 기반이다. 만약 FM3 이후에도 구현 후보가 B3/B5만 남는다면, 그때는 "리스/주석
도구킷"처럼 좁은 wedge 제품으로 방향을 다시 좁히는 신호로 본다.
