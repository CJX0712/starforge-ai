"""Mock 向量化 — 确定性，基于词频哈希（TF-hash）。

相同文本恒定同向量；含相同关键词的文本余弦相似度高，足以驱动离线检索验证。
不依赖任何模型权重，干净环境零下载即可运行。
Author: 晨星
"""
from __future__ import annotations

import hashlib
import math
from typing import List

from starforge.modules.embeddings.base import EmbeddingProvider


class MockEmbeddingProvider(EmbeddingProvider):
    name = "mock"

    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def _tokenize(self, text: str) -> List[str]:
        # 空白分词；对含非 ASCII（如中文）的 token 额外展开为字符级特征，
        # 使中文相关文本在余弦空间有非零重叠，保证离线检索有意义。
        feats: List[str] = []
        for tok in text.lower().split():
            feats.append(tok)
            if any(ord(c) > 127 for c in tok):
                feats.extend(list(tok))
        return feats

    def _vec(self, text: str) -> List[float]:
        vec = [0.0] * self.dimension
        for tok in self._tokenize(text):
            h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
            vec[h % self.dimension] += 1.0
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def embed(self, texts: List[str]) -> List[List[float]]:
        return [self._vec(t) for t in texts]
