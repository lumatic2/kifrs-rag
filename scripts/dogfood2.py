"""Phase 1 Dogfood 2차: 5개 기준서 전체 대상 새 질문 5개."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
from kifrs import store

def show(label, items, bodylen=160):
    print(f"\n━━━ {label} ━━━")
    if not items:
        print("  (결과 없음)"); return
    for it in items:
        if not it: continue
        std = it.get("standard", "?"); no = it.get("no"); sec = it.get("section") or ""
        page = it.get("page")
        snip = it.get("snippet") or it.get("body") or it.get("preview") or ""
        snip = snip.replace("\n", " ")[:bodylen]
        print(f"  [{std}-{no}] p.{page} ({sec})")
        print(f"    → {snip}")

# ────────────────────────────────────────────────────────
print("\n\n████ Q1: 1116 리스의 정의와 식별 기준은? ████")
show("search '리스의 정의'", store.search_fts("리스의 정의", "1116", limit=3))
show("list_paragraphs section='리스의 식별'", store.list_paragraphs("1116", section="리스의 식별", limit=5))
p = store.get_paragraph("1116","9"); show("1116-9 (핵심 문단 후보)", [p])

# ────────────────────────────────────────────────────────
print("\n\n████ Q2: 1109 금융자산 분류 범주 3가지는? ████")
show("search '상각후원가'", store.search_fts("상각후원가", "1109", limit=3))
show("search '당기손익-공정가치'", store.search_fts("당기손익-공정가치", "1109", limit=3))
show("search '기타포괄손익-공정가치'", store.search_fts("기타포괄손익-공정가치", "1109", limit=2))

# ────────────────────────────────────────────────────────
print("\n\n████ Q3: 1001 재무제표 전체 구성은? ████")
show("search '재무제표'", store.search_fts("재무제표 전체 한 벌", "1001", limit=3))
show("search '재무상태표'", store.search_fts("재무상태표", "1001", limit=3))
sections = store.list_sections("1001")[:12]
print("\n  ▸ 1001 섹션 상위 12개:")
for s in sections:
    print(f"    - {s['appendix']} / {s['section']} ({s['paragraph_count']}개)")

# ────────────────────────────────────────────────────────
print("\n\n████ Q4: 1019 확정급여제도 회계처리는? ████")
show("search '확정급여'", store.search_fts("확정급여제도", "1019", limit=3))
show("section='확정급여제도'", store.list_paragraphs("1019", section="확정급여제도", limit=5))
show("search '순확정급여부채'", store.search_fts("순확정급여부채", "1019", limit=3))

# ────────────────────────────────────────────────────────
print("\n\n████ Q5: '공정가치' 용어가 5개 기준서에 어떻게 쓰이나 (cross-standard) ████")
hits = store.search_fts("공정가치로 측정", None, limit=10)
print(f"\n  총 {len(hits)}건 (전체 기준서):")
from collections import Counter
by_std = Counter(h["standard"] for h in hits)
print(f"  기준서별 분포: {dict(by_std)}")
for h in hits[:5]:
    print(f"    [{h['standard']}-{h['no']}] p.{h['page']} ({h['section']})")
    print(f"      → {h['snippet'][:120]}")

# ────────────────────────────────────────────────────────
print("\n\n████ 보너스: list_standards ████")
for s in store.list_standards():
    print(f"  {s['standard']}: {s['total_paragraphs']} paragraphs")
