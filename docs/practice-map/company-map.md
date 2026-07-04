# 회계법인 company/service-line map — v0

> Created: 2026-07-04 · Horizon: `firm-service-map` · Milestone: FM1
> Status: 공개자료 기반 v0. 실제 팀명·직급별 업무 비중은 PM2/FM2 현업 검증 전까지 추정.

## 왜 다시 만들었나

기존 `taxonomy.md`는 회계사 업무를 33개 task로 쪼갰지만, 그 앞단의 "회계법인은 어떤 팀으로
구성되고 각 팀이 무엇을 파는가"가 별도 지도 없이 5대분류로 압축돼 있었다. 그 결과 다음 자동화
대상이 기준서 도메인 또는 로컬 검증성 중심으로 빨리 좁혀졌고, 사용자가 지적한 감사팀·세법팀·
컨설팅팀 같은 실제 조직 맥락이 약했다.

이 문서는 task taxonomy 앞단의 회사/서비스라인 지도다. 목적은 "어느 팀의 어떤 산출물에 AI를
넣을 것인가"를 먼저 고르고, 그 뒤에 task와 엔진 구현을 연결하는 것이다.

## 공개자료 기반 서비스라인 축

| 코드 | 서비스라인 | 대표 고객/상황 | 주요 산출물 | 이 레포와의 1차 접점 |
|---|---|---|---|---|
| F-AUD | Audit / Assurance | 상장·비상장 외부감사, 내부회계 감사 | 감사계획, 테스트조서, 이슈메모, 감사보고서, KAM | A8 리서치, B3 판단메모, B5 주석 초안 |
| F-ACC | Accounting Advisory / CMAAS류 | 복잡 거래, IFRS 전환, 회계정책·결산 자문 | 회계처리 검토메모, 기준서 적용 판단, 전환/결산 지원 문서 | B3 결정준비 초안의 최우선 적용처 |
| F-TAX | Tax | 법인세·부가세·원천세·이전가격·세무조사 | 세무조정, 신고서, 예규 검토메모, 조사 대응 자료 | `tax-agent` 경계. kifrs-rag은 회계/세무 경계 표시만 |
| F-DEAL | Deal / FAS / Valuation | M&A, 실사, 가치평가, 구조조정, IPO | FDD 보고서, valuation memo, IM, SPA 회계/세무 쟁점 | D1~D3 후보. 일부는 세법/시장데이터 의존 |
| F-RISK | Risk / Internal Control / K-SOX | 내부회계 구축·운영평가, 통제 개선 | 프로세스 문서, 통제 설계/평가표, 개선 권고 | E1/A12. 내부 프로세스 데이터 의존 커서 보류 |
| F-CONS | Consulting / Digital / AI | 프로세스 개선, AX, 데이터/AI, 운영모델 | 진단보고서, 로드맵, PoC, 구현 산출물 | 이 레포 자체를 소개할 대상이나, 회계 판단 엔진의 직접 업무는 아님 |
| F-ESG | Sustainability / ESG Assurance | 지속가능성 공시·인증 | ESG 인증보고, 비재무 데이터 검증 문서 | E3. 기준/데이터 유동성 때문에 후순위 |
| F-FORE | Forensic / Compliance | 부정조사, 분쟁, 컴플라이언스 | 조사보고서, 증거 분석, 내부통제 개선안 | 입력 비공개·법률 리스크로 보류 |

## Big4/로컬 법인 차이

| 축 | Big4·대형 법인 | 로컬·중견 법인 | 자동화 시사점 |
|---|---|---|---|
| 주력 | Audit, Tax, Deal, Consulting, Risk/ESG가 분화 | 외부감사, 기장/결산, 세무, CFO 자문이 섞임 | 동일 task라도 팀 맥락과 입력 품질이 다르다 |
| 데이터 | 조서·방법론·내부 플랫폼 접근 가능 | 엑셀·증빙·고객자료 중심 | 공개 repo는 내부 데이터 의존 task를 후순위로 둬야 한다 |
| AI 현황 | Document AI, 감사 플랫폼, Tax Agent, K-SOX Hub 등 일부 도입 | 상용 회계/세무 SW + 개인 AI 활용 편차 | 이 레포의 차별점은 리서치가 아니라 판단/메모 초안 |
| PoC 접근 | 공식 도입 장벽 높지만 임팩트 큼 | 빠른 실사용 피드백 가능 | 현업 검증은 로컬/주변 회계사, 소개 스토리는 Big4 service-line 기준 |

## 서비스라인별 AI insertion point

