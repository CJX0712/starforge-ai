"""检索模块 — 单一职责：把切片索引进向量库，并按查询召回相似切片。

组合 EmbeddingProvider 与 VectorStore，是 RAG 与 Agent 的知识入口。
Author: 晨星
"""
from __future__ import annotations

from typing import List

from starforge.core.observability import get_logger
from starforge.modules.embeddings.base import EmbeddingProvider
from starforge.modules.ingestion.base import Chunk
from starforge.modules.vectorstore.base import SearchResult, VectorStore

_LOG = get_logger("starforge.retrieval")


class Retriever:
    def __init__(self, embedding: EmbeddingProvider, vectorstore: VectorStore):
        self._embedding = embedding
        self._store = vectorstore

    def index_chunks(self, chunks: List[Chunk]) -> int:
        if not chunks:
            return 0
        vecs = self._embedding.embed([c.text for c in chunks])
        for c, v in zip(chunks, vecs):
            self._store.add(c.id, v, {"text": c.text, **c.metadata})
        _LOG.info("已索引 %d 个切片", len(chunks))
        return len(chunks)

    def retrieve(self, query: str, top_k: int = 3) -> List[SearchResult]:
        (qv,) = self._embedding.embed([query])
        return self._store.search(qv, top_k=top_k)
