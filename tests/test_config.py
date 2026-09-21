from starforge.core.config import Settings


def test_defaults():
    s = Settings()
    assert s.llm_provider == "mock"
    assert s.embedding_provider == "mock"
    assert s.vectorstore_backend == "numpy"
    assert s.embedding_dim == 384
    assert s.author == "晨星"
