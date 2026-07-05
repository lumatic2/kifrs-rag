from __future__ import annotations

from scripts.failure_boundary_matrix import build_matrix, render_markdown


def test_failure_boundary_matrix_covers_core_failure_modes() -> None:
    matrix = build_matrix()
    categories = {row["category"] for row in matrix["boundaries"]}

    assert matrix["ok"] is True
    assert {
        "retrieval_quality",
        "citation_assembly",
        "client_private_fact_gap",
        "unsupported_workflow",
        "authority_boundary",
        "default_promotion",
    }.issubset(categories)


def test_failure_boundary_matrix_has_runnable_verification_commands() -> None:
    matrix = build_matrix()

    assert all(row["verification_command"].startswith(("python ", "python -m ")) for row in matrix["boundaries"])
    assert any("rag_quality_final_gate.py" in row["verification_command"] for row in matrix["boundaries"])
    assert any("default_retriever_guard.py" in row["verification_command"] for row in matrix["boundaries"])


def test_failure_boundary_matrix_report_is_public_safe() -> None:
    rendered = render_markdown(build_matrix())

    assert "PTQ3 Failure Boundary Matrix" in rendered
    assert "Do not copy private source body into public reports" in rendered
    assert "api_key" not in rendered
    assert "source_body" not in rendered
