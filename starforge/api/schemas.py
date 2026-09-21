"""API 数据结构 — 单一职责：定义请求/响应契约。
Author: 晨星
"""
from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    author: str
    components: Dict[str, str]


class IngestRequest(BaseModel):
    text: Optional[str] = None
    path: Optional[str] = None


class IngestResponse(BaseModel):
    documents: int
    chunks: int


class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = None


class SourceItem(BaseModel):
    id: str
    score: float
    text: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceItem]


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
