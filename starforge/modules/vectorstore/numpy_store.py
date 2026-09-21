"""纯 NumPy 向量库 — 零外部依赖，干净环境默认可用。

基于余弦相似度检索；作为默认后端保证一键复现与离线验证。
Author: 晨星
"""
from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
from starforge.modules.vectorstore.base import SearchResult, VectorStore


class NumpyVectorStore(VectorStore):
    def __init__(self) -> None:
        self._ids: List[str] = []
        self._vectors: List[List[float]] = []
        self._payloads: List[Dict[str, Any]] = []

    def add(self, id: str, vector: List[float], payload: Dict[str, Any]) -> None:
        self._ids.append(id)
        self._vectors.append(list(vector))
        self._payloads.append(payload)

    def search(self, vector: List[float], top_k: int = 3) -> List[SearchResult]:
        if not self._vectors:
            return []
        q = np.asarray(vector, dtype=float)
        qn = np.linalg.norm(q) or 1.0
        q = q / qn
        mat = np.asarray(self._vectors, dtype=float)
        norms = np.linalg.norm(mat, axis=1)
        norms[norms == 0] = 1.0
        mat = mat / norms[:, None]
        sims = mat @ q  # 余弦相似度
        idx = np.argsort(-sims)[:top_k]
        return [
            SearchResult(
                id=self._ids[i], score=float(sims[i]), payload=self._payloads[i]
            )
            for i in idx
        ]
