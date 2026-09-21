"""OpenAI 兼容后端 — 通过 httpx 调用任意 OpenAI-compatible 端点（OpenAI / 本地 vLLM / 第三方）。

复用业界标准 /v1/chat/completions 协议，不绑定特定厂商。
Author: 晨星
"""
from __future__ import annotations

from typing import List

import httpx
from starforge.core.observability import get_logger
from starforge.modules.llm.base import LLMProvider, Message

_LOG = get_logger("starforge.llm.openai")


class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(
        self, api_key: str, base_url: str, model: str, timeout: float = 60.0
    ):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout

    def complete(self, prompt: str, **kwargs) -> str:
        return self.chat([Message(role="user", content=prompt)], **kwargs)

    def chat(self, messages: List[Message], **kwargs) -> str:
        if not self._api_key:
            raise RuntimeError("未设置 OPENAI_API_KEY，无法调用 OpenAI 兼容后端。")
        url = f"{self._base_url}/chat/completions"
        payload = {
            "model": kwargs.get("model", self._model),
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": kwargs.get("temperature", 0.2),
            "stream": False,
        }
        headers = {"Authorization": f"Bearer {self._api_key}"}
        try:
            resp = httpx.post(
                url, json=payload, headers=headers, timeout=self._timeout
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except httpx.HTTPError as e:
            _LOG.error("OpenAI 请求失败: %s", e)
            raise RuntimeError(f"OpenAI 后端调用失败: {e}") from e
