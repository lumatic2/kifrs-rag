import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "quality_preflight", ROOT / "scripts" / "quality_preflight.py"
)
quality_preflight = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(quality_preflight)

DEFAULT_COMMANDS = quality_preflight.DEFAULT_COMMANDS
run_preflight = quality_preflight.run_preflight


def test_quality_preflight_declares_public_safe_commands():
    command_names = {entry["name"] for entry in DEFAULT_COMMANDS}
    assert {
        "focused_pytest",
        "local_rag_threshold_gate",
        "authority_registry",
        "authority_source_pack",
        "user_note_v2_audit",
    } <= command_names
    joined = " ".join(" ".join(entry["cmd"]) for entry in DEFAULT_COMMANDS)
    assert "data/kifrs.db" not in joined
    assert ".env" not in joined


def test_quality_preflight_smoke():
    result = run_preflight(timeout=240)
    assert result["ok"], result["results"]
    assert result["public_safe"] is True
    assert result["protected_assets_required"] is False
