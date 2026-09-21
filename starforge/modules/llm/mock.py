"""Mock LLM — 确定性输出，用于离线验证与测试，无需网络/密钥。

相同输入恒定返回相同输出，保证测试可复现；实际部署时切换为 openai/ollama 后端。
Author: 晨星
"""
from __future__ import annotations

from typing import List

from starforge.modules.llm.base import LLMProvider, Message


class MockLLMProvider(LLMProvider):
    name = "mock"

    def complete(self, prompt: str, **kwargs) -> str:
        snippet = " ".join(prompt.split())[:160]
        return (
            f"[MOCK 回答] 已基于提供的上下文进行分析。问题摘要：{snippet}。"
            "（这是确定性离线 mock 响应，用于端到端验证；配置真实 LLM 后端后即可获得实际生成结果。）"
        )

    def chat(self, messages: List[Message], **kwargs) -> str:
        last = messages[-1].content if messages else ""
        snippet = " ".join(last.split())[:160]
        return (
            f"[MOCK 对话] 针对用户最新消息「{snippet}」，"
            "给出确定性离线回应。（mock 模式不调用真实模型。）"
        )
