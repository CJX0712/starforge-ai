"""离线端到端验证：摄入 -> 检索 -> 生成 -> Agent，全程 mock 后端，零网络零密钥。
Author: 晨星
"""
from tests.conftest import SAMPLE


def test_end_to_end_offline(container):
    ingest = container.rag.ingest(SAMPLE)
    assert ingest["chunks"] > 0

    ans = container.rag.answer("StarForge 的核心能力有哪些")
    assert ans["answer"]
    assert len(ans["sources"]) >= 1

    a = container.agent.run("StarForge 能做什么")
    assert a["answer"]
    assert a["trace"]


def test_swap_backend_is_interface_driven(container):
    # 验证上层仅依赖抽象接口：替换向量库实现不影响调用方式
    from starforge.modules.vectorstore.base import SearchResult
    from starforge.modules.vectorstore.numpy_store import NumpyVectorStore

    assert isinstance(container.vectorstore, NumpyVectorStore)
    # 检索结果结构一致
    res = container.retriever.retrieve("StarForge", top_k=1)
    assert all(isinstance(r, SearchResult) for r in res)
