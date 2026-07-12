#!/usr/bin/env python3
"""Export data/kifrs.db metadata (standard/section titles + cross-reference counts only —
never paragraph body/context) into web/public/universe/graph.json for the 3D universe viewer.

Node/edge schema follows obsidian/poc-graph's dist/graph.json (galaxy -> cluster -> star,
2-tier hierarchy — no system level).
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "kifrs.db"
STANDARDS_JSON = ROOT / "web" / "src" / "data" / "standards.json"
OUT_PATH = ROOT / "web" / "public" / "universe" / "graph.json"

MAX_SECTIONS_PER_STANDARD = 6
MIN_SECTION_PARAGRAPHS = 5

GALAXY_LABELS = {
    "kifrs": "K-IFRS 기준서",
    "interp": "해석서",
    "gaap": "일반기업회계기준",
    "framework": "개념체계·실무서·준칙",
}

CLUSTER_LABELS = {
    ("kifrs", "presentation"): "표시·공시",
    ("kifrs", "financial"): "금융상품",
    ("kifrs", "assets"): "자산",
    ("kifrs", "liabilities"): "부채·급여·보상",
    ("kifrs", "revenue"): "수익·비용·보조금",
    ("kifrs", "groups"): "연결·지분·결합",
    ("kifrs", "industry"): "산업·특수",
    ("interp", "interpretations"): "해석서",
    ("gaap", "gaap-core"): "총칙·재무제표",
    ("gaap", "gaap-assets"): "자산",
    ("gaap", "gaap-capital"): "자본·부채·법인세",
    ("gaap", "gaap-etc"): "기타",
    ("framework", "framework"): "개념체계 등",
}

# std id -> (galaxy, cluster). Built from the explicit id lists in the task spec.
_KIFRS_CLUSTERS = {
    "presentation": ["1001", "1007", "1008", "1010", "1024", "1027", "1033", "1034", "1108", "1112", "1113"],
    "financial": ["1032", "1039", "1107", "1109"],
    "assets": ["1002", "1016", "1023", "1036", "1038", "1040", "1105", "1106"],
    "liabilities": ["1012", "1019", "1026", "1037", "1102"],
    "revenue": ["1015", "1020", "1021", "1029", "1115"],
    "groups": ["1028", "1103", "1110", "1111"],
    "industry": ["1041", "1101", "1114", "1116", "1117"],
}
_GAAP_CLUSTERS = {
    "gaap-core": [f"gaap_{i:02d}" for i in range(1, 10)],
    "gaap-assets": [f"gaap_{i:02d}" for i in range(10, 15)],
    "gaap-capital": [f"gaap_{i:02d}" for i in range(15, 23)],
    "gaap-etc": [f"gaap_{i:02d}" for i in range(23, 34)] + [
        "gaap_보험업회계처리준칙",
        "gaap_일반기업회계기준_시행일_및_경과규정",
        "gaap_재무회계개념체계",
    ],
}


def build_std_to_cluster() -> dict[str, tuple[str, str]]:
    mapping: dict[str, tuple[str, str]] = {}
    for cluster_id, ids in _KIFRS_CLUSTERS.items():
        for sid in ids:
            mapping[sid] = ("kifrs", cluster_id)
    for cluster_id, ids in _GAAP_CLUSTERS.items():
        for sid in ids:
            mapping[sid] = ("gaap", cluster_id)
    mapping["special_5002"] = ("framework", "framework")
    return mapping


def slugify(text: str, maxlen: int = 40) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^0-9a-z가-힣]+", "-", s)
    s = s.strip("-") or "section"
    return s[:maxlen].strip("-") or "section"


def resolve_hierarchy(std_id: str, std_to_cluster: dict[str, tuple[str, str]]) -> tuple[str, str]:
    if std_id in std_to_cluster:
        return std_to_cluster[std_id]
    if re.fullmatch(r"1\d{3}", std_id):
        print(f"WARN: kifrs id {std_id} has no cluster mapping, falling back to industry", file=sys.stderr)
        return ("kifrs", "industry")
    if re.fullmatch(r"2\d{3}", std_id):
        return ("interp", "interpretations")
    if std_id.startswith("gaap_"):
        print(f"WARN: gaap id {std_id} has no cluster mapping, falling back to gaap-etc", file=sys.stderr)
        return ("gaap", "gaap-etc")
    return ("framework", "framework")


def main() -> None:
    standards_meta = json.loads(STANDARDS_JSON.read_text(encoding="utf-8"))
    title_by_id = {s["id"]: s["title"] for s in standards_meta}

    con = sqlite3.connect(str(DB_PATH))
    cur = con.cursor()

    cur.execute("SELECT id, source, total_paragraphs FROM standard ORDER BY id")
    standards = cur.fetchall()

    std_to_cluster = build_std_to_cluster()

    nodes: list[dict] = []
    edges: list[dict] = []
    galaxy_ids: set[str] = set()
    cluster_keys: set[tuple[str, str]] = set()
    galaxy_counts: Counter[str] = Counter()

    for std_id, source, total_paragraphs in standards:
        galaxy, cluster = resolve_hierarchy(std_id, std_to_cluster)
        galaxy_ids.add(galaxy)
        cluster_keys.add((galaxy, cluster))
        galaxy_counts[galaxy] += 1

        title = title_by_id.get(std_id)
        if title is None:
            # Fallback: derive from source filename (rare — standards.json should cover all).
            stem = re.sub(r"\.pdf$", "", source)
            m = re.search(r"제\d+호[_\s]*([^(]+)", stem) or re.search(r"제\d+장[_\s]*([^(]+)", stem)
            title = (m.group(0) if m else stem).replace("_", " ").strip()
            print(f"WARN: no standards.json title for {std_id}, derived '{title}'", file=sys.stderr)

        galaxy_label = GALAXY_LABELS[galaxy]
        cluster_label = CLUSTER_LABELS[(galaxy, cluster)]

        node = {
            "id": f"std/{std_id}",
            "label": title,
            "type": "standard",
            "domain": galaxy,
            "date": "",
            "tags": [cluster],
            "paragraphs": total_paragraphs or 0,
            "hierarchy": {
                "galaxy": galaxy,
                "galaxy_label": galaxy_label,
                "cluster": cluster,
                "cluster_label": cluster_label,
                "role": "star",
            },
        }
        nodes.append(node)

        # top sections by paragraph count
        cur.execute(
            "SELECT section, COUNT(*) AS cnt FROM paragraph "
            "WHERE standard = ? AND section IS NOT NULL AND TRIM(section) != '' "
            "GROUP BY section ORDER BY cnt DESC",
            (std_id,),
        )
        sections = [(sec, cnt) for sec, cnt in cur.fetchall() if cnt >= MIN_SECTION_PARAGRAPHS]
        sections = sections[:MAX_SECTIONS_PER_STANDARD]

        seen_slugs: set[str] = set()
        for sec_title, cnt in sections:
            slug = slugify(sec_title)
            base_slug = slug
            i = 2
            while slug in seen_slugs:
                slug = f"{base_slug}-{i}"
                i += 1
            seen_slugs.add(slug)

            sec_id = f"sec/{std_id}/{slug}"
            nodes.append({
                "id": sec_id,
                "label": sec_title,
                "type": "section",
                "domain": galaxy,
                "date": "",
                "tags": [cluster],
                "paragraphs": cnt,
            })
            edges.append({"source": sec_id, "target": node["id"], "type": "link", "rel": "contains"})

    # cross-reference edges (standard-to-standard, aggregated, no context text read)
    cur.execute("SELECT from_standard, to_standard FROM cross_reference")
    pair_counts: Counter[tuple[str, str]] = Counter()
    for from_std, to_std in cur.fetchall():
        if from_std == to_std:
            continue
        pair_counts[(from_std, to_std)] += 1

    for (from_std, to_std), weight in pair_counts.items():
        edges.append({
            "source": f"std/{from_std}",
            "target": f"std/{to_std}",
            "type": "link",
            "rel": "related",
            "weight": weight,
        })

    con.close()

    # hierarchy virtual nodes: galaxy -> cluster -> star (2-tier, no system level)
    for galaxy in sorted(galaxy_ids):
        gid = f"hier/galaxy/{galaxy}"
        nodes.append({
            "id": gid,
            "label": GALAXY_LABELS[galaxy],
            "type": "topic",
            "domain": "hierarchy",
            "date": "",
            "tags": ["galaxy"],
            "hierarchy_virtual": True,
            "hierarchy": {
                "role": "galaxy",
                "level": 0,
                "parent": "",
                "galaxy": galaxy,
                "galaxy_label": GALAXY_LABELS[galaxy],
                "angle": 0,
                "radius": 0,
                "center": False,
            },
        })

    for galaxy, cluster in sorted(cluster_keys):
        gid = f"hier/galaxy/{galaxy}"
        cid = f"hier/cluster/{galaxy}/{cluster}"
        nodes.append({
            "id": cid,
            "label": CLUSTER_LABELS[(galaxy, cluster)],
            "type": "topic",
            "domain": "hierarchy",
            "date": "",
            "tags": ["cluster"],
            "hierarchy_virtual": True,
            "hierarchy": {
                "role": "cluster",
                "level": 1,
                "parent": gid,
                "galaxy": galaxy,
                "galaxy_label": GALAXY_LABELS[galaxy],
                "cluster": cluster,
                "cluster_label": CLUSTER_LABELS[(galaxy, cluster)],
            },
        })
        edges.append({"source": gid, "target": cid, "type": "hierarchy", "rel": "contains"})

    for n in nodes:
        h = n.get("hierarchy")
        if h and h.get("role") == "star":
            cid = f"hier/cluster/{h['galaxy']}/{h['cluster']}"
            edges.append({"source": cid, "target": n["id"], "type": "hierarchy", "rel": "contains"})

    graph = {"nodes": nodes, "edges": edges}

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")

    star_count = sum(1 for n in nodes if n.get("type") == "standard")
    sec_count = sum(1 for n in nodes if n.get("type") == "section")
    hier_count = sum(1 for n in nodes if n.get("hierarchy_virtual"))
    print(f"nodes={len(nodes)} (standard={star_count}, section={sec_count}, hierarchy_virtual={hier_count})")
    print(f"edges={len(edges)}")
    print("by galaxy:", dict(galaxy_counts))


if __name__ == "__main__":
    main()
