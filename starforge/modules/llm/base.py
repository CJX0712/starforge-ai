"""LLM 抽象接口 — 单一职责：定义文本生成契约，屏蔽具体后端差异。
Author: 晨星
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    role: str  # system | user | assistant
    content: str


class LLMProvider(ABC):
    name: str = "base"

    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        """单次补全。"""

    @abstractmethod
    def chat(self, messages: List[Message], **kwargs) -> str:
        """多轮对话。"""