| 서비스라인 | AI가 바로 들어갈 수 있는 지점 | 사람 검토가 남는 지점 | 현재 자산 |
|---|---|---|---|
| F-AUD | 회계이슈 리서치, 기준서 근거 수집, 주석 요구사항 체크, 분석적 절차 계산 | 감사계획 판단, 조서 결론, KAM 문구, 서명 책임 | `/accounting`, B5 1116 주석, A5 후보 |
| F-ACC | 거래 정보 구조화, 기준서 판단트리, 분개 초안, 검토메모 초안 | 계약 해석, 경영진 의도, 중요성·표시 판단 | 1109/1116 결정 엔진 |
| F-TAX | 세무 리서치, 신고 체크, 산식 계산 | 세무조사 대응, 불복 전략, 법률 판단 | `tax-agent`로 이관 |
| F-DEAL | 재무자료 정합성 체크, valuation 산식 검산, 회계 쟁점 memo | 가정 설정, 협상, 시너지·시장 판단 | D2/D3 후보 |
| F-RISK | 통제 문서 요약, control checklist, evidence 대사 | 통제 설계 적정성, 조직 책임자 인터뷰 | A12/E1 후보이나 내부자료 필요 |
| F-CONS | discovery note, 프로세스 진단 초안, PoC 설계 | 변화관리, 이해관계자 조율 | 제품 소개/도입 채널 |
| F-ESG | 공시 요구사항 체크, 비재무 데이터 consistency check | 측정 방법론, 인증 결론 | 후순위 |
| F-FORE | 문서 분류·타임라인 정리 | 조사 결론, 법적 판단 | 보류 |

## 기존 task taxonomy 재해석

기존 5대분류는 폐기하지 않는다. 다만 다음 순서로 읽는다.

1. `company-map.md`: 회계법인 service-line과 팀 맥락을 고른다.
2. `taxonomy.md`: 해당 팀의 task를 33개 업무 중 어디에 둘지 찾는다.
3. `candidates.md`: AI 구현 후보를 고른다.
4. 구현 horizon: 선택된 업무를 엔진/문서/검증 산출물로 만든다.

이 기준으로 보면 지금까지의 구현은 다음 위치다.

| 구현 자산 | service-line 위치 | task 위치 | 해석 |
|---|---|---|---|
| `/accounting` + K-IFRS RAG | F-AUD / F-ACC | A8 | 이미 법인 AI가 닿은 리서치 영역. 강점이지만 차별점은 약함 |
| 1109 결정 엔진 | F-ACC 중심, F-AUD 이슈검토 보조 | B3/B2 | 회계처리 판단·분개 초안. 제품 차별점의 핵심 |
| 1116 결정 엔진 | F-ACC 중심, F-AUD 이슈검토 보조 | B3/B2 | 2번째 도메인 이식으로 판단 엔진 패턴 검증 |
| 1116 주석 초안 | F-AUD / F-ACC | B5 | 재무제표 주석 요구사항 대사. 실제 공시와 대사 가능한 좋은 PoC 표면 |

## 소스

- 삼정KPMG Deal Advisory: https://kpmg.com/kr/ko/services/deal-advisory.html
- 삼정KPMG US IPO 지원센터: https://kpmg.com/kr/ko/services/special-service-support-center/us-ipo-support.html
- 삼일PwC Korea Business Network: Japan: https://www.pwc.com/kr/ko/services/korea-business-network/japan.html
- 삼일PwC M&A guide book: https://www.pwc.com/kr/ko/services/samilpwc_mna_guide-book.pdf
- EY Korea services: https://www.ey.com/ko_kr/services
- EY Korea Business Network: https://www.ey.com/ko_kr/services/korea-business-network
- EY AI Center: https://www.ey.com/ko_kr/services/ai/ey-ai-hub
- Deloitte Korean Services Group: https://www.deloitte.com/kr/ko/services/firmwide-integrated-services/services/ibs-korean-services-group-en.html
- Deloitte IFRS e-learning: https://www.deloitte.com/kr/ko/services/audit-assurance/services/ifrs-elearning.html
- 기존 PM1 출처: `docs/practice-map/sources.md`

## 한계와 다음 작업

- 이 문서는 회사 홈페이지·공개자료 기반이라 실제 팀별 시간 배분과 junior/senior 업무 분담은 약하다.
- 다음 FM2는 이 service-line map을 기준으로 팀별 workflow를 다시 써야 한다. 특히 Audit와 Accounting
  Advisory를 분리해서, 같은 B3 회계처리 판단이라도 "감사 이슈검토"인지 "회계자문 산출물"인지
  다르게 봐야 한다.
- PM2 현업 검증은 여전히 필요하다. 다만 질문지도 이제 task 목록이 아니라 service-line별 workflow를
  기준으로 만들어야 한다.
