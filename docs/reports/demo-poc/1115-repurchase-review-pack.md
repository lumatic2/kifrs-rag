# F-ACC Review Pack — scenario_04_repurchase_call_option

- 기준서: KIFRS1115
- 상태: automated
- 판단 경로: repurchase_financing_arrangement
- 판단 요약: scenario_04_repurchase_call_option: repurchase_financing_arrangement 경로로 자동 판단. 수익 초안 0, 분개 초안 2개 산출.

## 1. 검토메모
# 검토 메모 — scenario_04_repurchase_call_option

## 1. 거래 개요
- 시나리오 유형: repurchase_call_option
- 판단 경로: repurchase_financing_arrangement
- 계약금액: 1,000,000

## 2. 5단계 수익인식 판단
- Step 1 contract_identification: contract is identified with payment terms and probable collectability [1115-9]
- Step 2 performance_obligations: sale with repurchase right assessment [1115-B64~B69]
- Step 3 transaction_price: assess repurchase terms before treating the consideration as ordinary sale revenue [1115-47]
- Step 4 allocate_transaction_price: repurchase arrangement classification before revenue recognition [1115-73]
- Step 5 recognize_revenue: do not treat as an ordinary sale; account for the arrangement as financing until repurchase economics are resolved [1115-B64~B69]

## 3. 측정
- 당기 수익 초안: 0
- 금융요소/스프레드 초안: 80,000
- 재매입 관련 부채 초안: 1,000,000
- 측정 메모: Entity call option blocks ordinary sale accounting until the repurchase arrangement is resolved.

## 4. 분개 초안
### scenario_04_repurchase_call_option 재매입약정 초안
- (차) 현금  1,000,000
- (대) 금융부채  1,000,000
### scenario_04_repurchase_call_option 재매입스프레드 초안
- (차) 금융비용  80,000
- (대) 금융부채  80,000

## 5. 결론
- scenario_04_repurchase_call_option: repurchase_financing_arrangement 경로.
- 주요 근거: 1115-B64~B69
- 잔존 의문점: 입력 사실과 추정치 검토 필요(R15 자동 산출 초안).

## 2. 분개 초안
- scenario_04_repurchase_call_option 재매입약정 초안
  - (차) 현금: 1,000,000
  - (대) 금융부채: 1,000,000
- scenario_04_repurchase_call_option 재매입스프레드 초안
  - (차) 금융비용: 80,000
  - (대) 금융부채: 80,000

## 3. 리뷰 체크리스트
- [ready] 5단계 판단: 5개 step 결론 산출
- [ready] 측정표: 수익 0, 이연 0
- [ready] 분개 초안: 분개 2개, 차대 일치 확인
- [ready] 검토메모: 거래개요, 판단, 측정, 분개, 결론 섹션 포함

## 4. 사람 검토 필요 항목
### 입력 사실과 추정치 검토
- 왜 필요한가: 자동 산출물은 구조화 fixture 입력에 근거한 초안이며 실제 계약 원문, 확률, SSP, 지급조건은 사람이 확인해야 한다.
- 필요한 추가자료:
  - 계약 원문
  - 독립판매가격 근거
  - 권리 행사 확률
  - 지급조건
  - 경영진 판단 메모
- 리뷰 질문:
  - repurchase_financing_arrangement 경로가 실제 계약 조건과 일치하는지?
  - 금액 산정에 사용한 SSP/확률/현금판매가격이 외부 증거와 일치하는지?

## 외부 근거
### 해석 보조 근거
- KASB metadata catalog seed (`kasb-interpretation-material` / `kasb-interpretation-material-catalog-seed`): {"type": "url", "url": "https://www.kasb.or.kr/"}
### 법적 경계 근거
- Commercial Act capital transaction locator (`commercial-act-capital` / `commercial-act-capital-locator-seed`): {"article_locator": "capital-transactions", "type": "official_registry", "url": "https://www.law.go.kr/"}
### 수치 사실 근거
- Synthetic DART revenue fact (`opendart-structured-financials` / `synthetic-dart-2025-annual-001-revenue`): {"filing_id": "synthetic-dart-2025-annual-001", "line_item": "revenue", "type": "synthetic_filing"}

## 5. 인용
- 1115-47
- 1115-73
- 1115-9
- 1115-B64~B69
