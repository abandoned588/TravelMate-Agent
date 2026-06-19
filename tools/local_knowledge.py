from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "city_knowledge_base.csv"
CITY_ALIASES = {
    "beijing": "Beijing",
    "bj": "Beijing",
    "??": "Beijing",
    "shanghai": "Shanghai",
    "sh": "Shanghai",
    "??": "Shanghai",
    "hangzhou": "Hangzhou",
    "hz": "Hangzhou",
    "??": "Hangzhou",
    "zhengzhou": "Zhengzhou",
    "zz": "Zhengzhou",
    "??": "Zhengzhou",
    "chengdu": "Chengdu",
    "cd": "Chengdu",
    "??": "Chengdu",
    "xian": "Xian",
    "xi'an": "Xian",
    "xa": "Xian",
    "??": "Xian",
    "guangzhou": "Guangzhou",
    "gz": "Guangzhou",
    "??": "Guangzhou",
    "shenzhen": "Shenzhen",
    "sz": "Shenzhen",
    "??": "Shenzhen",
    "nanjing": "Nanjing",
    "nj": "Nanjing",
    "??": "Nanjing",
    "suzhou": "Suzhou",
    "szhou": "Suzhou",
    "??": "Suzhou",
}


def _normalize(text: str) -> str:
    return text.strip().lower()


def _canonical_city(text: str) -> str:
    key = _normalize(text)
    return CITY_ALIASES.get(key, text.strip())


def _load_rows() -> list[dict[str, str]]:
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]


def _row_matches_city(row: dict[str, str], city: str) -> bool:
    target = _canonical_city(city)
    row_city = row.get("city", "").strip()
    if row_city == target:
        return True
    aliases = {alias.strip().lower() for alias in row.get("city_aliases", "").split("|") if alias.strip()}
    return _normalize(city) in aliases


def _matches_query(row: dict[str, str], query: str) -> bool:
    if not query:
        return True
    haystack = " ".join(
        [
            row.get("city", ""),
            row.get("name", ""),
            row.get("type", ""),
            row.get("district", ""),
            row.get("highlights", ""),
            row.get("best_for", ""),
            row.get("notes", ""),
        ]
    ).lower()
    keywords = [part.strip().lower() for part in query.split() if part.strip()]
    return all(keyword in haystack for keyword in keywords) if keywords else True


def search_local_knowledge(city: str, categories: list[str], query: str = "", limit: int = 8) -> dict[str, Any]:
    rows = _load_rows()
    if not rows:
        return {
            "success": False,
            "error": f"Local knowledge base not found: {DATA_PATH}",
        }

    category_keys = {_normalize(category) for category in categories if category.strip()}

    matches: list[dict[str, str]] = []
    for row in rows:
        row_category = _normalize(row.get("category", ""))
        if not _row_matches_city(row, city):
            continue
        if category_keys and row_category not in category_keys:
            continue
        if not _matches_query(row, query):
            continue
        matches.append(row)
        if len(matches) >= limit:
            break

    grouped: dict[str, list[dict[str, str]]] = {"attraction": [], "food": []}
    for row in matches:
        grouped.setdefault(row.get("category", "other"), []).append(row)

    return {
        "success": True,
        "data": {
            "city": city,
            "query": query,
            "categories": categories,
            "results": matches,
            "grouped_results": grouped,
            "data_path": str(DATA_PATH),
        },
        "summary": f"Loaded {len(matches)} local knowledge records for {city} from CSV.",
    }
