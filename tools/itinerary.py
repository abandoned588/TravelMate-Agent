from __future__ import annotations

from datetime import datetime

from config.settings import ITINERARY_PATH, ensure_project_directories


def save_itinerary(title: str, content: str) -> dict:
    """Save the final itinerary into storage/outputs/itinerary.md."""
    ensure_project_directories()
    try:
        markdown = "\n".join(
            [
                f"# {title}",
                "",
                f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                content.strip(),
                "",
            ]
        )
        ITINERARY_PATH.write_text(markdown, encoding="utf-8")
        return {
            "success": True,
            "data": {"path": str(ITINERARY_PATH), "title": title},
            "summary": f"行程已保存到 {ITINERARY_PATH}",
        }
    except Exception as exc:
        return {"success": False, "error": f"保存行程失败: {exc}"}

