"""测试夹具 — 默认全 mock 后端，保证离线可复现。
Author: 晨星
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from starforge.core.config import Settings
from starforge.core.container import Container

SAMPLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples", "sample.txt")


@pytest.fixture
def settings() -> Settings:
    return Settings(
        llm_provider="mock",
        embedding_provider="mock",
        vectorstore_backend="numpy",
        embedding_dim=384,
    )


@pytest.fixture
def container(settings) -> Container:
    return Container(settings)
