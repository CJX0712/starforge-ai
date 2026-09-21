from starforge.modules.agent.tools import calculator, get_tools

from tests.conftest import SAMPLE


def test_tools_registry(container):
    tools = get_tools(container.retriever)
    assert set(tools.keys()) == {"knowledge_search", "calculator"}


def test_calculator():
    assert calculator("(1+2)*3") == "9"
    assert "不支持" in calculator("import os")


def test_agent_run_offline(container):
    container.rag.ingest(SAMPLE)
    out = container.agent.run("请告诉我 StarForge 的定位")
    assert out["answer"]
    assert "trace" in out
    assert isinstance(out["trace"], list)
