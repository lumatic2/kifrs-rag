"""Phase 1 Dogfood: 5개 질문을 store API 로 검증."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
from kifrs import store

def show(label, items):
    print(f"\n━━━━━ {label} ━━━━━")
    if not items:
        print("  (결과 없음)"); return
    for it in items:
        no = it.get("no"); sec = it.get("section") or ""; page = it.get("page")
        snip = it.get("snippet") or it.get("body") or it.get("preview") or ""
        snip = snip.replace("\n", " ")[:160]
        print(f"  [{no}] (p.{page}) {sec}\n    → {snip}")

# Q1: 수익 인식 5단계
print("\n\n====== Q1: K-IFRS 1115호 수익 인식 5단계는? ======")
show("search '핵심 원칙'", store.search_fts("핵심 원칙", "1115", limit=2))
show("search '수행의무 식별'", store.search_fts("수행의무의 식별", "1115", limit=3))
show("문단 2 (핵심 원칙)", [store.get_paragraph("1115","2")])

# Q2: 계약변경 회계처리
print("\n\n====== Q2: 1115호 계약변경 회계처리 방법은? ======")
show("section='계약변경' 문단 목록", store.list_paragraphs("1115", section="계약변경", limit=10))
for no in ("20","21"):
    p = store.get_paragraph("1115", no)
    if p: show(f"문단 {no}", [p])

# Q3: 거래가격 산정
print("\n\n====== Q3: 거래가격은 뭐고 어떻게 산정? ======")
show("search '거래가격을 산정'", store.search_fts("거래가격을 산정", "1115", limit=3))
show("section='거래가격의 산정' 일부", store.list_paragraphs("1115", section="거래가격의 산정", limit=5))

# Q4: 한국 추가 조항
print("\n\n====== Q4: 1115호에 한국이 추가한 조항이 있나? ======")
import sqlite3
with store._conn() as c:
    rows = c.execute("SELECT no, section, page, substr(body,1,120) AS preview FROM paragraph WHERE standard='1115' AND ko_added=1 ORDER BY ord").fetchall()
show("ko_added=True 조항", [dict(r) for r in rows])

# Q5: 부록 B5
print("\n\n====== Q5: 부록 B5는 뭐에 대한 내용? ======")
p = store.get_paragraph("1115","B5")
show("get B5", [p])
show("B5 앞뒤 맥락 (around=1)", store.get_context("1115","B5",1))
