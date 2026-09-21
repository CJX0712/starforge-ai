"""FAISS 向量库 — 可选高性能后端（CPU 即可，免服务进程）。

未安装 faiss-cpu 时给出明确指引；安装后通过 VECTORSTORE_BACKEND=faiss 启用。
Author: 晨星
"""
from __future__ import annotations

from typing import Any, Dict, List

from starforge.modules.vectorstore.base import SearchResult, VectorStore


class FAISSVectorStore(VectorStore):
    def __init__(self) -> None:
        try:
            import faiss  # 惰性导入
        except ImportError as e:  # pragma: no cover - 可选依赖
            raise RuntimeError(
                "未安装 faiss-cpu，请执行: pip install -r requirements-optional.txt"
            ) from e
        self._faiss = faiss
        self._index = None
        self._ids: List[str] = []
        self._payloads: List[Dict[str, Any]] = []

    def add(self, id: str, vector: List[float], payload: Dict[str, Any]) -> None:
        import numpy as np

        v = np.asarray([vector], dtype="float32")
        if self._index is None:
            self._index = self._faiss.IndexFlatL2(len(vector))
        self._index.add(v)
        self._ids.append(id)
        self._payloads.append(payload)

    def search(self, vector: List[float], top_k: int = 3) -> List[SearchResult]:
        if self._index is None or self._index.ntotal == 0:
            return []
        import numpy as np

        q = np.asarray([vector], dtype="float32")
        k = min(top_k, self._index.ntotal)
        distances, indices = self._index.search(q, k)
        results: List[SearchResult] = []
        for dist, i in zip(distances[0], indices[0]):
            if i < 0:
                continue
            sim = 1.0 / (1.0 + float(dist))  # L2 距离 -> 相似度
            results.append(
                SearchResult(id=self._ids[i], score=sim, payload=self._payloads[i])
            )
        return results
