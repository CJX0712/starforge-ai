"""Agent 编排 — 最小 ReAct 循环，可接入真实 LLM 或 mock。

真实 LLM 时按 Action/Final Answer 协议多步调用工具；mock 时直接返回确定性回应，
保证离线链路可验证。工具列表通过 get_tools 注入，保持编排与工具解耦。
Author: 晨星
"""
from __future__ import annotations

import re
from typing import Dict, List

from starforge.core.observability import get_logger
from starforge.modules.agent.tools import get_tools
from starforge.modules.llm.base import LLMProvider, Message
from starforge.modules.retrieval.retriever import Retriever

_LOG = get_logger("starforge.agent")

_SYSTEM = (
    "你是一个具备工具调用能力的助手。可用工具：knowledge_search(查询知识库), calculator(数学表达式)。\n"
    "当需要工具时，输出单行：Action: <工具名>(<参数>)\n"
    "当可以直接回答时，输出单行：Final Answer: <回答>\n"
    "每次只输出一行。"
)


class Agent:
    def __init__(self, llm: LLMProvider, retriever: Retriever, max_steps: int = 5):
        self._llm = llm
        self._retriever = retriever
        self._tools = get_tools(retriever)
        self._max_steps = max_steps

    def run(self, query: str) -> Dict[str, Any]:
        messages = [
            Message(role="system", content=_SYSTEM),
            Message(role="user", content=query),
        ]
        trace: List[str] = []
        for _ in range(self._max_steps):
            reply = self._llm.chat(messages)
            trace.append(reply)
            if reply.startswith("Final Answer:"):
                return {"answer": reply[len("Final Answer:"):].strip(), "trace": trace}
            m = re.match(r"Action:\s*(\w+)\((.*)\)\s*$", reply.strip())
            if m:
                name, arg = m.group(1), m.group(2).strip().strip('"').strip("'")
                if name in self._tools:
                    obs = self._tools[name](arg)
                    messages.append(Message(role="assistant", content=reply))
                    messages.append(Message(role="user", content=f"Observation: {obs}"))
                    continue
            # mock 或未识别动作：直接作为最终回答
            return {"answer": reply, "trace": trace}
        return {"answer": "（达到最大步数，未得出最终答案）", "trace": trace}
