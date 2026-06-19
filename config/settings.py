from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from config.constants import DEFAULT_REQUEST_TIMEOUT


BASE_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = BASE_DIR / "core"
TOOLS_DIR = BASE_DIR / "tools"
SERVICES_DIR = BASE_DIR / "services"
SCHEMAS_DIR = BASE_DIR / "schemas"
PROMPTS_DIR = BASE_DIR / "prompts"
UI_DIR = BASE_DIR / "ui"
WEB_DIR = BASE_DIR / "web"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = BASE_DIR / "tests"
SCRIPTS_DIR = BASE_DIR / "scripts"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_CACHE_DIR = STORAGE_DIR / "cache"
STORAGE_LOGS_DIR = STORAGE_DIR / "logs"
STORAGE_OUTPUTS_DIR = STORAGE_DIR / "outputs"
WEATHER_CACHE_PATH = STORAGE_CACHE_DIR / "weather_cache.json"
POI_CACHE_PATH = STORAGE_CACHE_DIR / "poi_cache.json"
TOOL_TRACE_PATH = STORAGE_LOGS_DIR / "tool_trace.jsonl"
ITINERARY_PATH = STORAGE_OUTPUTS_DIR / "itinerary.md"


@dataclass
class Settings:
    llm_api_key: str
    llm_base_url: str
    model_name: str
    amap_api_key: str
    geoapify_api_key: str
    request_timeout: int = DEFAULT_REQUEST_TIMEOUT

    @property
    def has_llm_credentials(self) -> bool:
        return bool(self.llm_api_key and self.llm_base_url and self.model_name)

    @property
    def has_amap_key(self) -> bool:
        return bool(self.amap_api_key)

    @property
    def has_geoapify_key(self) -> bool:
        return bool(self.geoapify_api_key)


def ensure_project_directories() -> None:
    directories = [
        CORE_DIR,
        TOOLS_DIR,
        SERVICES_DIR,
        SCHEMAS_DIR,
        PROMPTS_DIR,
        UI_DIR,
        WEB_DIR,
        DOCS_DIR,
        TESTS_DIR,
        SCRIPTS_DIR,
        SCREENSHOTS_DIR,
        STORAGE_DIR,
        STORAGE_CACHE_DIR,
        STORAGE_LOGS_DIR,
        STORAGE_OUTPUTS_DIR,
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    json_seed_files = {
        WEATHER_CACHE_PATH: "{}\n",
        POI_CACHE_PATH: "{}\n",
    }
    for path, content in json_seed_files.items():
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    if not TOOL_TRACE_PATH.exists():
        TOOL_TRACE_PATH.write_text("", encoding="utf-8")
    if not ITINERARY_PATH.exists():
        ITINERARY_PATH.write_text("", encoding="utf-8")


def get_settings() -> Settings:
    load_dotenv()
    ensure_project_directories()

    llm_api_key = os.getenv("DEEPSEEK_API_KEY", os.getenv("OPENAI_API_KEY", "")).strip()
    llm_base_url = os.getenv(
        "DEEPSEEK_BASE_URL",
        os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1"),
    ).strip()
    model_name = os.getenv(
        "DEEPSEEK_MODEL_NAME",
        os.getenv("MODEL_NAME", "deepseek-chat"),
    ).strip()

    return Settings(
        llm_api_key=llm_api_key,
        llm_base_url=llm_base_url,
        model_name=model_name,
        amap_api_key=os.getenv("AMAP_API_KEY", "").strip(),
        geoapify_api_key=os.getenv("GEOAPIFY_API_KEY", "").strip(),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", str(DEFAULT_REQUEST_TIMEOUT))),
    )