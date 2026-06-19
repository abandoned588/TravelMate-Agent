from __future__ import annotations

import json
from typing import Any

from config.settings import POI_CACHE_PATH, WEATHER_CACHE_PATH, ensure_project_directories


CACHE_PATHS = {
    "weather_cache": WEATHER_CACHE_PATH,
    "poi_cache": POI_CACHE_PATH,
}


def _load_cache_file(cache_name: str) -> dict[str, Any]:
    ensure_project_directories()
    path = CACHE_PATHS.get(cache_name)
    if path is None:
        return {}

    try:
        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            return {}
        payload = json.loads(raw)
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def read_cache(cache_name: str, key: str) -> dict[str, Any] | None:
    cache = _load_cache_file(cache_name)
    value = cache.get(key)
    return value if isinstance(value, dict) else None


def write_cache(cache_name: str, key: str, value: dict[str, Any]) -> None:
    path = CACHE_PATHS.get(cache_name)
    if path is None:
        return

    cache = _load_cache_file(cache_name)
    cache[key] = value
    try:
        path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        return
