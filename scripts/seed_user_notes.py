from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs import store
from kifrs.user_notes import parse_user_note

DB_PATH = ROOT / "data" / "kifrs.db"
CREATED_AT = "2026-06-30"

SEEDS = [
    (
        "1109",
        "4.2.1",
        "type=term_bridge; trigger=공매도; expansion=당기손익-공정가치 측정 금융부채; 단기매매항목; 차입한 주식 인도 의무; 매도부채; source=q05; rationale=1109 본문에 공매도 직접 표현이 없어 검색 실패",
    ),
    (
        "1102",
        "35",
        "type=term_bridge; trigger=선택형 주식기준보상; expansion=현금결제 선택권; 복합금융상품; 종업원 선택; 기업 선택; 부채요소와 자본요소; source=q05; rationale=시험 표현 그대로는 1102-35~43 회수가 약함",
    ),
    (
        "1115",
        "B40",
        "type=term_bridge; trigger=갱신선택권; expansion=고객 선택권; 중요한 권리; 추가 재화나 용역; 계약갱신 선택권; source=q07; rationale=B39~B43 회수 안정화",
    ),
    (
        "1115",
        "B42",
        "type=term_bridge; trigger=외상거래할인권; expansion=고객 선택권; 할인; 선택권 행사 가능성; 개별 판매가격; 증분 할인; source=q07; rationale=할인권을 고객 선택권 분기로 유도",
    ),
    (
        "1115",
        "118",
        "type=exam_convention; trigger=갱신선택권 부채 금액; expansion=계약부채와 잔여 수행의무 표시액을 구분한다; source=q07; rationale=시험 답안이 잔여 수행의무를 부채로 요구해 q07-1 실패",
    ),
    (
        "1115",
        "B43",
        "type=exam_convention; trigger=진행률 반올림; expansion=원가진행률 중간 반올림과 최종 금액 반올림을 모두 검산한다; source=q07; rationale=q07-1 수익 금액 소폭 차이",
    ),
    (
        "1019",
        "123",
        "type=exam_convention; trigger=중간 정산 순이자; expansion=원금 단순 분배 산식과 누적 이자 산식을 모두 검산한다; source=q06; rationale=시험 표준과 정밀 산식 차이 150 발생",
    ),
    (
        "1019",
        "103",
        "type=interpretation_note; trigger=해고급여 vs 구조조정 충당부채; expansion=1019 해고급여와 1037 구조조정 직접지출의 분리/합산 일관성 확인; source=q06; rationale=충당부채 포함 후 발생 시 PL 재인식 여부 분기",
    ),
    (
        "1019",
        "101A",
        "type=exam_convention; trigger=자산인식상한 적용 시점; expansion=보고기간 말 순확정급여자산 발생 후 마지막 적용 우선; source=q06; rationale=정산·제도개정 중간 적용 오해 방지",
    ),
    (
        "1116",
        "80",
        "type=retriever_policy; trigger=금융리스 변경; expansion=금융→운용은 80(1), 금융→금융은 80+1109 변경손익, 운용→금융은 대칭 처리 해석 여부 명시; source=P4C2; rationale=리스제공자 변경 시나리오 4/5/6 분기 정리",
    ),
    (
        "1113",
        "76",
        "type=term_bridge; trigger=종가; expansion=상장주식; 거래소 시세; 활성시장; 동일한 자산; 조정하지 않은 공시가격; 수준 1 투입변수; source=P4C4; rationale=사용자 입력에는 수준 1이 아니라 종가/시세만 나오는 경우가 많음",
    ),
    (
        "1113",
        "81",
        "type=term_bridge; trigger=수익률 곡선; expansion=회사채; 신용스프레드; 관측 가능한 할인율; 이익접근법; 현재가치; 수준 2 투입변수; source=P4C4; rationale=채권 공정가치 문제는 할인율/스프레드가 핵심 검색 단서",
    ),
    (
        "1113",
        "86",
        "type=term_bridge; trigger=DCF; expansion=사업계획; 장기성장률; 내부 현금흐름; 비상장 지분; 관측할 수 없는 투입변수; 수준 3 투입변수; source=P4C4; rationale=모델명이나 내부 가정 입력을 1113 서열체계 문단으로 연결",
    ),
    # Engine Hardening CS-5: kifrs/store.py의 하드코딩 TERM_BRIDGE dict를 user_note_v2로 이관.
    # "공매도"는 위 1109-4.2.1 seed가 이미 상위 집합을 커버하므로 재등록하지 않음.
    (
        "1115",
        "60",
        "type=term_bridge; trigger=할부판매; expansion=유의적 금융요소; 화폐의 시간가치; 현금판매가격; source=engine-hardening-cs5; rationale=구 TERM_BRIDGE dict 이관 — 시험 표현 '할부판매'가 1115 본문 어휘로 직접 존재하지 않음",
    ),
    (
        "1115",
        "61",
        "type=term_bridge; trigger=현재가치 할인; expansion=유의적 금융요소; 화폐의 시간가치; source=engine-hardening-cs5; rationale=구 TERM_BRIDGE dict 이관",
    ),
    (
        "1102",
        "16",
        "type=term_bridge; trigger=측정기준일; expansion=부여일; source=engine-hardening-cs5; rationale=구 TERM_BRIDGE dict 이관",
    ),
    (
        "1019",
        "8",
        "type=term_bridge; trigger=재측정요소; expansion=보험수리적손익; source=engine-hardening-cs5; rationale=구 TERM_BRIDGE dict 이관",
    ),
    # RO2 term bridge candidate evaluation (2026-07-05): docs/reports/2026-07-05-ro2-term-bridge-candidate-eval.md
    (
        "1037",
        "14",
        "type=term_bridge; trigger=충당부채; expansion=현재의무 과거사건 자원 유출 가능성 신뢰성 있는 추정; source=ro2-term-bridge; rationale=Q039 misses 1037-14 because the original lease-focused question lacks provision recognition criteria terms",
    ),
    (
        "1036",
        "18",
        "type=term_bridge; trigger=손상차손; expansion=회수가능액 순공정가치 사용가치; source=ro2-term-bridge; rationale=Q048 misses 1036-18 while already finding 1036-59; this bridge recovers 1036-18 and preserves 1036-59",
    ),
    # Remaining hard miss candidate evaluation (2026-07-05): docs/reports/2026-07-05-hard-miss-candidate-eval.md
    (
        "1116",
        "45",
        "type=term_bridge; trigger=리스 범위를 좁히는; expansion=리스변경 별도 리스 아님 리스 범위 감소 사용권자산 장부금액 감소 손익 인식; source=hard-miss-q029; rationale=Q029 misses 1116-45 while already finding 1116-46; this bridge recovers the scope-decrease lease modification paragraph",
    ),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Phase 4 user_note rows into v2 with legacy mirror.")
    parser.add_argument("--apply", action="store_true", help="insert rows; default is dry-run")
    args = parser.parse_args()

    store.init_db()
    parsed_seeds = [
        parse_user_note(standard, no, note, CREATED_AT)
        for standard, no, note in SEEDS
    ]
    with store._conn() as conn:
        existing = {
            (
                row["standard"], row["no"], row["type"], row["trigger"],
                row["expansion"], row["source"], row["rationale"],
            )
            for row in conn.execute(
                """
                SELECT standard, no, type, trigger, expansion, source, rationale
                FROM user_note_v2
                """
            )
        }
    to_insert = [
        note for note in parsed_seeds
        if (
            note.standard, note.no, note.type, note.trigger,
            note.expansion, note.source, note.rationale,
        ) not in existing
    ]

    print(f"DB: {DB_PATH}")
    print(f"seed rows: {len(SEEDS)}")
    print(f"existing rows: {len(SEEDS) - len(to_insert)}")
    print(f"new rows: {len(to_insert)}")

    for note in to_insert:
        print(f"  + {note.standard}-{note.no}: {note.trigger}")

    if args.apply and to_insert:
        inserted = 0
        for note in to_insert:
            result = store.add_user_note_v2(
                note.standard, note.no, note.type or "", note.trigger or "",
                note.expansion or "", note.source, note.rationale, CREATED_AT,
                mirror_legacy=True,
            )
            inserted += 1 if result["inserted"] else 0
        print(f"inserted: {inserted}")
    elif args.apply:
        print("nothing to insert")
    else:
        print("dry-run only; pass --apply to insert")


if __name__ == "__main__":
    main()
