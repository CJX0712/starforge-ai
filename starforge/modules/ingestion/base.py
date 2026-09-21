"""摄入抽象接口与数据结构 — 单一职责：定义文档/切片契约。
Author: 晨星
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Document:
    id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class Ingestor(ABC):
    @abstractmethod
    def load(self, source: str) -> List[Document]:
        """从路径/目录/纯文本加载为 Document 列表。"""

    @abstractmethod
    def chunk(self, doc: Document, size: int, overlap: int) -> List[Chunk]:
        """将文档切分为定长重叠切片。"""
