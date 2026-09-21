"""RAG 生成管线 — 组合摄入 / 检索 / LLM，形成可独立验证的问答能力。

输入文档 -> 切分 -> 向量化 -> 入库；输入问题 -> 检索上下文 -> 拼接提示 -> LLM 生成。
Author: 晨星
"""
from __future__ import annotations

from typing import Any, Dict

from starforge.core.config import Settings, get_settings
from starforge.core.observability import get_logger
from starforge.modules.ingestion.loaders import FileIngestor
from starforge.modules.llm.base import LLMProvider
from starforge.modules.retrieval.retriever import Retriever

_LOG = get_logger("starforge.rag")

_PROMPT = (
    "你是企业知识助手。请仅基于下面的【上下文】用中文回答用户问题；"
    "若上下文不足，请明确说明无法回答。\n\n【上下文】\n{context}\n\n【问题】\n{question}\n\n【回答】"
)


class RAGPipeline:
    def __init__(self, retriever: Retriever, llm: LLMProvider, settings: Settings | None = None):
        self._retriever = retriever
        self._llm = llm
        self._ingestor = FileIngestor()
        self._settings = settings or get_settings()

    def ingest(self, source: str) -> Dict[str, Any]:
        docs = self._ingestor.load(source)
        total = 0
        for d in docs:
            chunks = self._ingestor.chunk(
                d, self._settings.chunk_size, self._settings.chunk_overlap
            )
            total += self._retriever.index_chunks(chunks)
        return {"documents": len(docs), "chunks": total}

    def answer(self, question: str, top_k: int | None = None) -> Dict[str, Any]:
        top_k = top_k or self._settings.top_k
        results = self._retriever.retrieve(question, top_k=top_k)
        context = "\n---\n".join(r.payload.get("text", "") for r in results)
        prompt = _PROMPT.format(context=context, question=question)
        text = self._llm.complete(prompt)
        return {
            "answer": text,
            "sources": [
                {
                    "id": r.id,
                    "score": round(r.score, 4),
                    "text": r.payload.get("text", "")[:200],
                }
                for r in results
            ],
        }
