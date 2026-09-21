"""Agent 工具集 — 单一职责：可被编排调用的原子能力。

每个工具是 (str) -> str 的纯函数，便于真实 LLM 解析 Action 后调用，也便于离线单测。
Author: 晨星
"""
from __future__ import annotations

from typing import Callable, Dict

from starforge.modules.retrieval.retriever import Retriever


def knowledge_search(retriever: Retriever, query: str, top_k: int = 3) -> str:
    results = retriever.retrieve(query, top_k=top_k)
    if not results:
        return "（知识库为空，无相关片段）"
    return "\n".join(
        f"[{i + 1}] {r.payload.get('text', '')[:300]}" for i, r in enumerate(results)
    )


def calculator(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "不支持的表达式（仅允许数字与 + - * / ( ) ）"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))  # 受限求值，禁用内置
    except Exception as e:  # pragma: no cover
        return f"计算错误: {e}"


def get_tools(retriever: Retriever) -> Dict[str, Callable[[str], str]]:
    return {
        "knowledge_search": lambda q: knowledge_search(retriever, q),
        "calculator": calculator,
    }
