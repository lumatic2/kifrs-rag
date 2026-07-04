from __future__ import annotations

from scripts.client_private_routing_bridge_check import check_client_private_routing_bridge


def test_client_private_routing_bridge_check_passes() -> None:
    result = check_client_private_routing_bridge()

    assert result["ok"], result["errors"]
    assert result["route_1116"]["status"] == "candidate"
    assert result["route_1116"]["route"] == "kifrs1116_review_pack"
    assert result["route_1109"]["status"] == "needs_more_facts"
    assert result["route_blocked"]["status"] == "blocked"
