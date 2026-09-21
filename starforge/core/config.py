"""全局配置 — 单一职责：集中读取环境变量/.env，提供类型化 Settings。

所有模块经此读取运行参数；切换 LLM/向量化/向量库后端均通过环境变量完成，
无需改动代码，保证干净环境可一键复现。
Author: 晨星
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # 应用元信息
    app_name: str = "StarForge-AI"
    version: str = "1.0.0"
    author: str = "晨星"

    # LLM 后端: mock | openai | ollama
    llm_provider: str = "mock"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    # 向量化后端: mock | sentence-transformers
    embedding_provider: str = "mock"
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dim: int = 384

    # 向量库后端: numpy | faiss
    vectorstore_backend: str = "numpy"

    # 检索 / 切分
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 3

    # 可观测
    log_level: str = "INFO"
    prometheus_enabled: bool = False

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000


@lru_cache
def get_settings() -> Settings:
    return Settings()
