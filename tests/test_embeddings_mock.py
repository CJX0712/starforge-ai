import math

from starforge.modules.embeddings.mock import MockEmbeddingProvider


def test_dimension():
    e = MockEmbeddingProvider(384)
    assert e.dimension == 384


def test_deterministic():
    e = MockEmbeddingProvider(384)
    v1 = e.embed(["深度学习是机器学习的一个分支"])[0]
    v2 = e.embed(["深度学习是机器学习的一个分支"])[0]
    assert v1 == v2


def test_similarity_bounded():
    e = MockEmbeddingProvider(384)
    v1 = e.embed(["StarForge 是模块化 AI 平台"])[0]
    v3 = e.embed(["苹果 香蕉 水果 营养"])[0]
    dot = sum(a * b for a, b in zip(v1, v3))
    assert -1.0 <= dot <= 1.0
    # 相同文本相似度应为 1
    v_same = e.embed(["StarForge 是模块化 AI 平台"])[0]
    same = sum(a * b for a, b in zip(v1, v_same))
    assert abs(same - 1.0) < 1e-9
