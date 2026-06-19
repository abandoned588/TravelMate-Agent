from __future__ import annotations

from typing import Any

from openai import OpenAI

from config.settings import get_settings
from core.exceptions import ConfigurationError, LLMClientError


class LLMCompatibleClient:
    """Small wrapper around the OpenAI-compatible chat completions API.

    The project defaults to DeepSeek's OpenAI-compatible endpoint.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        if not self.settings.has_llm_credentials:
            raise ConfigurationError(
                "Missing DeepSeek/OpenAI-compatible credentials in .env. "
                "Set DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, and DEEPSEEK_MODEL_NAME "
                "or their OPENAI-compatible fallbacks."
            )
        self.client = OpenAI(
            api_key=self.settings.llm_api_key,
            base_url=self.settings.llm_base_url,
        )

    def create_chat_completion(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | dict[str, Any] = "auto",
        temperature: float = 0.2,
        stream: bool = False,
    ) -> Any:
        try:
            payload: dict[str, Any] = {
                "model": self.settings.model_name,
                "messages": messages,
                "temperature": temperature,
                "stream": stream,
            }
            if tools is not None:
                payload["tools"] = tools
                payload["tool_choice"] = tool_choice
            return self.client.chat.completions.create(**payload)
        except Exception as exc:
            raise LLMClientError(f"LLM request failed: {exc}") from exc