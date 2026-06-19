from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

import api.app as api_module
import tools.itinerary as itinerary_module


def test_health_endpoint_returns_status() -> None:
    client = TestClient(api_module.app)

    response = client.get("/api/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert "llm_configured" in payload["data"]


def test_web_root_serves_frontend_shell() -> None:
    client = TestClient(api_module.app)

    response = client.get("/")

    assert response.status_code == 200
    assert "TravelMate Web" in response.text


def test_save_itinerary_endpoint_writes_file(monkeypatch) -> None:
    output_path = Path("storage/outputs/test_api_itinerary.md").resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(itinerary_module, "ITINERARY_PATH", output_path)
    monkeypatch.setattr(api_module, "ITINERARY_PATH", output_path)

    client = TestClient(api_module.app)
    response = client.post(
        "/api/save-itinerary",
        json={"title": "API Trip", "content": "## Day 1\n- Demo"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert output_path.exists()
