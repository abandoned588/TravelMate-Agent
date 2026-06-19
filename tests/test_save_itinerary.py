from pathlib import Path
from uuid import uuid4

import tools.itinerary as itinerary_module


def test_save_itinerary_writes_markdown(monkeypatch) -> None:
    output_path = Path(f"storage/outputs/test_itinerary_{uuid4().hex}.md").resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(itinerary_module, "ITINERARY_PATH", output_path)
    monkeypatch.setattr(itinerary_module, "ensure_project_directories", lambda: None)

    result = itinerary_module.save_itinerary("Hangzhou Trip", "## Day 1\n- West Lake")

    assert result["success"] is True
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "# Hangzhou Trip" in content
    assert "## Day 1" in content
