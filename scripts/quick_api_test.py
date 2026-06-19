from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.app import app


def main() -> None:
    from fastapi.testclient import TestClient

    client = TestClient(app)

    print("[GET] /api/health")
    health = client.get("/api/health")
    print(health.status_code)
    print(json.dumps(health.json(), ensure_ascii=False, indent=2))

    print("\n[POST] /api/save-itinerary")
    save_result = client.post(
        "/api/save-itinerary",
        json={"title": "API Smoke Test", "content": "## Day 1\n- Demo itinerary from API"},
    )
    print(save_result.status_code)
    print(json.dumps(save_result.json(), ensure_ascii=False, indent=2))

    print("\n[GET] /api/itinerary")
    itinerary = client.get("/api/itinerary")
    print(itinerary.status_code)
    print(json.dumps(itinerary.json(), ensure_ascii=False, indent=2))

    print("\n[GET] /api/tool-traces")
    traces = client.get("/api/tool-traces?limit=5")
    print(traces.status_code)
    print(json.dumps(traces.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
