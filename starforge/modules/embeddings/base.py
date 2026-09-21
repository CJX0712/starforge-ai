"""向量化抽象接口 — 单一职责：定义文本到向量的契约。
Author: 晨星
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    name: str = "base"
    dimension: int = 0

    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """批量将文本编码为向量列表。"""
