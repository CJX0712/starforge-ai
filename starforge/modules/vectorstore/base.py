"""向量库抽象接口与结果结构 — 单一职责：向量存取与相似检索契约。
Author: 晨星
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SearchResult:
    id: str
    score: float  # 相似度，越高越相关
    payload: Dict[str, Any]


class VectorStore(ABC):
    @abstractmethod
    def add(self, id: str, vector: List[float], payload: Dict[str, Any]) -> None:
        """写入一条向量及附属元数据。"""

    @abstractmethod
    def search(self, vector: List[float], top_k: int = 3) -> List[SearchResult]:
        """返回最相似的 top_k 条结果（按 score 降序）。"""
