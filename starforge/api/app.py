"""REST 网关 — 单一职责：暴露 HTTP 接口，委托给 Container 中的管线。

端点：/health 健康检查；/ingest 摄入；/query 知识库问答；/chat 对话。
仅在 lifespan 内构建一次 Container，所有请求共享同一内存向量库。
Author: 晨星
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from starforge.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    SourceItem,
)
from starforge.core.config import Settings, get_settings
from starforge.core.container import Container
from starforge.modules.llm.base import Message


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = get_settings()
    app.state.container = Container.from_settings(settings)
    yield


app = FastAPI(title="StarForge-AI", version=get_settings().version, lifespan=lifespan)


def _components(c: Container) -> Dict[str, str]:
    return {
        "llm": c.llm.name,
        "embedding": getattr(c.embedding, "name", c.embedding.__class__.__name__),
        "vectorstore": c.vectorstore.__class__.__name__,
    }


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    c: Container = app.state.container
    s: Settings = get_settings()
    return HealthResponse(
        status="ok", version=s.version, author=s.author, components=_components(c)
    )


@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest) -> IngestResponse:
    c: Container = app.state.container
    source = req.path or req.text or ""
    if not source:
        return IngestResponse(documents=0, chunks=0)
    res = c.rag.ingest(source)
    return IngestResponse(**res)


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest) -> QueryResponse:
    c: Container = app.state.container
    res = c.rag.answer(req.question, top_k=req.top_k)
    return QueryResponse(
        answer=res["answer"],
        sources=[SourceItem(**s) for s in res["sources"]],
    )


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    c: Container = app.state.container
    messages = [Message(role=m.role, content=m.content) for m in req.messages]
    reply = c.llm.chat(messages)
    return ChatResponse(reply=reply)
