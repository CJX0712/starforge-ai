"""依赖注入容器 — 单一职责：按 Settings 装配各模块实例。

这是模块间唯一的耦合点：上层（API/CLI/RAG/Agent）只通过 Container 取用接口，
不直接 import 具体实现，从而保证任一模块可独立替换、独立验证。
Author: 晨星
"""
from __future__ import annotations

from starforge.core.config import Settings
from starforge.modules.agent.agent import Agent
from starforge.modules.embeddings.base import EmbeddingProvider
from starforge.modules.embeddings.mock import MockEmbeddingProvider
from starforge.modules.embeddings.sentence_transformer import SentenceTransformerProvider
from starforge.modules.llm.base import LLMProvider
from starforge.modules.llm.mock import MockLLMProvider
from starforge.modules.llm.ollama_provider import OllamaProvider
from starforge.modules.llm.openai_provider import OpenAIProvider
from starforge.modules.rag.pipeline import RAGPipeline
from starforge.modules.retrieval.retriever import Retriever
from starforge.modules.vectorstore.base import VectorStore
from starforge.modules.vectorstore.faiss_store import FAISSVectorStore
from starforge.modules.vectorstore.numpy_store import NumpyVectorStore


class Container:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm: LLMProvider = self._build_llm(settings)
        self.embedding: EmbeddingProvider = self._build_embedding(settings)
        self.vectorstore: VectorStore = self._build_vectorstore(settings)
        self.retriever: Retriever = Retriever(self.embedding, self.vectorstore)
        self.rag: RAGPipeline = RAGPipeline(self.retriever, self.llm, settings)
        self.agent: Agent = Agent(self.llm, self.retriever)

    @staticmethod
    def _build_llm(settings: Settings) -> LLMProvider:
        if settings.llm_provider == "openai":
            return OpenAIProvider(
                settings.openai_api_key, settings.openai_base_url, settings.openai_model
            )
        if settings.llm_provider == "ollama":
            return OllamaProvider(settings.ollama_base_url, settings.ollama_model)
        return MockLLMProvider()

    @staticmethod
    def _build_embedding(settings: Settings) -> EmbeddingProvider:
        if settings.embedding_provider == "sentence-transformers":
            return SentenceTransformerProvider(settings.embedding_model)
        return MockEmbeddingProvider(dimension=settings.embedding_dim)

    @staticmethod
    def _build_vectorstore(settings: Settings) -> VectorStore:
        if settings.vectorstore_backend == "faiss":
            return FAISSVectorStore()
        return NumpyVectorStore()

    @classmethod
    def from_settings(cls, settings: Settings) -> "Container":
        return cls(settings)
