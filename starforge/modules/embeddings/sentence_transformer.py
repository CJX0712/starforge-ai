"""sentence-transformers 后端 — 复用业界领先开源向量模型（如 all-MiniLM-L6-v2）。

属于可选依赖（requirements-optional.txt），未安装时给出明确指引，不阻断主流程。
Author: 晨星
"""
from __future__ import annotations

from typing import List

from starforge.modules.embeddings.base import EmbeddingProvider


class SentenceTransformerProvider(EmbeddingProvider):
    name = "sentence-transformers"

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer  # 惰性导入
        except ImportError as e:  # pragma: no cover - 可选依赖
            raise RuntimeError(
                "未安装 sentence-transformers，请执行: pip install -r requirements-optional.txt"
            ) from e
        self._model = SentenceTransformer(model_name)
        self.dimension = self._model.get_sentence_embedding_dimension()

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self._model.encode(texts, normalize_embeddings=True).tolist()
