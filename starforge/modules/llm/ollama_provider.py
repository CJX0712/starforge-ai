"""Ollama 本地后端 — 通过 httpx 调用本地 Ollama /api/chat，零 API key。

适合本机私有化部署，复用 Ollama 生态模型。
Author: 晨星
"""
from __future__ import annotations

from typing import List

import httpx
from starforge.core.observability import get_logger
from starforge.modules.llm.base import LLMProvider, Message

_LOG = get_logger("starforge.llm.ollama")


class OllamaProvider(LLMProvider):
    name = "ollama"

    def __init__(self, base_url: str, model: str, timeout: float = 120.0):
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout

    def complete(self, prompt: str, **kwargs) -> str:
        return self.chat([Message(role="user", content=prompt)], **kwargs)

    def chat(self, messages: List[Message], **kwargs) -> str:
        url = f"{self._base_url}/api/chat"
        payload = {
            "model": kwargs.get("model", self._model),
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
        }
        try:
            resp = httpx.post(url, json=payload, timeout=self._timeout)
            resp.raise_for_status()
            data = resp.json()
            return data["message"]["content"]
        except httpx.HTTPError as e:
            _LOG.error("Ollama 请求失败: %s", e)
            raise RuntimeError(
                f"Ollama 后端调用失败（确认 Ollama 已启动且模型已拉取）: {e}"
            ) from e
